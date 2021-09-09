{ pkgs }: {
  deps = [
    pkgs.cowsay
    pkgs.Python39
    pkgs.Python39Packages.pip
    pkgs.Python39Packages.setuptools
    pkgs.Python39Packages.wheel
  ];
}
