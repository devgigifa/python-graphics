"""Violin plot - Sales probability density distribution by product category."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate violin plot of sales distribution across categories."""
    df = pd.read_csv(data_path)

    fig = px.violin(
        df,
        x="categoria",
        y="vendas",
        color="categoria",
        box=True,  # displays inner box plot inside each violin
        points="all",  # displays all observation points
        title="Sales Distribution by Category (Violin Plot)",
        labels={"categoria": "Category", "vendas": "Sales ($)"},
    )
    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales ($)",
        showlegend=False,
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
