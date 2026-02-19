import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter

def create_stacked_bar(study_data):
    """
    Initializes a Matplotlib Figure and renders a stacked bar chart.

    Args:
        study_data (dict): A dictionary where keys are day labels (str) and
                           values are dicts with 'manual' and 'timer' hours (float).

    Returns:
        Figure: A Matplotlib Figure object containing the initial chart.
    """
    fig = Figure(figsize=(8, 6), dpi=100)
    update_stacked_bar(fig, study_data)
    return fig

def update_stacked_bar(fig, study_data):
    """
    Clears the existing figure and redraws the stacked bar chart with new data.

    This function handles the visualization logic, including axis formatting,
    limit scaling, and legend placement.

    Args:
        fig (Figure): The existing Matplotlib Figure object to be updated.
        study_data (dict): Updated dictionary containing study hours per day.
    """
    fig.clear()
    fig.patch.set_facecolor('none')

    if not study_data:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        manual = [0] * 7
        timer = [0] * 7
    else:
        days = list(study_data.keys())
        manual = [study_data[d].get("manual", 0) for d in days]
        timer = [study_data[d].get("timer", 0) for d in days]
   
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')
   
    x = np.arange(len(days))
    width = 0.6

    ax.bar(x, manual, width, label='Manual', color='#87CEEB', linewidth=0)
    ax.bar(x, timer, width, bottom=manual, label='Timer', color='#FFA500', linewidth=0)

    time_formatter = FuncFormatter(lambda x, p: f"{int(x)}:{int((x % 1) * 60):02d}")
    ax.yaxis.set_major_formatter(time_formatter)
   
    total_hours = [m + t for m, t in zip(manual, timer)]
    max_val = max(total_hours) if any(total_hours) else 0
    ax.set_ylim(0, max(4, max_val * 1.1))

    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.set_ylabel('Study Time (HH:MM)')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
   
    if fig.canvas:
        fig.canvas.draw_idle()