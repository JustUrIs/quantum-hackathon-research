import * as judge from 'qcp.service';
globalThis.QCPMode = 'Qollab · Qiskit Statevector';
globalThis.QCPCatalog = JSON.parse(await judge.catalog.callPromising());
globalThis.QCPJudge = async (payload, progress) => {
  progress('Qiskit is checking the test suite…');
  return JSON.parse(await judge.evaluate.callPromising(JSON.stringify(payload)));
};
await import('./main.js');
