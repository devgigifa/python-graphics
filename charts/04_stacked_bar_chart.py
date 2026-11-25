"""Stacked bar chart - Sales by category stacked by customer segment."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate stacked bar chart of sales by category and segment."""
    df = pd.read_csv(data_path)
    data = df.groupby(["categoria", "segmento"], as_index=False)["vendas"].sum()

    fig = px.bar(
        data,
        x="categoria",
        y="vendas",
        color="segmento",
        barmode="stack",
        title="Sales by Category and Segment (Stacked)",
        labels={
            "categoria": "Category",
            "segmento": "Segment",
            "vendas": "Sales ($)",
        },
    )
    fig.update_layout(xaxis_title="Category", yaxis_title="Total Sales ($)")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
