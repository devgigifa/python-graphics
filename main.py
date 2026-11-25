"""Main CLI runner for interactive sales data visualizations.

Allows running any of the 25 Plotly charts individually, by number,
or via an interactive terminal menu.
"""
from __future__ import annotations

import argparse
import importlib
from pathlib import Path
import sys

CHARTS_DIR = Path(__file__).resolve().parent / "charts"


def get_available_charts() -> list[tuple[str, str, Path]]:
    """Return a sorted list of (id, title, file_path) for all charts."""
    charts: list[tuple[str, str, Path]] = []
    for file in sorted(CHARTS_DIR.glob("*.py")):
        if file.name == "__init__.py":
            continue
        # Extract number prefix e.g. "01"
        chart_id = file.stem.split("_")[0]
        # Readable title from filename
        title = " ".join(file.stem.split("_")[1:]).title()
        charts.append((chart_id, title, file))
    return charts


def run_chart(chart_path: Path) -> None:
    """Import and execute the create_figure and show methods of a chart module."""
    module_name = f"charts.{chart_path.stem}"
    print(f"\n[INFO] Loading chart from '{chart_path.name}'...")
    try:
        mod = importlib.import_module(module_name)
        if hasattr(mod, "main"):
            mod.main()
        elif hasattr(mod, "create_figure"):
            fig = mod.create_figure()
            fig.show()
        else:
            print(f"[ERROR] Module {module_name} has no runnable entry point.", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] Failed to render chart {chart_path.name}: {e}", file=sys.stderr)
        raise


def list_charts() -> None:
    """Print a clean numbered list of all available charts."""
    print("\nAvailable Visualizations:")
    print("=" * 60)
    print("  [00] Launch Interactive Web Dashboard     (dashboard.py)")
    for chart_id, title, file in get_available_charts():
        print(f"  [{chart_id}] {title:<35} ({file.name})")
    print("=" * 60)


def interactive_menu() -> None:
    """Display interactive menu prompting user for chart selection."""
    charts = get_available_charts()
    list_charts()
    print("\nEnter a chart number (e.g. 00 for web dashboard, 01, 15), 'all', or 'q' to quit:")
    while True:
        choice = input(">> ").strip().lower()
        if choice in ("q", "quit", "exit"):
            print("Exiting.")
            break
        if choice in ("00", "0", "dashboard", "web"):
            import dashboard
            dashboard.main()
            break
        if choice == "all":
            confirm = input("This will open 25 browser tabs. Are you sure? (y/N): ").strip().lower()
            if confirm in ("y", "yes"):
                for _, _, path in charts:
                    run_chart(path)
            break

        matching = [c for c in charts if c[0] == choice.zfill(2) or c[0] == choice]
        if matching:
            run_chart(matching[0][2])
            break
        print(f"Invalid option '{choice}'. Please enter a valid number (00-25) or 'q' to quit.")


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Run Plotly sales visualization charts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Open interactive menu
  python main.py --dashboard        # Open unified web dashboard
  python main.py --list             # List all available charts
  python main.py --chart 01         # Run chart 01 (Bar Chart)
  python main.py --chart 08         # Run chart 08 (Histogram)
  python main.py --chart bar        # Run by partial name match
        """,
    )
    parser.add_argument(
        "-d", "--dashboard",
        action="store_true",
        help="Build and open the interactive web dashboard with all 25 charts",
    )
    parser.add_argument(
        "-c", "--chart",
        type=str,
        help="Chart number (e.g. 01, 7, 25) or name substring to run",
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available charts and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    charts = get_available_charts()

    if args.dashboard:
        import dashboard
        dashboard.main()
        return

    if args.list:
        list_charts()
        return

    if args.chart:
        target = args.chart.strip().lower()
        # Try match by number first (e.g. "1" or "01")
        target_num = target.zfill(2) if target.isdigit() else ""
        matched = [
            c for c in charts
            if c[0] == target_num or target in c[2].stem.lower()
        ]

        if not matched:
            print(f"[ERROR] No chart matching '{args.chart}'. Run 'python main.py --list' to see options.", file=sys.stderr)
            sys.exit(1)

        run_chart(matched[0][2])
        return

    interactive_menu()


if __name__ == "__main__":
    main()
