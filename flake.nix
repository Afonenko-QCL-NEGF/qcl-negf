{
  description = "QCL-NEGF integrated source graph and development environment";
  inputs.self.submodules = true;
  inputs.platform.url = "path:./components/qcl-negf-platform";
  outputs = { self, platform }: let
    systems = [ "x86_64-linux" "aarch64-linux" ];
    forAll = platform.inputs.nixpkgs.lib.genAttrs systems;
  in {
    inherit (platform) nixosModules;
    lib = {
      mkPinnedJulia = { system, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
        import ./components/QCLNEGFRunner.jl/nix/julia.nix {
          pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
          testProfile = juliaTestProfile; testWorkerLimit = juliaTestWorkerLimit;
        };
      depotCompatibilityInputs = { system, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
        (import ./nix/depot-compatibility.nix).inputs {
          root = ./.; inherit system juliaTestProfile juliaTestWorkerLimit;
          julia = self.lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; };
        };
      mkPreparedDepot = { system, metadata, juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
        policy = import ./nix/depot-compatibility.nix;
        v2 = metadata.format == "qcl-negf.julia-depot.v2";
        expected = self.lib.depotCompatibilityInputs { inherit system juliaTestProfile juliaTestWorkerLimit; };
        manifest = builtins.hashFile "sha256" ./julia/Manifest.toml;
        depot = import ./nix/depot.nix { inherit pkgs; metadata = { inherit (metadata) url hash; }; };
      in assert metadata.julia == "1.13.0";
         assert metadata.juliaManifest == manifest;
         assert if v2 then policy.valid { inherit metadata expected manifest; }
           else metadata.format == "qcl-negf.julia-depot.v1" && metadata.sources.revision == self.rev;
         depot // { qclDepotFormat = metadata.format;
           qclDepotInputsSha256 = if v2 then policy.hash expected else null; };
      mkApplication = { system }: platform.lib.mkApplication {
        inherit system;
        workspaceRoot = self.outPath;
      };
      mkSolver = { system, preparedDepot, juliaTestProfile ? "production-build",
        juliaTestWorkerLimit ? null }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
        runtimeSources = import ./nix/runtime-sources.nix {
          inherit (pkgs) lib;
          root = ./.;
        };
      in assert (preparedDepot.qclDepotFormat or null) != "qcl-negf.julia-depot.v2" ||
        preparedDepot.qclDepotInputsSha256 == (import ./nix/depot-compatibility.nix).hash
          (self.lib.depotCompatibilityInputs { inherit system juliaTestProfile juliaTestWorkerLimit; });
      import ./components/QCLNEGFRunner.jl/nix/package.nix {
        inherit pkgs preparedDepot;
        # Select only the Results capture CLI from the shared locked PythonSet.
        # Runner retains one ordinary spawn when this capability is unavailable.
        captureExecutable = "${(self.lib.mkApplication { inherit system; }).captureRuntime}/bin/qcl-negf-results";
        testProfile = juliaTestProfile;
        julia = self.lib.mkPinnedJulia { inherit system juliaTestProfile juliaTestWorkerLimit; };
        coreSrc = runtimeSources.core;
        runnerSrc = runtimeSources.runner;
        environmentSrc = runtimeSources.environment;
      };
    };
    packages = forAll (system: {
      application = self.lib.mkApplication { inherit system; };
      default = self.packages.${system}.application;
    });
    devShells = forAll (system: let
      pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = with pkgs; [ deno git gh nix nixos-rebuild uv python314 nodejs_24 prefetch-npm-deps opentofu ansible ];
        shellHook = ''
          export NIX_CONFIG="experimental-features = nix-command flakes"
        '';
      };
    });
    checks = forAll (system: {
      inherit (platform.checks.${system}) operations infrastructure slurm-vm;
    });
  };
}
