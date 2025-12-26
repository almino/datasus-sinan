# Arquivos DBC do SINAM (DataSUS)

Processa os arquivos DBC em uma pasta,
descompactando-os para DBF
e criando notebooks Jupyter.

**Usage**:

```console
$ main [OPTIONS] [DIR]
```

**Arguments**:

* `[DIR]`: Pasta onde os arquivos DBC estão localizados  [default: (pasta atual)]

**Options**:

* `--rw-ipynb`: Sobrescreve os arquivos .ipynb (notebooks Jupyter)
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
