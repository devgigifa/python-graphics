"""Pie chart - Proportion of total sales by product category."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate pie chart showing sales share by category."""
    df = pd.read_csv(data_path)
    data = df.groupby("categoria", as_index=False)["vendas"].sum()

    fig = px.pie(
        data,
        values="vendas",
        names="categoria",
        title="Market Share: Total Sales by Category",
        labels={"categoria": "Category", "vendas": "Sales ($)"},
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
