{ source, system ? "x86_64-linux", juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
(builtins.getFlake source).lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; }
