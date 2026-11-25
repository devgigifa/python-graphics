"""Sankey diagram - Sales flow from countries to product categories."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate Sankey diagram displaying sales value flow: Country -> Category."""
    df = pd.read_csv(data_path)
    flow = df.groupby(["pais", "categoria"], as_index=False)["vendas"].sum()

    # List of unique node names (countries first, then categories)
    labels = list(flow["pais"].unique()) + list(flow["categoria"].unique())
    label_to_index = {label: i for i, label in enumerate(labels)}

    fig = go.Figure(
        go.Sankey(
            node={
                "pad": 15,
                "thickness": 20,
                "line": {"color": "black", "width": 0.5},
                "label": labels,
            },
            link={
                "source": flow["pais"].map(label_to_index),
                "target": flow["categoria"].map(label_to_index),
                "value": flow["vendas"],
            },
        )
    )
    fig.update_layout(
        title="Sales Volume Flow: Country to Product Category",
        font_size=11,
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
