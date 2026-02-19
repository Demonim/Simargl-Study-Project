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
    fig = Figure(figsize=(8, 6), dpi=120, tight_layout=True)
    fig.patch.set_facecolor('none')
    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    if not subjects or not dates:
        ax.text(0.5, 0.5, 'No message data available', ha='center', va='center', color=color, transform=ax.transAxes)   
        ax.set_axis_off()
        return fig

    matrix_df = topics_week_matrix_df(subjects, dates)
    
    if matrix_df.empty or matrix_df.shape[0] == 0:
        ax.text(0.5, 0.5, 'No message data available', ha='center', va='center', color=color, transform=ax.transAxes)   
        ax.set_axis_off()
        return fig
    
    data = matrix_df.values  
   
    labels = []
    for tid in matrix_df.index:
        if tid in TOPICS:
            labels.append(TOPICS[tid]["label"])
        else:
            labels.append(str(tid))

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
    except Exception:
        pass

    weeks = ["4 weeks ago", "3 weeks ago", "2 weeks ago", "Last week", "Current week"]
    ax.set_xticks(np.arange(len(weeks)))
    ax.set_xticklabels(weeks, color=color, rotation=25, ha='right')
   
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, color=color)

    max_val = data.max() if data.size > 0 else 0
    for i in range(len(labels)):
        for j in range(min(len(weeks), data.shape[1] if len(data.shape) > 1 else 0)):
            try:
                val = int(data[i, j]) if len(data.shape) > 1 else 0
                txt_color = "white" if val > (max_val * 0.7) and val > 0 else "black"
                ax.text(j, i, val, ha="center", va="center", color=txt_color, fontsize=9)
            except (IndexError, ValueError):
                continue

    fig.suptitle("Topic Activity (Last 5 Weeks)",
                 fontsize=12, fontweight='bold', color=color)
   
    for spine in ax.spines.values():
        spine.set_edgecolor(color)

    return fig