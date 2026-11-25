"""3D Scatter plot - Visualizing sales, profit, and quantity simultaneously."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate 3D scatter plot of sales, profit, and quantity."""
    df = pd.read_csv(data_path)

    fig = px.scatter_3d(
        df,
        x="vendas",
        y="lucro",
        z="quantidade",
        color="categoria",
        hover_data=["produto", "pais"],
        title="3D Scatter: Sales vs. Profit vs. Quantity",
        labels={
            "vendas": "Sales ($)",
            "lucro": "Profit ($)",
            "quantidade": "Quantity",
            "categoria": "Category",
        },
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
