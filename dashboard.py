"""Interactive Web Dashboard Generator for Sales Analytics.

Builds a self-contained, responsive HTML dashboard containing all 25
interactive Plotly visualizations, organized into categorized sections
with KPI cards, live search, and filter tabs.
"""
from __future__ import annotations

import argparse
import importlib
import os
from pathlib import Path
import sys
import webbrowser
import pandas as pd
import plotly.graph_objects as go

BASE_DIR = Path(__file__).resolve().parent
CHARTS_DIR = BASE_DIR / "charts"
DATA_PATH = BASE_DIR / "sales.csv" if (BASE_DIR / "sales.csv").exists() else BASE_DIR / "vendas.csv"
OUTPUT_HTML = BASE_DIR / "dashboard.html"

# Categorization mapping for the 25 charts
CHART_CATEGORIES = {
    # Trends & Overview
    "01": ("Overview & Trends", "Categorical aggregation of total gross sales by department."),
    "02": ("Overview & Trends", "Ranked horizontal breakdown of sales across all products."),
    "05": ("Overview & Trends", "Time-series trend showing monthly revenue evolution."),
    "06": ("Overview & Trends", "Area chart visualizing volume and monthly trends."),
    "22": ("Overview & Trends", "Progress gauge tracking annual sales performance against target."),

    # Segmentation & Categories
    "03": ("Segmentation", "Side-by-side comparison of customer segments per product category."),
    "04": ("Segmentation", "Stacked breakdown revealing segment proportions across categories."),
    "15": ("Segmentation", "Percentage market share distribution per category."),
    "16": ("Segmentation", "Donut chart displaying department revenue proportions."),
    "17": ("Segmentation", "Ranked funnel of product category sales volumes."),

    # Financials & Profitability
    "11": ("Financials & Profit", "Bivariate scatter plot analyzing correlation between sales and profit."),
    "12": ("Financials & Profit", "Multi-dimensional bubble chart with size proportional to units sold."),
    "13": ("Financials & Profit", "3D interactive scatter plot of Sales × Profit × Units."),
    "14": ("Financials & Profit", "2D contour density heatmap showing transaction concentration zones."),
    "20": ("Financials & Profit", "Stepwise waterfall showing net profit contribution up to total."),

    # Distributions & Statistics
    "07": ("Distributions & Stats", "Weekly financial OHLC (Open, High, Low, Close) candlestick metrics."),
    "08": ("Distributions & Stats", "Frequency distribution histogram of individual transaction values."),
    "09": ("Distributions & Stats", "Quartiles, median, and outlier detection across product categories."),
    "10": ("Distributions & Stats", "Kernel density estimation and probability curves per category."),
    "23": ("Distributions & Stats", "Multi-axis polar radar chart of customer satisfaction ratings."),

    # Geospatial, Hierarchy & Flows
    "18": ("Geospatial & Hierarchy", "Multi-tier nested rectangular treemap: Country > Category > Product."),
    "19": ("Geospatial & Hierarchy", "Concentric radial rings showing international product hierarchy."),
    "21": ("Geospatial & Hierarchy", "Cross-tabulation heatmap matrix of sales by Country and Category."),
    "24": ("Geospatial & Hierarchy", "Sankey flow diagram mapping revenue paths from Country to Category."),
    "25": ("Geospatial & Hierarchy", "Global choropleth world map visualising sales by country ISO-3 codes."),
}


def compute_kpis() -> dict[str, str]:
    """Calculate executive KPI summary metrics from sales dataset."""
    if not DATA_PATH.exists():
        return {
            "total_sales": "$0",
            "total_profit": "$0",
            "profit_margin": "0%",
            "transactions": "0",
            "avg_satisfaction": "0.0 / 5.0",
        }

    df = pd.read_csv(DATA_PATH)
    total_sales = df["vendas"].sum()
    total_profit = df["lucro"].sum()
    margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_sat = df["satisfacao"].mean()
    total_tx = len(df)

    return {
        "total_sales": f"${total_sales:,.2f}",
        "total_profit": f"${total_profit:,.2f}",
        "profit_margin": f"{margin:.1f}%",
        "transactions": f"{total_tx:,}",
        "avg_satisfaction": f"{avg_sat:.2f} / 5.0",
    }


