import numpy as np
from matplotlib.figure import Figure
from .messages_logic import topics_week_matrix, topic_labels


def create_heatmap(subjects, dates, color='black'):
    matrix_dict = topics_week_matrix(subjects, dates)
    labels = topic_labels()

    topic_ids = list(matrix_dict.keys())
    data = np.array([matrix_dict[tid] for tid in topic_ids])

    fig = Figure(figsize=(8, 6), dpi=120)
    fig.patch.set_facecolor('none')

    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    im = ax.imshow(data, cmap='YlGn')

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label('Message Count', color=color)
    cbar.ax.yaxis.set_tick_params(color=color, labelcolor=color)
    cbar.outline.set_edgecolor(color)

    weeks = ["4 weeks ago", "3 weeks ago", "2 weeks ago", "Last week", "Current week"]

    ax.set_xticks(np.arange(len(weeks)))
    ax.set_xticklabels(weeks, color=color)

    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, color=color)


    for label in ax.get_xticklabels():
        label.set_rotation(25)
        label.set_horizontalalignment('right')

    for i in range(len(labels)):
        for j in range(len(weeks)):
            max_val = data.max() if data.max() > 0 else 1

            inner_color = "black" if data[i, j] < max_val / 2 else "white"
            ax.text(j, i, int(data[i, j]),
                    ha="center", va="center", color=inner_color)

    fig.suptitle("Topic Activity Heatmap (Last 5 Weeks)",
                 fontsize=10, fontweight='bold', color=color)

    fig.subplots_adjust(bottom=0.2)

    for spine in ax.spines.values():
        spine.set_edgecolor(color)

    return fig