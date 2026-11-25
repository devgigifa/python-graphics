"""Donut chart - Proportion of total sales by product category with a hollow center."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate donut chart of sales share by category."""
    df = pd.read_csv(data_path)
    data = df.groupby("categoria", as_index=False)["vendas"].sum()

    # hole=0.5 turns the standard pie chart into a donut chart
    fig = px.pie(
        data,
        values="vendas",
        names="categoria",
        hole=0.5,
        title="Sales Distribution by Category (Donut Chart)",
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
