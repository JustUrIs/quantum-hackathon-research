"""Bounded interpreter for a documented Python/Qiskit circuit-building subset.

No user exec/eval, modules, filesystem or dynamic attribute access. This is a
language implementation for local practice, not a server Python sandbox.
Oracle calls produce symbolic instructions; the secret is never given to solve.
"""
import ast
import json
import math
import operator

VERSION = "qcp-1.0"


class VerdictError(Exception):
    def __init__(self, status, message):
        self.status = status
        super().__init__(message)


class Circuit:
    def __init__(self, width, limit):
        if type(width) is not int or not 1 <= width <= limit:
            raise VerdictError("QLE", f"Use at most {limit} qubits, including the oracle target.")
        self.width, self.ops = width, []

    def emit(self, name, args):
        if len(self.ops) >= 512:
            raise VerdictError("DLE", "The instruction limit is 512.")
        if name == "barrier":
            return
        if name in ("h", "x", "y", "z", "s", "sdg", "t", "tdg"):
            if len(args) != 1:
                raise VerdictError("RE", f"{name} expects one qubit or iterable.")
            qubits = list(args[0]) if isinstance(args[0], (list, tuple, range)) else [args[0]]
            for q in qubits:
                self.check([q])
                if len(self.ops) >= 512:
                    raise VerdictError("DLE", "The instruction limit is 512.")
                self.ops.append([name, [q], []])
        elif name in ("rx", "ry", "rz", "p"):
            if len(args) != 2 or not isinstance(args[0], (int, float)) or not math.isfinite(args[0]):
                raise VerdictError("RE", f"{name} expects a finite angle and a qubit.")
            self.check([args[1]])
            self.ops.append([name, [args[1]], [float(args[0])]])
        elif name in ("cx", "cz", "swap", "ccx"):
            if len(args) != (3 if name == "ccx" else 2):
                raise VerdictError("RE", f"Invalid arguments for {name}.")
            self.check(args)
            self.ops.append([name, list(args), []])
        elif name in ("mcx", "mcp"):
            angle = []
            if name == "mcp":
                if len(args) != 3 or not isinstance(args[0], (int, float)) or not math.isfinite(args[0]):
                    raise VerdictError("RE", "mcp expects angle, controls, target.")
                angle, args = [float(args[0])], args[1:]
            if len(args) != 2 or not isinstance(args[0], (list, tuple, range)):
                raise VerdictError("RE", f"{name} expects controls and target.")
            qubits = list(args[0]) + [args[1]]
            self.check(qubits)
            self.ops.append([name, qubits, angle])
        else:
            raise VerdictError("UGE", f"Unsupported instruction: {name}. The judge adds readout.")

    def check(self, qubits):
        if any(type(q) is not int or not 0 <= q < self.width for q in qubits):
            raise VerdictError("RE", "Qubit index outside the allocated register.")
        if len(set(qubits)) != len(qubits):
            raise VerdictError("RE", "Controls and targets must be distinct.")


