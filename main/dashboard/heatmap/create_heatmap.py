import numpy as np
from matplotlib.figure import Figure
from .messages_logic import topics_week_matrix_df, TOPICS


def create_heatmap(subjects, dates, color='black'):
    """
    Generates a heatmap visualization of message activity trends.
    
    Args:
        subjects (list): List of message subject strings to analyze.
        dates (list): List of corresponding message timestamps.
        color (str): Theme-compliant color for text, ticks, and spine elements.
        
    Returns:
        Figure: Matplotlib Figure object containing the rendered heatmap.
    """

    matrix_df = topics_week_matrix_df(subjects, dates)
    data = matrix_df.values  
   
    labels = [TOPICS[tid]["label"] for tid in matrix_df.index]

    fig = Figure(figsize=(8, 6), dpi=120, tight_layout=True)
    fig.patch.set_facecolor('none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    if data.sum() == 0:
        ax.text(0.5, 0.5, 'No message data available', ha='center', va='center', color=color, transform=ax.transAxes)   
        ax.set_axis_off()
        return fig

    im = ax.imshow(data, cmap='YlGn', aspect='auto')

    try:
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Messages', color=color)
        cbar.outline.set_edgecolor(color)
        cbar.ax.yaxis.set_tick_params(color=color, labelcolor=color)
    except Exception as e:
        print("Error:", e)

    weeks = ["4 weeks ago", "3 weeks ago", "2 weeks ago", "Last week", "Current week"]
    ax.set_xticks(np.arange(len(weeks)))
    ax.set_xticklabels(weeks, color=color, rotation=25, ha='right')
   
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, color=color)

    max_val = data.max()
    for i in range(len(labels)):
        for j in range(len(weeks)):
            val = int(data[i, j]) 
            txt_color = "white" if val > (max_val * 0.7) and val > 0 else "black"
            ax.text(j, i, val, ha="center", va="center", color=txt_color, fontsize=9)

    fig.suptitle("Topic Activity (Last 5 Weeks)",
                 fontsize=12, fontweight='bold', color=color)
   
    for spine in ax.spines.values():
        spine.set_edgecolor(color)

    return fig