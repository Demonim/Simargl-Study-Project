from main.dashboard.pie.create_pie import create_pie
from main.dashboard.pie.subjects_logic import subject_hours
from main.dashboard.heatmap.create_heatmap import create_heatmap
from main.simargl import ECampusMail

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

def get_heatmap(ecampusmail, color='black'):
    """
    High-level function to generate an activity heatmap based on email metadata.

    Fetches the most recent emails, extracts subject/date pairs, and 
    visualizes the frequency of specific topics over the last 5 weeks.

    Args:
        ecampusmail (ECampusMail): Active mail client instance to fetch data.
        color (str): Theme-compliant color for text and heatmap borders.

    Returns:
        Figure: A Matplotlib Figure object representing topic activity.
    """
    
    subjects_data, dates_data = ecampusmail.show_subjects(last_n=300)
    heatmap_chart = create_heatmap(subjects_data, dates_data, color)
    return heatmap_chart