let worker = null;
let active = null;
export function run(payload, progress) {
  if (globalThis.QCPJudge) return globalThis.QCPJudge(payload, progress);
  return new Promise(resolve => {
    worker ||= new Worker(new URL('./worker.js', import.meta.url));
    const finish = result => { if (!active) return; clearTimeout(active.timer); active = null; resolve(result); };
    active = {finish, timer:setTimeout(() => {
      worker.terminate(); worker = null;
      finish({status:'JE',message:'Judge runtime exceeded 90 seconds. It was stopped; retry without a contest penalty.',source:'Browser runtime'});
    },90000)};
    worker.onmessage = e => { if (e.data.stage) progress(e.data.stage); else finish(e.data.result); };
    worker.onerror = e => { worker.terminate(); worker=null; finish({status:'JE',message:e.message,source:'Browser runtime'}); };
    worker.postMessage(payload);
  });
}
export function cancel() {
  if (active) {
    worker.terminate(); worker=null;
    active.finish({status:'CANCELLED',message:'Execution cancelled. This attempt does not count toward contest penalties.'});
  }
}
