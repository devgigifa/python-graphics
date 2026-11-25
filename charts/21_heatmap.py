"""Heatmap - 2D matrix of total sales by country across product categories."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate heatmap matrix: Country vs Category."""
    df = pd.read_csv(data_path)

    table = df.pivot_table(
        index="pais",
        columns="categoria",
        values="vendas",
        aggfunc="sum",
        fill_value=0,
    )

    fig = px.imshow(
        table,
        text_auto=".2s",
        aspect="auto",
        color_continuous_scale="Viridis",
        title="Sales Matrix: Country vs. Product Category",
        labels={"x": "Category", "y": "Country", "color": "Sales ($)"},
    )
    fig.update_layout(xaxis_title="Category", yaxis_title="Country")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
