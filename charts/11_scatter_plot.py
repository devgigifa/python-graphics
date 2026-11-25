"""Scatter plot - Relationship between sales amount and profit."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate scatter plot of sales vs profit."""
    df = pd.read_csv(data_path)

    fig = px.scatter(
        df,
        x="vendas",
        y="lucro",
        color="categoria",
        hover_data=["produto", "segmento", "pais"],
        title="Relationship Between Sales and Profit",
        labels={
            "vendas": "Sales ($)",
            "lucro": "Profit ($)",
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
