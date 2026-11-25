"""Polar/Radar chart - Average customer satisfaction score by product category."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate polar/radar chart of mean customer satisfaction per category."""
    df = pd.read_csv(data_path)
    data = df.groupby("categoria", as_index=False)["satisfacao"].mean()

    fig = px.line_polar(
        data,
        r="satisfacao",
        theta="categoria",
        line_close=True,
        range_r=[0, 5],
        title="Average Customer Satisfaction Score by Category (1-5 Scale)",
        labels={"satisfacao": "Satisfaction Score", "categoria": "Category"},
    )
    fig.update_traces(fill="toself")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
