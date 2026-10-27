# Evaluation receipt for the real composed capture runtime; never realizes it.
# Caller supplies an existing prepared depot and the current local source flake.
# Inspect capture_drv recursively after evaluation to verify its dependency graph.
{ root, preparedDepot, system ? "x86_64-linux" }:
let
  release = builtins.getFlake (toString root);
  application = release.lib.mkApplication { inherit system; };
  capture = application.captureRuntime;
  captureExecutable = "${capture}/bin/qcl-negf-results";
  solver = release.lib.mkSolver { inherit system preparedDepot; };
  context = builtins.getContext captureExecutable;
in
assert capture.type == "derivation";
assert capture.outPath != application.outPath;
# The immutable executable carries only the capture derivation string context,
# rather than a context reference to the full application environment.
assert builtins.attrNames context == [ capture.drvPath ];
assert context.${capture.drvPath}.outputs == [ "out" ];
{
  capture_executable = captureExecutable;
  capture_drv = capture.drvPath;
  application_drv = application.drvPath;
  solver_drv = solver.drvPath;
}
