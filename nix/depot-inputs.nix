{ source, system ? "x86_64-linux", juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
(builtins.getFlake source).lib.depotCompatibilityInputs { inherit system juliaTestProfile juliaTestWorkerLimit; }
