"""Sunburst chart - Radial hierarchical breakdown: Country > Category."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate sunburst chart of sales across countries and categories."""
    df = pd.read_csv(data_path)

    fig = px.sunburst(
        df,
        path=["pais", "categoria"],
        values="vendas",
        color="vendas",
        color_continuous_scale="RdBu",
        title="Sales Hierarchy: Country > Category (Sunburst)",
        labels={
            "pais": "Country",
            "categoria": "Category",
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
