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
    if fig is None:
        return
    fig.clear()
    fig.patch.set_facecolor('none')

    # If no study data, show empty chart for all days
    if not study_data:
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        manual = [0] * 7
        timer = [0] * 7
    else:
        # Extract study data for each day
        days = list(study_data.keys())
        manual = []
        timer = []
        
        for d in days:
            try:
                day_data = study_data.get(d, {})
                manual_val = day_data.get("manual", 0)
                timer_val = day_data.get("timer", 0)
                # Convert values to float, default to 0 if missing
                manual.append(float(manual_val) if manual_val is not None else 0.0)
                timer.append(float(timer_val) if timer_val is not None else 0.0)
            except (ValueError, TypeError, AttributeError):
                manual.append(0.0)
                timer.append(0.0)
   
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    # Prepare x-axis positions and bar width
    x = np.arange(len(days))
    width = 0.6

    # Ensure no negative values for hours
    manual = [max(0, m) for m in manual]
    timer = [max(0, t) for t in timer]

    # Draw stacked bars for manual and timer hours
    ax.bar(x, manual, width, label='Manual', color='#87CEEB', linewidth=0)
    ax.bar(x, timer, width, bottom=manual, label='Timer', color='#FFA500', linewidth=0)

    # Format y-axis as hours:minutes
    time_formatter = FuncFormatter(lambda x, p: f"{int(x)}:{int((x % 1) * 60):02d}")
    ax.yaxis.set_major_formatter(time_formatter)

    # Set y-axis limits based on total hours
    total_hours = [m + t for m, t in zip(manual, timer)]
    max_val = max(total_hours) if any(total_hours) else 0
    ax.set_ylim(0, max(4, max_val * 1.1))

    # Set x-axis ticks and labels
    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.set_ylabel('Study Time (HH:MM)')

    # Add legend and grid for clarity
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Redraw canvas if available
    if fig.canvas:
        fig.canvas.draw_idle()