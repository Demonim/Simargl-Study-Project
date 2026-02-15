from main.dashboard.pie.create_pie import create_pie
from main.dashboard.pie.subjects_logic import subject_hours

def get_pie_chart(schedule, text_color='black'):
    """
    High-level function to generate a pie chart of study hours per subject.
   
    Args:
        schedule: The user's schedule object with lesson entries.
        text_color (str): Theme-compliant color for text elements in the chart.
    Returns:
        Figure: Matplotlib Figure object ready for UI integration.
    """

    subject_data = subject_hours(schedule)
    pie_chart = create_pie(subject_data, text_color)
    return pie_chart

