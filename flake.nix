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
      mkPreparedDepot = { system, metadata }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
      in assert metadata.format == "qcl-negf.julia-depot.v1";
         assert metadata.julia == "1.13.0";
         assert metadata.sources.revision == self.rev;
         assert metadata.juliaManifest == builtins.hashFile "sha256" ./julia/Manifest.toml;
         import ./nix/depot.nix { inherit pkgs metadata; };
      mkApplication = { system }: platform.lib.mkApplication {
        inherit system;
        workspaceRoot = self.outPath;
      };
      mkSolver = { system, preparedDepot }: let
        pkgs = platform.inputs.nixpkgs.legacyPackages.${system};
      in import ./components/QCLNEGFRunner.jl/nix/package.nix {
        inherit pkgs preparedDepot;
        julia = import ./components/QCLNEGFRunner.jl/nix/julia.nix { inherit pkgs; };
        coreSrc = ./components/QCLNEGF.jl;
        runnerSrc = ./components/QCLNEGFRunner.jl;
        environmentSrc = ./julia;
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
