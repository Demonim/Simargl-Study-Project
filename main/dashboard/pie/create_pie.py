from main.dashboard.pie.pie_val_lab import pie_values_labels
from matplotlib.figure import Figure

def create_pie(subject_hours):
    fig = Figure(figsize=(8, 6), tight_layout=True)
    ax = fig.add_subplot(111)

    values, labels = pie_values_labels(subject_hours)

    wedges, texts, autotexts = ax.pie(
        values, 
        labels=None, 
        autopct='%1.1f%%', 
        startangle=90, 
        pctdistance=0.75
    )

    ax.legend(
        wedges, 
        labels,
        title="Subjects",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=8
    )

    fig.suptitle("Subject Hours Distribution", fontsize=14, fontweight='bold', y=0.95)

    return fig