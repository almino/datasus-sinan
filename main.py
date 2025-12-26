from pathlib import Path
from rich.console import Console
from typing import Annotated
import datasus_dbc
import glob
import nbformat as nbf
import os
import typer

app = typer.Typer(help="Descompacta arquivos DBC do DATASUS e cria notebooks Jupyter.")
konsole = Console()


def picle_pandas(file: Path):
    """
    Cria um arquivo pickle com o conteúdo do DBC para DataFrames do Pandas.
    """
    from dbfread import DBF
    from pandas import DataFrame

    target_pickle = file.with_suffix(".pkl")

    if target_pickle.exists():
        konsole.print(f"Ignorando criação do arquivo pickle para {file.name}…")
        return target_pickle

    # https://stackoverflow.com/a/46000253/437459
    dbf = DBF(file, encoding="cp1252")
    konsole.print(f"Lendo DBF {file.name} em um DataFrame do Pandas…")
    # https://dbfread.readthedocs.io/en/latest/exporting_data.html#pandas-data-frames
    frame = DataFrame(iter(dbf))

    konsole.print(f"Salvando DataFrame em {target_pickle.name}…")
    # https://stackoverflow.com/a/17098736/437459
    frame.to_pickle(target_pickle)
    return target_pickle


@app.command()
def main(
    dir: Annotated[
        str,
        typer.Argument(
            help="Pasta onde os arquivos DBC estão localizados",
            show_default="pasta atual",
        ),
    ] = "",
    rw_ipynb: Annotated[
        bool,
        typer.Option(
            "--rw-ipynb",
            help="Sobrescreve os arquivos .ipynb (notebooks Jupyter)",
        ),
    ] = False,
):
    """
    Processa os arquivos DBC em uma pasta,
    descompactando-os para DBF
    e criando notebooks Jupyter.

    :param dir: Pasta onde os arquivos DBC estão localizados
    :type dir: str
    :param rw_ipynb: Recria notebooks Jupyter para leitura dos arquivos DBC
    :type rw_ipynb: bool
    """
    if len(dir) < 1:
        dir = Path(os.getcwd())
    else:
        dir = Path(dir)

    for file in glob.glob(str(dir / "*.dbc")):
        pathable = Path(file)
        target_dbf = pathable.with_suffix(".dbf")

        if target_dbf.exists():
            konsole.print(f"Ignorando {pathable.name}, arquivo DBF já existe.")
            continue

        konsole.print(f"Descompactando {pathable.name}…")
        konsole.print(f"Arquivo: {target_dbf}")
        datasus_dbc.decompress(file, str(target_dbf))

    for file in glob.glob(str(dir / "*.dbf")):
        pathable = Path(file)
        target_ipynb = pathable.with_suffix(".ipynb")
        ipynb_dbf = target_dbf.relative_to(target_ipynb.parent)

        if target_ipynb.exists() and not rw_ipynb:
            konsole.print(f"Ignorando {pathable.name}, arquivo .ipynb já existe.")
            continue

        # https://stackoverflow.com/a/45672031/437459
        nb = nbf.v4.new_notebook()
        text = f"# Arquivo {pathable.name}.dbc descompactado"

        pickle_pandas = picle_pandas(pathable).relative_to(target_ipynb.parent)

        pre_code = f"""\"\"\"
            Carrega o conteúdo do arquivo DBC em um DataFrame do Pandas.
            \"\"\"

            import pandas

            frame = pandas.read_pickle(r"{pickle_pandas}")

            frame
        """

        code = []

        for l in pre_code.splitlines():
            l = l.rstrip()
            code.append(l[12:] if l.startswith(" " * 12) else l)

        nb["cells"] = [
            nbf.v4.new_markdown_cell(text),
            nbf.v4.new_code_cell(code),
        ]

        konsole.print(f"Criando Python Notebook para {pathable.name}…")
        konsole.print(f"Arquivo: {target_ipynb}")

        with open(target_ipynb, "w") as f:
            nbf.write(nb, f)


if __name__ == "__main__":
    app()
