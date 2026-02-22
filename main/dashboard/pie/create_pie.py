from matplotlib.figure import Figure
from .subjects_logic import pie_values_labels


def create_pie(subject_hours, text_color='black'):
    """
    Generates a pie chart showing study hours distribution.
    
    Args:
        subject_hours (dict): Subject titles mapping to total hours.
        text_color (str): Color for labels, legend, and titles.
        
    Returns:
        Figure: Matplotlib Figure object with the rendered chart.
    """
    fig = Figure(figsize=(8, 6), tight_layout=True)
    fig.patch.set_facecolor('none')

    ax = fig.add_subplot(111)
    ax.set_facecolor('none')

    if not subject_hours:
        ax.text(0.5, 0.5, 'No study data available', ha='center', va='center', color=text_color)   
        return fig

    # Prepare values and labels for pie chart
    values, labels = pie_values_labels(subject_hours)

    if not values or not labels:
        ax.text(0.5, 0.5, 'No study data available', ha='center', va='center', color=text_color)   
        return fig

    # Filter out zero values for cleaner chart
    filtered_pairs = [(v, l) for v, l in zip(values, labels) if v > 0]
    if not filtered_pairs:
        ax.text(0.5, 0.5, 'No study data available', ha='center', va='center', color=text_color)   
        return fig
    
    # Sort pairs alphabetically for consistent display
    sorted_pairs = sorted(filtered_pairs, key=lambda x: x[1])
    values, labels = zip(*sorted_pairs)

    # Draw pie chart with subject hours
    wedges, _, autotexts = ax.pie(
        values,
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=0.75,
        textprops={'color': text_color}
    )

    # Add legend for subjects, style for theme
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

    # Set plot title and return figure
    fig.suptitle("Subject Hours Distribution",
                 fontsize=14,
                 fontweight='bold',
                 y=0.95,
                 color=text_color)

    return fig