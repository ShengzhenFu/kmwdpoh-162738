{ system ? "x86_64-linux", pkgs ? import ./nix { inherit system; } }:
let
  self = import ./. { inherit pkgs; };
in
{
  chaindImage =
    pkgs.dockerTools.buildLayeredImage {
      name = "crypto-org-chain/chain-maind";
      config.Entrypoint = [ "${self.chain-maind}/bin/chain-maind" ];
    };

  pystarportImage =
    pkgs.dockerTools.buildLayeredImage {
      name = "crypto-org-chain/chain-main-pystarport";
      config.Entrypoint = [ "${self.pystarport}/bin/pystarport" ];
    };
}
