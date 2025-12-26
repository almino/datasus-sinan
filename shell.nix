{ pkgs ? import <nixos-unstable> { }, ... }:

let
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    # beautifulsoup4
    black
    dbfread
    nbformat
    pip
    pyarrow
    pylance
    # regex
    virtualenv
    werkzeug # webserver
  ]);
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3Packages.virtualenv # run virtualenv .
    python3Packages.pip
    rustup
  ] ++ [ pythonEnv ];
  packages = with pkgs; [
    pythonEnv
    rustup
    sqlitebrowser
    uv
  ];
  shellHook = ''
    if [ ! -d .venv ]; then
      virtualenv -p ${pythonEnv}/bin/python .venv
    fi
    uv sync --active --no-install-project --managed-python --quiet --python .venv/bin/python
  '';
}
