from dashboard.pie.create_pie import create_pie
from dashboard.pie.subjects_logic import subject_hours
from dashboard.heatmap.create_heatmap import create_heatmap
from .timer_bar.weekly_study_tracker import WeeklyStudyTracker
from .timer_bar.create_bar import create_stacked_bar, update_stacked_bar
from datetime import datetime

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

def get_new_stacked_bar(tracker):
    """
    High-level function to generate an updated stacked bar chart of weekly study hours.

    Args:
        tracker (WeeklyStudyTracker): The tracker instance containing current study data.
    Returns:
        Figure: Matplotlib Figure object representing the updated study hours.
    """
    current_data = tracker.all()
    new_bar = create_stacked_bar(current_data)
    return new_bar

def refresh_stacked_bar(canvas_bar, manual_inputs=None):
    """
    High-level function to refresh the bar chart from UI.
    Moves visualization calls away from main.py.
    """
    if not _tracker:
        return

    if manual_inputs:
        process_manual_input(manual_inputs)

    current_data = get_tracker_data()

    update_stacked_bar(canvas_bar.figure, current_data)

_tracker = None

def initialize_tracker(login: str):
    global _tracker
    _tracker = WeeklyStudyTracker(login=login)

def get_formatted_placeholders():
    data = get_tracker_data()
    placeholders = {}
   
    for day, values in data.items():
        manual_val = values.get('manual', 0.0)
        h = int(manual_val)
        m = int((manual_val % 1) * 60)
        placeholders[day] = {"h": str(h), "m": str(m)}
       
    return placeholders

def get_weekly_bar_chart():
    current_data = get_tracker_data()
    return create_stacked_bar(current_data)

def process_manual_input(day_inputs):
    if not _tracker:
        return {}

    for day, h, m in day_inputs:
        h_str = h.strip()
        m_str = m.strip()
       
        if not h_str and not m_str:
            continue
           
        try:
            total_hours = float(h_str or 0) + (float(m_str or 0) / 60.0)
            _tracker.set_day(day, total_hours)
        except ValueError:
            continue
           
    return _tracker.all()

def get_tracker_data():
    return _tracker.all() if _tracker else {}

def start_study_session():
    return datetime.now().strftime('%a')

def stop_study_session(day_code, hours):
    if _tracker and day_code:
        _tracker.add_time(day_code, hours)
    return _tracker.all() if _tracker else {}

def clear_all_data():
    """
    Resets all stored study sessions in the tracker and returns the empty state.
    """
    if _tracker:
        _tracker.reset_all()
    return get_tracker_data()