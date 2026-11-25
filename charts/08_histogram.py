"""Histogram - Frequency distribution of sales transaction amounts."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate histogram showing distribution of sales values.

    Note: Fixed original bug where 'x' was mapped to 'categoria' instead of 'vendas'.
    """
    df = pd.read_csv(data_path)

    fig = px.histogram(
        df,
        x="vendas",
        nbins=40,
        title="Distribution of Sales Transaction Amounts",
        labels={"vendas": "Sales Amount ($)", "count": "Transaction Count"},
        marginal="box",  # adds an informative box plot on top
        color="categoria",
    )
    fig.update_layout(
        xaxis_title="Sales Amount ($)",
        yaxis_title="Count of Transactions",
        bargap=0.05,
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
