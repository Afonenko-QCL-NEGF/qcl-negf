# Requires explicit tiny manufactured fixture and cached nixpkgs; evaluates only.
{ fixture, nixpkgs }:
let r=../.; f=/. + fixture;
 p=import (/. + nixpkgs) {system="x86_64-linux";};
 policy=import (r+"/nix/depot-compatibility.nix");
 julia={drvPath="/nix/store/11111111111111111111111111111111-julia.drv";outPath="/nix/store/22222222222222222222222222222222-julia";};
 input = name: workers: policy.inputs {root=f+"/${name}";inherit julia;system="x86_64-linux";juliaTestProfile="production-build";juliaTestWorkerLimit=workers;};
 depot=import (r+"/nix/depot.nix") {pkgs=p;metadata={url="https://example.invalid/depot.tar";hash="sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";};};
 runtime = name: let sources=import (r+"/nix/runtime-sources.nix") {lib=p.lib;root=f+"/${name}";};
 in import (r+"/components/QCLNEGFRunner.jl/nix/package.nix") {pkgs=p;julia=julia.outPath;preparedDepot=depot;coreSrc=sources.core;runnerSrc=sources.runner;environmentSrc=sources.environment;};
 hold = name: let t=builtins.tryEval (builtins.deepSeq (input name 2) true);in !t.success;
 a=input "a" 2;
in assert a==input "docs" 2;
assert a==input "source" 2;
assert a!=input "project" 2;
assert a!=input "alias" 2;
assert a!=input "a" 4;
assert hold "selector" && hold "prefs";
assert (runtime "a").drvPath==(runtime "docs").drvPath;
assert (runtime "a").drvPath!=(runtime "source").drvPath;
{inputs_sha256=policy.hash a;docs_runtime_drv=(runtime "docs").drvPath;source_runtime_drv=(runtime "source").drvPath;depot_drv=depot.drvPath;unknown_selector_hold=hold "selector";custom_preferences_hold=hold "prefs";}
