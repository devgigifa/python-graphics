"""Waterfall chart - Stepwise profit contribution by product category leading to total."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate waterfall chart for profit contribution per category."""
    df = pd.read_csv(data_path)
    data = df.groupby("categoria", as_index=False)["lucro"].sum()

    categories = list(data["categoria"]) + ["Total"]
    profits = list(data["lucro"]) + [data["lucro"].sum()]
    measures = ["relative"] * len(data) + ["total"]

    fig = go.Figure(
        go.Waterfall(
            name="Profit Contribution",
            orientation="v",
            measure=measures,
            x=categories,
            y=profits,
            textposition="outside",
            text=[f"${v:,.0f}" for v in profits],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        )
    )
    fig.update_layout(
        title="Profit Contribution by Category (Waterfall)",
        xaxis_title="Category",
        yaxis_title="Profit ($)",
        waterfallgap=0.3,
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
