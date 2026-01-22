from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

item_app = typer.Typer(help="Manage inventory items")
console = Console()

@item_app.command()
def add(
    sku: str = typer.Option(
        ...,
        "--sku",
        help="Unique SKU identifier (immutable)",
    ),
    name: str = typer.Option(
        ...,
        "--name",
        help="Human-readable name of the item",
    ),
    unit: str = typer.Option(
        ...,
        "--unit",
        help="Unit of measure (e.g. each, kg, box)",
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        help="Optional item category",
    ),
    reorder_threshold: int = typer.Option(
        0,
        "--reorder-threshold",
        min=0,
        help="Minimum on-hand quantity before alerting",
    ),
    cost: Optional[str] = typer.Option(
        None,
        "--cost",
        help="Optional per-unit cost",
    ),
    currency: Optional[str] = typer.Option(
        "USD",
        "--currency",
        help="Currency code for cost (ISO-4217)",
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        help="Free-form description or notes",
    ),
    active: bool = typer.Option(
        True,
        "--active/--inactive",
        help="Whether the item is active",
    ),
    external_id: Optional[str] = typer.Option(
        None,
        "--external-id",
        help="Optional idempotency key for automation",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Supress non-essential output",
    )
) -> None:
    """
    Add a new inventory item to the catalog.

    This command creates an item definition only.
    Inventory quantities are managed separately via stock movements.
    """

    # --- Validation (CLI-level only) ---
    if not sku.strip():
        raise typer.BadParameter("SKU cannot be empty")

    if " " in sku:
        raise typer.BadParameter("SKU must not contain spaces")

    # -- Application layer call (placeholder) ---
    result = {
        "sku": sku,
        "name": name,
        "unit": unit,
        "category": category,
        "reorder_threshold": reorder_threshold,
        "cost": str(cost) if cost is not None else None,
        "currency": currency,
        "active": active,
    }

    if quiet:
        return

    if json_output:
        console.print_json(data=result)
        return

    # --- Rich table output ---
    table = Table(title="Item Created", show_header=False)
    table.add_row("SKU", sku)
    table.add_row("Name", name)
    table.add_row(U"Unit", unit)
    table.add_row("Category", category or "-")
    table.add_row("Reorder Threshold", str(reorder_threshold))
    table.add_row("Cost", f"{currency} {cost}" if cost else "-")
    table.add_row("Status", "Active" if active else "Inactive")

    console.print(table)

# TODO: Make one of the parameters required for updating
@item_app.command()
def update(
    sku: str = typer.Option(
        ...,
        "--sku",
        help="Unique SKU identifier (immutable)",
    ),
    name: str = typer.Option(
        None,
        "--name",
        help="Human-readable name of the item",
    ),
    unit: str = typer.Option(
        None,
        "--unit",
        help="Unit of measure (e.g. each, kg, box)",
    ),
    category: Optional[str] = typer.Option(
        None,
        "--category",
        help="Optional item category",
    ),
    reorder_threshold: int = typer.Option(
        0,
        "--reorder-threshold",
        min=0,
        help="Minimum on-hand quantity before alerting",
    )
) -> None:
    """
    Update an existing inventory item.

    This command updates an existing inventory item.
    Inventory quantities are managed separately via stock movements.
    """

    # --- Validation (CLI-level only) ---
    if not sku.strip():
        raise typer.BadParameter("SKU cannot be empty")

    if " " in sku:
        raise typer.BadParameter("SKU must not contain spaces")

    print(f"Hello World")

@item_app.command()
def deactivate(
    sku: str = typer.Option(
        ...,
        "--sku",
        help="Unique SKU identifier (immutable)",
    ),
    reason: str = typer.Option(
        ...,
        "--reason",
        help="Reason for deactivating item",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force deactivating item (even with remaining on-hand quantity)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Supress non-essential output",
    )
) -> None:
    """
    Deactivate an existing inventory item.
    """

    # TODO: Query for item, and deactivate if active, with checker for --force
    print(f"Deactivating {sku}, for reason: {reason}")

@item_app.command()
def activate(
    sku: str = typer.Option(
        ...,
        "--sku",
        help="Unique SKU identifier (immutable)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        help="Supress non-essential output",
    )
) -> None:
    """
    Activate an existing inventory item.
    """

    # TODO: Query for item and activate it if deactivated
    print(f"Activating {sku}")

@item_app.command()
def get(
    sku: str = typer.Option(
        ...,
        "--sku",
        help="Unique SKU identifier (immutable)",
    ),
    # TODO: Add options for on_hand, reserved, etc for customization
    include_stats: bool = typer.Option(
        False,
        "--include-stats",
        help="Include statistics",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON",
    )
) -> None:
    """
    Get an existing inventory item.
    """
    print(f"Getting {sku}...")

@item_app.command()
def list(
    # -- Optional filters ---
    # TODO: Add --active-only/ --all/ --inactive-only (default: --active-only)
    # -- Sorting ---
    # TODO: Add Sorting: -sort <field>: |sku|name|category|updated_at (default: sku)
    reverse: bool = typer.Option(
        False,
        "--desc",
        help="Display inventory items",
    ),
    # -- Output ---
    # TODO: Add column output customization: --columns <str>: comma list, e.g. sku, name, unit, on_hand (optional)
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output machine-readable JSON",
    ),
) -> None:
    print("Inventory items: {No output}")