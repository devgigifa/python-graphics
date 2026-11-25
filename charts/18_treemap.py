"""Treemap - Hierarchical rectangular visualization: Country > Category > Product."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate treemap of sales aggregated hierarchically."""
    df = pd.read_csv(data_path)

    # path specifies the hierarchy levels: Country -> Category -> Product
    fig = px.treemap(
        df,
        path=["pais", "categoria", "produto"],
        values="vendas",
        color="vendas",
        color_continuous_scale="Blues",
        title="Sales Hierarchy: Country > Category > Product (Treemap)",
        labels={
            "pais": "Country",
            "categoria": "Category",
            "produto": "Product",
            "vendas": "Sales ($)",
        },
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
