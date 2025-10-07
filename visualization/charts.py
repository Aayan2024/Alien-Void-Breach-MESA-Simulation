"""
charts.py - visualization charts for population counts.
"""
from mesa.visualization.modules import ChartModule

def population_chart():
    """
    Returns a ChartModule that plots Natives and Voidspawns population over time.
    """
    chart = ChartModule(
        [
            {"Label": "Natives", "Color": "#4CAF50"},
            {"Label": "Voidspawns", "Color": "#E53935"},
        ],
        data_collector_name="data_collector",
    )
    return chart
