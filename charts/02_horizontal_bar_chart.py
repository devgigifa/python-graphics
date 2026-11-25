"""Horizontal bar chart - Total sales by product."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate horizontal bar chart of total sales by product."""
    df = pd.read_csv(data_path)
    data = (
        df.groupby("produto", as_index=False)["vendas"]
        .sum()
        .sort_values("vendas", ascending=True)
    )

    fig = px.bar(
        data,
        x="vendas",
        y="produto",
        orientation="h",
        title="Total Sales by Product",
        labels={"produto": "Product", "vendas": "Sales ($)"},
        text_auto=".2s",
    )
    fig.update_layout(xaxis_title="Total Sales ($)", yaxis_title="Product")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