class Interpreter:
    def __init__(self, n):
        self.n, self.budget, self.result = n, 12000, None
        self.env = {"n": n, "oracle": "@oracle", "QuantumCircuit": "@circuit", "math": "@math"}

    def tick(self, node):
        self.budget -= 1
        if self.budget < 0:
            raise VerdictError("TLE", "Circuit-building step budget exceeded.")

    def expr(self, node):
        self.tick(node)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float, bool):
            if not math.isfinite(node.value) or abs(node.value) > 1_000_000:
                raise VerdictError("RE", "Numeric literal outside the supported range.")
            return node.value
        if isinstance(node, ast.Name):
            if node.id not in self.env:
                raise VerdictError("RE", f"Unknown name: {node.id}.")
            return self.env[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            return [self.expr(x) for x in node.elts]
        if isinstance(node, ast.BinOp):
            left, right = self.expr(node.left), self.expr(node.right)
            functions = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                         ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
                         ast.Mod: operator.mod, ast.Pow: operator.pow,
                         ast.BitAnd: operator.and_, ast.BitOr: operator.or_, ast.BitXor: operator.xor}
            if type(node.op) not in functions:
                raise VerdictError("CE", "Unsupported arithmetic operator.")
            if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                raise VerdictError("CE", "Arithmetic is restricted to numbers.")
            if isinstance(node.op, ast.Pow) and abs(right) > 16:
                raise VerdictError("RE", "Exponent limit exceeded.")
            out = functions[type(node.op)](left, right)
            if not isinstance(out, (int, float)) or not math.isfinite(out) or abs(out) > 1e12:
                raise VerdictError("RE", "Numeric result outside the supported range.")
            return out
        if isinstance(node, ast.UnaryOp):
            value = self.expr(node.operand)
            if isinstance(node.op, ast.USub): return -value
            if isinstance(node.op, ast.UAdd): return +value
            if isinstance(node.op, ast.Not): return not value
        if isinstance(node, ast.Compare):
            funcs = {ast.Eq: operator.eq, ast.NotEq: operator.ne, ast.Lt: operator.lt,
                     ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge}
            left = self.expr(node.left)
            for op, other in zip(node.ops, node.comparators):
                right = self.expr(other)
                if type(op) not in funcs or not funcs[type(op)](left, right): return False
                left = right
            return True
        if isinstance(node, ast.Subscript):
            value = self.expr(node.value)
            if not isinstance(value, (list, tuple, range)):
                raise VerdictError("CE", "Indexing is restricted to lists and ranges.")
            if isinstance(node.slice, ast.Slice):
                parts = [self.expr(x) if x else None for x in (node.slice.lower, node.slice.upper, node.slice.step)]
                return value[slice(*parts)]
            return value[self.expr(node.slice)]
        if isinstance(node, ast.Attribute):
            owner = self.expr(node.value)
            if owner == "@math" and node.attr in ("pi", "e"):
                return getattr(math, node.attr)
            raise VerdictError("CE", "Only supported circuit methods and math constants are exposed.")
        if isinstance(node, ast.Call):
            if node.keywords:
                raise VerdictError("CE", "Use positional arguments in this first release.")
            args = [self.expr(a) for a in node.args]
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name == "QuantumCircuit":
                    if len(args) != 1: raise VerdictError("CE", "Use QuantumCircuit(n + 1).")
                    return Circuit(args[0], self.n + 1)
                if name == "oracle":
                    if len(args) != 3 or not isinstance(args[0], Circuit):
                        raise VerdictError("RE", "Use oracle(qc, range(n), n).")
                    qc, inputs, target = args
                    if list(inputs) != list(range(self.n)) or target != self.n or qc.width != self.n + 1:
                        raise VerdictError("RE", "Oracle registers must be range(n) and target n, in order.")
                    if len(qc.ops) >= 512: raise VerdictError("DLE", "The instruction limit is 512.")
                    qc.ops.append(["oracle", list(range(self.n + 1)), []])
                    return None
                funcs = {"range": range, "list": list, "len": len, "int": int,
                         "float": float, "abs": abs, "min": min, "max": max, "round": round}
                if name in funcs:
                    if name == "range" and any(type(a) is not int or abs(a) > 256 for a in args):
                        raise VerdictError("TLE", "Range arguments must be integers between -256 and 256.")
                    value = funcs[name](*args)
                    if isinstance(value, (list, range)) and len(value) > 256:
                        raise VerdictError("TLE", "Iterable limit exceeded.")
                    return value
            if isinstance(node.func, ast.Attribute):
                owner = self.expr(node.func.value)
                if isinstance(owner, Circuit): return owner.emit(node.func.attr, args)
                if owner == "@math" and node.func.attr in ("sqrt", "floor", "ceil", "sin", "cos"):
                    return getattr(math, node.func.attr)(*args)
            raise VerdictError("CE", "Unsupported call. See the language reference.")
        raise VerdictError("CE", f"Unsupported expression: {type(node).__name__}.")

    def statements(self, body):
        for node in body:
            self.tick(node)
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in ("oracle", "QuantumCircuit", "math", "n"):
                    raise VerdictError("CE", "Do not overwrite judge-provided names.")
                self.env[node.targets[0].id] = self.expr(node.value)
            elif isinstance(node, ast.Expr):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str): continue
                self.expr(node.value)
            elif isinstance(node, ast.For) and isinstance(node.target, ast.Name) and not node.orelse:
                if node.target.id in ("n", "oracle", "QuantumCircuit", "math"):
                    raise VerdictError("CE", "Do not overwrite judge-provided names.")
                iterable = self.expr(node.iter)
                if not isinstance(iterable, (list, tuple, range)) or len(iterable) > 256:
                    raise VerdictError("TLE", "For loops require a bounded list or range.")
                for value in iterable:
                    self.env[node.target.id] = value
                    if self.statements(node.body): return True
            elif isinstance(node, ast.If):
                if self.statements(node.body if self.expr(node.test) else node.orelse): return True
            elif isinstance(node, ast.Return):
                self.result = self.expr(node.value)
                return True
            elif isinstance(node, ast.Pass): continue
            else:
                raise VerdictError("CE", f"Unsupported statement: {type(node).__name__}.")
        return False


def compile_solution(source, n):
    if not isinstance(source, str) or len(source) > 16000:
        raise VerdictError("CE", "Source limit is 16,000 characters.")
    try:
        tree = ast.parse(source)
        if sum(1 for _ in ast.walk(tree)) > 2500:
            raise VerdictError("CE", "Source is too complex for this release.")
        functions = []
        for node in tree.body:
            if isinstance(node, ast.Import) and all(a.name == "math" and a.asname is None for a in node.names): continue
            if isinstance(node, ast.ImportFrom) and node.module == "qiskit" and node.level == 0 and all(a.name == "QuantumCircuit" and a.asname is None for a in node.names): continue
            if isinstance(node, ast.FunctionDef): functions.append(node)
            else: raise VerdictError("CE", "Only math, QuantumCircuit and def solve(n, oracle) are allowed at top level.")
        if len(functions) != 1:
            raise VerdictError("CE", "Define exactly one function: solve(n, oracle).")
        fn = functions[0]
        if (fn.name != "solve" or [a.arg for a in fn.args.args] != ["n", "oracle"]
                or fn.args.posonlyargs or fn.args.kwonlyargs or fn.args.vararg or fn.args.kwarg
                or fn.args.defaults or fn.decorator_list):
            raise VerdictError("CE", "Use def solve(n, oracle), without decorators or default arguments.")
        vm = Interpreter(n)
        vm.statements(fn.body)
        if not isinstance(vm.result, Circuit):
            raise VerdictError("RE", "solve must return its QuantumCircuit.")
        if vm.result.width != n + 1:
            raise VerdictError("QLE", "Allocate exactly n + 1 qubits for these problems.")
        return {"width": vm.result.width, "ops": vm.result.ops}
    except VerdictError: raise
    except SyntaxError as exc:
        raise VerdictError("CE", f"Line {exc.lineno}: {exc.msg}.") from exc
    except Exception as exc:
        raise VerdictError("RE", f"{type(exc).__name__}: {str(exc)[:180]}") from exc


def compile_batch(source, sizes=None):
    try:
        return json.dumps({"version": VERSION, "circuits": {str(n): compile_solution(source, n) for n in (sizes or range(2, 7))}})
    except VerdictError as exc:
        return json.dumps({"status": exc.status, "message": str(exc)})
