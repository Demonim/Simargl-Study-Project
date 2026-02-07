from pie_val_lab import pie_values_labels
from matplotlib.figure import Figure

def create_pie(subject_hours):
    fig = Figure()
    ax = fig.add_subplot(111)

    values, labels = pie_values_labels(subject_hours)
    ax.pie(values, labels = labels, autopct = '%1.1f%%', startangle=90)


    return fig