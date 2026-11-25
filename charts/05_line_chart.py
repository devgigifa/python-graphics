"""Line chart - Monthly sales trend over time."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate line chart of monthly sales over time."""
    df = pd.read_csv(data_path)
    df["data"] = pd.to_datetime(df["data"])
    df["month"] = df["data"].dt.to_period("M").dt.to_timestamp()

    data = df.groupby("month", as_index=False)["vendas"].sum()

    fig = px.line(
        data,
        x="month",
        y="vendas",
        markers=True,
        title="Monthly Sales Trend",
        labels={"month": "Month", "vendas": "Sales ($)"},
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
