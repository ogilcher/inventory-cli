from inv.core.config import Settings

import typer
import inv.cli.item_cmd as item_cmd

app = typer.Typer()
app.add_typer(item_cmd.item_app, name="item")

def run():
    settings = Settings.load()

    app()