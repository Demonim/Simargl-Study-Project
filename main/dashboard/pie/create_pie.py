from matplotlib.figure import Figure
from dashboard.pie.pie_val_lab import pie_values_labels


def create_pie(subject_hours, text_color='black'):
    fig = Figure(figsize=(8, 6), tight_layout=True)

    fig.patch.set_facecolor('none')

    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    values, labels = pie_values_labels(subject_hours)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,
        textprops={'color': text_color}
    )

    leg = ax.legend(
        wedges,
        labels,
        title="Subjects",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
        frameon=False
    )

    leg.get_title().set_color(text_color)
    for text in leg.get_texts():
        text.set_color(text_color)

    fig.suptitle("Subject Hours Distribution",
                 fontsize=14,
                 fontweight='bold',
                 y=0.95,
                 color=text_color)

    return fig