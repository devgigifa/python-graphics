"""Funnel chart - Sales by category ordered in descending rank."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate funnel chart showing sales volume across categories."""
    df = pd.read_csv(data_path)
    data = (
        df.groupby("categoria", as_index=False)["vendas"]
        .sum()
        .sort_values("vendas", ascending=False)
    )

    fig = px.funnel(
        data,
        x="categoria",
        y="vendas",
        title="Sales Funnel by Category",
        labels={"categoria": "Category", "vendas": "Sales ($)"},
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
