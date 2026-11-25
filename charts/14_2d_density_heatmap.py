"""2D Density Heatmap - Density contour of sales vs profit concentration."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate 2D density heatmap showing where sales and profit concentrate."""
    df = pd.read_csv(data_path)

    fig = px.density_heatmap(
        df,
        x="vendas",
        y="lucro",
        nbinsx=30,
        nbinsy=30,
        marginal_x="histogram",
        marginal_y="histogram",
        title="2D Density Heatmap: Sales vs. Profit Concentration",
        labels={"vendas": "Sales ($)", "lucro": "Profit ($)"},
    )
    fig.update_layout(xaxis_title="Sales ($)", yaxis_title="Profit ($)")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
