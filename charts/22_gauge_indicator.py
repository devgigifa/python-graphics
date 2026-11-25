"""Gauge indicator - Total sales achieved vs predefined annual sales target."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate gauge indicator comparing total sales to target."""
    df = pd.read_csv(data_path)

    total_sales = float(df["vendas"].sum())
    target = 3_000_000.0

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=total_sales,
            delta={"reference": target, "valueformat": "$,.0f"},
            number={"valueformat": "$,.0f"},
            gauge={
                "axis": {"range": [0, max(total_sales, target) * 1.25]},
                "bar": {"color": "#1f77b4"},
                "steps": [
                    {"range": [0, target * 0.7], "color": "#f0f2f6"},
                    {"range": [target * 0.7, target], "color": "#d9e2ec"},
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": target,
                },
            },
            title={"text": "Total Sales Achievement vs. Target ($3M)"},
        )
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
