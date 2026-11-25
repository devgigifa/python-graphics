"""Box plot - Sales distribution by product category (median, quartiles, outliers)."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate box plot of sales distribution across categories."""
    df = pd.read_csv(data_path)

    fig = px.box(
        df,
        x="categoria",
        y="vendas",
        color="categoria",
        title="Sales Distribution by Category (Box Plot)",
        labels={"categoria": "Category", "vendas": "Sales ($)"},
        points="outliers",
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
