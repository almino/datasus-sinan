import datasus_dbc
import typer
import glob
import os
from pathlib import Path
from typing import Annotated

app = typer.Typer()


@app.command()
def main(dir: Annotated[str, typer.Argument()] = ""):
    if len(dir) < 1:
        dir = Path(os.getcwd())
    else:
        dir = Path(dir)

    for dbc in glob.glob(str(dir / "*.dbc")):
        with open(dbc, "rb") as file:
            dbf_bytes = datasus_dbc.decompress_bytes(file.read())
            print(dbf_bytes)


if __name__ == "__main__":
    app()
