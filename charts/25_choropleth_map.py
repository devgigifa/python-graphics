"""Choropleth Map - Global geographical distribution of sales by country."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_PATH = Path(__file__).resolve().parent.parent / "sales.csv"


def create_figure(data_path: Path = DATA_PATH) -> go.Figure:
    """Generate choropleth world map of sales by country."""
    df = pd.read_csv(data_path)
    data = df.groupby(["pais", "iso_alpha"], as_index=False)["vendas"].sum()

    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="vendas",
        hover_name="pais",
        color_continuous_scale="Viridis",
        title="Global Sales Distribution by Country",
        labels={"vendas": "Sales ($)", "iso_alpha": "Country ISO Code"},
    )
    fig.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth")
    )
    return fig


def main() -> None:
    """Display the chart in the default browser."""
    fig = create_figure()
    fig.show()


if __name__ == "__main__":
    main()
