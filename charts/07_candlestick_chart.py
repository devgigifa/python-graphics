"""Candlestick chart - Weekly OHLC (Open, High, Low, Close) sales."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate weekly candlestick chart of sales from daily totals."""
    df = pd.read_csv(data_path)
    df["data"] = pd.to_datetime(df["data"])

    # Daily sales sum
    daily_sales = df.groupby("data")["vendas"].sum()

    # Aggregate by week: Open (first), High (max), Low (min), Close (last)
    ohlc = daily_sales.resample("W").agg(["first", "max", "min", "last"]).dropna()

    fig = go.Figure(
        go.Candlestick(
            x=ohlc.index,
            open=ohlc["first"],
            high=ohlc["max"],
            low=ohlc["min"],
            close=ohlc["last"],
            name="Weekly OHLC",
        )
    )
    fig.update_layout(
        title="Weekly Sales Performance (Candlestick)",
        xaxis_title="Week",
        yaxis_title="Sales ($)",
        xaxis_rangeslider_visible=False,
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
