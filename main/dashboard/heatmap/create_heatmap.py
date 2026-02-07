import numpy as np
from matplotlib.figure import Figure
from main.dashboard.heatmap.messages_logic import topics_week_matrix, topic_labels

def create_heatmap(subjects, dates):

    matrix_dict = topics_week_matrix(subjects, dates)
    labels = topic_labels()
    
    topic_ids = list(matrix_dict.keys())
    data = np.array([matrix_dict[tid] for tid in topic_ids])
    
    fig = Figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    
    im = ax.imshow(data, cmap='YlGn')
    
    fig.colorbar(im, ax=ax, label='Message Count')
    
    weeks = ["4 weeks ago", "3 weeks ago", "2 weeks ago", "Last week", "Current week"]
    
    ax.set_xticks(np.arange(len(weeks)))
    ax.set_xticklabels(weeks)
    
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels)
    
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_horizontalalignment('right')
    
    for i in range(len(labels)):
        for j in range(len(weeks)):

            max_val = data.max() if data.max() > 0 else 1
            color = "black" if data[i, j] < max_val / 2 else "white"
            ax.text(j, i, int(data[i, j]),
                    ha="center", va="center", color=color)

    fig.suptitle("Topic Activity Heatmap (Last 5 Weeks)", fontsize=12, fontweight='bold')
    
    fig.subplots_adjust(bottom=0.2) 
    
    return fig