def generate_chart_html(chart_file: Path) -> dict[str, str]:
    """Load a chart module, execute create_figure(), and extract HTML and metadata."""
    chart_id = chart_file.stem.split("_")[0]
    chart_title = " ".join(chart_file.stem.split("_")[1:]).title()
    category, description = CHART_CATEGORIES.get(chart_id, ("General", "Interactive data visualization."))

    module_name = f"charts.{chart_file.stem}"
    try:
        mod = importlib.import_module(module_name)
        fig: go.Figure = mod.create_figure(DATA_PATH)
        # Update layout to be responsive and fit card
        fig.update_layout(
            autosize=True,
            margin=dict(l=40, r=30, t=50, b=40),
            template="plotly_white",
        )
        plot_div = fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            config={"responsive": True, "displayModeBar": True},
        )
    except Exception as e:
        plot_div = f"<div class='error-box'>Failed to load {chart_file.name}: {e}</div>"

    return {
        "id": chart_id,
        "title": chart_title,
        "filename": chart_file.name,
        "category": category,
        "description": description,
        "html": plot_div,
    }


def build_dashboard_html() -> Path:
    """Build the standalone interactive HTML dashboard."""
    print("[INFO] Computing executive KPI metrics...")
    kpis = compute_kpis()

    chart_files = sorted(CHARTS_DIR.glob("*.py"))
    chart_files = [f for f in chart_files if f.name != "__init__.py"]

    print(f"[INFO] Rendering {len(chart_files)} interactive charts...")
    rendered_charts: list[dict[str, str]] = []
    for idx, cf in enumerate(chart_files, start=1):
        print(f"  [{idx:02d}/{len(chart_files):02d}] Processing {cf.name}...")
        rendered_charts.append(generate_chart_html(cf))

    categories = ["All"] + sorted(list({c["category"] for c in rendered_charts}))

    # Generate Chart Cards HTML
    cards_html = []
    for c in rendered_charts:
        card = f"""
        <div class="chart-card" data-category="{c['category']}" data-title="{c['title'].lower()}" data-id="{c['id']}">
            <div class="card-header">
                <div class="header-left">
                    <span class="badge">#{c['id']}</span>
                    <h3 class="chart-title">{c['title']}</h3>
                </div>
                <span class="cat-pill">{c['category']}</span>
            </div>
            <p class="chart-desc">{c['description']}</p>
            <div class="chart-container">
                {c['html']}
            </div>
            <div class="card-footer">
                <span class="file-tag">charts/{c['filename']}</span>
            </div>
        </div>
        """
        cards_html.append(card)

    cards_joined = "\n".join(cards_html)

    # Filter buttons HTML
    filter_btns = "\n".join([
        f'<button class="filter-btn {"active" if cat == "All" else ""}" data-filter="{cat}">{cat}</button>'
        for cat in categories
    ])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retail Analytics & Visualization Suite</title>
    <!-- Plotly.js Core CDN -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-body: #f8fafc;
            --bg-card: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --border: #e2e8f0;
            --badge-bg: #eff6ff;
            --badge-text: #1d4ed8;
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
            --shadow-hover: 0 10px 15px -3px rgb(0 0 0 / 0.08), 0 4px 6px -4px rgb(0 0 0 / 0.04);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.5;
            padding-bottom: 60px;
        }}

        /* Navbar & Header */
        header {{
            background: #ffffff;
            border-bottom: 1px solid var(--border);
            padding: 24px 32px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
        }}

        .header-content {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand h1 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .brand p {{
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: 2px;
        }}

        /* Container */
        .dashboard-container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 28px 32px;
        }}

        /* KPI Banner */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 32px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: var(--shadow);
            transition: transform 0.15s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
        }}

        .kpi-label {{
            font-size: 0.82rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
        }}

        .kpi-value {{
            font-size: 1.65rem;
            font-weight: 700;
            color: var(--text-main);
            margin-top: 6px;
        }}

        /* Controls: Search and Filters */
        .controls-panel {{
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-bottom: 28px;
            background: #ffffff;
            padding: 18px 24px;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }}

        .search-row {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .search-input {{
            flex: 1;
            padding: 10px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.15s ease;
        }}

        .search-input:focus {{
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .chart-count {{
            font-size: 0.88rem;
            color: var(--text-muted);
            white-space: nowrap;
        }}

        .filters-row {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .filter-btn {{
            background: #f1f5f9;
            border: 1px solid transparent;
            color: #475569;
            padding: 7px 16px;
            font-size: 0.85rem;
            font-weight: 500;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .filter-btn:hover {{
            background: #e2e8f0;
            color: #0f172a;
        }}

        .filter-btn.active {{
            background: var(--primary);
            color: #ffffff;
            font-weight: 600;
        }}

        /* Charts Grid */
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(680px, 1fr));
            gap: 24px;
        }}

        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            .dashboard-container, header {{
                padding: 16px;
            }}
        }}

        .chart-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 14px;
            box-shadow: var(--shadow);
            padding: 20px;
            display: flex;
            flex-direction: column;
            transition: box-shadow 0.2s ease, transform 0.2s ease;
        }}

        .chart-card:hover {{
            box-shadow: var(--shadow-hover);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .badge {{
            background: var(--badge-bg);
            color: var(--badge-text);
            font-weight: 700;
            font-size: 0.78rem;
            padding: 3px 8px;
            border-radius: 6px;
        }}

        .chart-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-main);
        }}

        .cat-pill {{
            font-size: 0.75rem;
            color: #64748b;
            background: #f1f5f9;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 500;
        }}

        .chart-desc {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 12px;
        }}

        .chart-container {{
            min-height: 420px;
            width: 100%;
            flex: 1;
        }}

        .card-footer {{
            margin-top: 12px;
            padding-top: 10px;
            border-top: 1px solid #f1f5f9;
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }}

        .file-tag {{
            font-family: monospace;
            font-size: 0.75rem;
            color: #94a3b8;
        }}

        .error-box {{
            background: #fef2f2;
            color: #dc2626;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #fecaca;
        }}

        .no-results {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px;
            color: var(--text-muted);
            font-size: 1.1rem;
            background: white;
            border-radius: 12px;
            border: 1px dashed var(--border);
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-content">
            <div class="brand">
                <h1>📊 Retail Analytics Visualization Dashboard</h1>
                <p>Complete interactive suite with 25 visualizations powered by Plotly & Pandas</p>
            </div>
        </div>
    </header>

    <main class="dashboard-container">

        <!-- KPI Metrics Overview -->
        <section class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Gross Sales</div>
                <div class="kpi-value">{kpis['total_sales']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Net Profit</div>
                <div class="kpi-value">{kpis['total_profit']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Profit Margin</div>
                <div class="kpi-value">{kpis['profit_margin']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Transactions</div>
                <div class="kpi-value">{kpis['transactions']}</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Satisfaction</div>
                <div class="kpi-value">{kpis['avg_satisfaction']}</div>
            </div>
        </section>

        <!-- Controls: Search & Category Filters -->
        <section class="controls-panel">
            <div class="search-row">
                <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search charts by title, category, or number (e.g. 'scatter', '08', 'map')...">
                <span id="chartCounter" class="chart-count">Showing 25 of 25 charts</span>
            </div>
            <div class="filters-row">
                {filter_btns}
            </div>
        </section>

        <!-- Charts Grid -->
        <section id="chartsGrid" class="charts-grid">
            {cards_joined}
        </section>

    </main>

    <script>
        // Interactive Category Filter & Live Search
        const searchInput = document.getElementById('searchInput');
        const filterBtns = document.querySelectorAll('.filter-btn');
        const cards = document.querySelectorAll('.chart-card');
        const counter = document.getElementById('chartCounter');
        let currentFilter = 'All';

        function filterCharts() {{
            const query = searchInput.value.trim().toLowerCase();
            let visibleCount = 0;

            cards.forEach(card => {{
                const cat = card.getAttribute('data-category');
                const title = card.getAttribute('data-title');
                const id = card.getAttribute('data-id');

                const matchesCat = (currentFilter === 'All' || cat === currentFilter);
                const matchesQuery = !query || title.includes(query) || id.includes(query) || cat.toLowerCase().includes(query);

                if (matchesCat && matchesQuery) {{
                    card.style.display = 'flex';
                    visibleCount++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            counter.textContent = `Showing ${{visibleCount}} of ${{cards.length}} charts`;
        }}

        filterBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.getAttribute('data-filter');
                filterCharts();
            }});
        }});

        searchInput.addEventListener('input', filterCharts);

        // Trigger resize event after load so Plotly graphs fit card dimensions cleanly
        window.addEventListener('load', () => {{
            setTimeout(() => {{
                window.dispatchEvent(new Event('resize'));
            }}, 300);
        }});
    </script>
</body>
</html>
"""
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"\n[SUCCESS] Dashboard generated at: {OUTPUT_HTML.resolve()}")
    return OUTPUT_HTML


def serve_dashboard(port: int = 8050) -> None:
    """Serve the dashboard locally using Python's http.server."""
    import http.server
    import socketserver

    os.chdir(BASE_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        url = f"http://localhost:{port}/dashboard.html"
        print(f"\n[INFO] Serving dashboard at: {url}")
        print("Press Ctrl+C to stop the server.")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and view the sales analytics web dashboard.",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Generate dashboard.html without opening in browser.",
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve the dashboard using a local HTTP server.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port for local HTTP server (default: 8050).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_path = build_dashboard_html()

    if args.serve:
        serve_dashboard(args.port)
    elif not args.build_only:
        print("[INFO] Opening dashboard in your default browser...")
        webbrowser.open(output_path.as_uri())


if __name__ == "__main__":
    main()
