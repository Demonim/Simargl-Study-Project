import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

def create_stacked_bar(study_data):
    fig = Figure(figsize=(8, 6), dpi=100)
    update_stacked_bar(fig, study_data)
    return fig

def update_stacked_bar(fig, study_data):
    fig.clear()
    fig.patch.set_facecolor('none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')
    days = list(study_data.keys())
    manual = [study_data[d]["manual"] for d in days]
    timer = [study_data[d]["timer"] for d in days]
    
    x = np.arange(len(days))
    width = 0.6

    ax.bar(x, manual, width, label='Manual', color='#87CEEB', linewidth=0)
    ax.bar(x, timer, width, bottom=manual, label='Timer', color='#FFA500', linewidth=0)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"{int(x)}:{int((x % 1) * 60):02d}"))

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

def show_chart(fig, title="Tracker"):
    new_manager = plt.figure().canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
    new_manager.set_window_title(title)
    plt.show()