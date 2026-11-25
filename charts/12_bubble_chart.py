"""Bubble chart - Sales vs profit with bubble size representing transaction quantity."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate bubble chart: sales vs profit (bubble size = quantity)."""
    df = pd.read_csv(data_path)

    fig = px.scatter(
        df,
        x="vendas",
        y="lucro",
        size="quantidade",
        color="categoria",
        hover_data=["produto", "pais"],
        title="Sales vs. Profit (Bubble Size = Units Sold)",
        labels={
            "vendas": "Sales ($)",
            "lucro": "Profit ($)",
            "quantidade": "Quantity Sold",
            "categoria": "Category",
        },
    )
    fig.update_layout(xaxis_title="Sales ($)", yaxis_title="Profit ($)")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
