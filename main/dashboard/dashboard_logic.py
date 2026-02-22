from dashboard.pie.create_pie import create_pie
from dashboard.pie.subjects_logic import subject_hours
from dashboard.heatmap.create_heatmap import create_heatmap
from .timer_bar.weekly_study_tracker import WeeklyStudyTracker
from .timer_bar.create_bar import create_stacked_bar, update_stacked_bar
from .scatter_plot.scatter_logic import prepare_scatter_data
from .scatter_plot.create_scatter_plot import generate_scatter_figure 
from datetime import datetime

def error_chart(message, color='black'):
    from matplotlib.figure import Figure
    fig = Figure(figsize=(8, 6), tight_layout=True)
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, message, ha='center', va='center', color=color)
    return fig

def get_pie_chart(schedule, text_color='black'):
    global subject_data
    """
    High-level function to generate a pie chart of study hours per subject.
   
    Args:
        schedule: The user's schedule object with lesson entries.
        text_color (str): Theme-compliant color for text elements in the chart.
    Returns:
        Figure: Matplotlib Figure object ready for UI integration.
    """
    try:
        if schedule is None:
            return error_chart('No schedule data available', text_color)
        
        # Calculate subject hours and create pie chart
        subject_data = subject_hours(schedule)
        pie_chart = create_pie(subject_data, text_color)
        return pie_chart
    except Exception as e:
        print(f"[dashboard_logic] Error in get_pie_chart: {e}")
        return error_chart(f'Error generating pie chart: {str(e)}', text_color)

def get_scatter_plot(messages, color='black'):
    """
    High-level orchestrator for the Study Intensity Matrix.
    Uses globally stored subject_data to correlate hours with message counts.
   
    Args:
        messages: List of message objects containing subject lines and metadata.
        color (str): Theme-compliant color for text, labels, and plot boundaries.


    Returns:
        Figure: A Matplotlib Figure object representing the interactive scatter plot.  
    """
   
    try:
        df, medians, math_stats = prepare_scatter_data(subject_data, messages)  
        scatter_chart = generate_scatter_figure(df, medians, math_stats, color=color) 
        return scatter_chart
    except Exception as e:
        print(f"[dashboard_logic] Error in get_scatter_plot: {e}")
        return error_chart(f'Error generating scatter plot: {str(e)}', color)

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
    try:
        if ecampusmail is None:
            return error_chart('No email data available', color)
        subjects_data, dates_data = ecampusmail.show_subjects(last_n=300)  # Get recent subjects and dates
        heatmap_chart = create_heatmap(subjects_data, dates_data, color)  # Generate heatmap
        return heatmap_chart
    except Exception as e:
        print(f"[dashboard_logic] Error in get_heatmap: {e}")
        return error_chart(f'Error generating heatmap: {str(e)}', color)

def refresh_stacked_bar(canvas_bar, manual_inputs=None):
    """
    Triggers a live update of the weekly study tracker bar chart.
    Useful for real-time timer updates or manual input synchronization.
    """
    try:
        if not _tracker:
            return

        if canvas_bar is None or not hasattr(canvas_bar, 'figure') or canvas_bar.figure is None:
            return

        if manual_inputs:
            process_manual_input(manual_inputs)  # Update tracker with manual input
        current_data = get_tracker_data()  # Get current tracker data
        update_stacked_bar(canvas_bar.figure, current_data)  # Update the bar chart
    except Exception as e:
        print(f"[dashboard_logic] Error in refresh_stacked_bar: {e}")

_tracker = None

def initialize_tracker(login: str):
    """Initializes the database-backed tracker for study sessions."""
    global _tracker
    _tracker = WeeklyStudyTracker(login=login)  # Create tracker instance

def get_weekly_bar_chart():
    """Returns a newly generated stacked bar chart for the current week."""
    current_data = get_tracker_data()  # Get current tracker data
    return create_stacked_bar(current_data)  # Create and return bar chart

def process_manual_input(day_inputs):
    """
    High-level Input/Output function to synchronize manual time entries with the persistent tracker.
   
    This function processes raw user input from UI fields (hours and minutes) and updates
    the underlying study database.

    Args:
        day_inputs (list/tuple): A collection of tuples in the format (day_code, hours, minutes).

    Returns:
        dict: The updated state of all study sessions across the week.
    """
    try:
        if not _tracker:
            return {}

        if not isinstance(day_inputs, (list, tuple)):
            return _tracker.all() if _tracker else {}

        for day_input in day_inputs:
            if not isinstance(day_input, (list, tuple)) or len(day_input) < 3:
                continue
           
            day, h, m = day_input[0], day_input[1], day_input[2]
           
            try:
                h_str = str(h).strip() if h is not None else ""
                m_str = str(m).strip() if m is not None else ""
            except Exception as e:
                print(f"[dashboard_logic] Error parsing manual input: {e}")
                continue
           
            if not h_str and not m_str:
                continue
               
            try:
                total_hours = float(h_str or 0) + (float(m_str or 0) / 60.0)  # Calculate total hours
                if total_hours < 0:
                    total_hours = 0
                _tracker.set_day(day, total_hours)  # Update tracker for the day
            except (ValueError, TypeError) as e:
                print(f"[dashboard_logic] Error converting manual input: {e}")
                continue
               
        return _tracker.all()
    except Exception as e:
        print(f"[dashboard_logic] Error in process_manual_input: {e}")
        return _tracker.all() if _tracker else {}

def get_tracker_data():
    """Fetches all raw study time data from the current session."""
    return _tracker.all() if _tracker else {}

def start_study_session():
    """Returns the current day of week in English format (Mon, Tue, etc.)"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    # Get current weekday as string
    return days[datetime.now().weekday()]

def stop_study_session(day_code, hours):
    """Adds a newly recorded time session to the tracker's persistent storage."""
    try:
        if _tracker and day_code:
            try:
                hours = float(hours) if hours is not None else 0.0
                if hours < 0:
                    hours = 0.0
                _tracker.add_time(day_code, hours)  # Add time to tracker for the day
            except (ValueError, TypeError) as e:
                print(f"[dashboard_logic] Error converting hours in stop_study_session: {e}")
        return _tracker.all() if _tracker else {}
    except Exception as e:
        print(f"[dashboard_logic] Error in stop_study_session: {e}")
        return _tracker.all() if _tracker else {}

def clear_all_data():
    """Resets all stored study sessions in the tracker and returns the empty state."""
    if _tracker:
        _tracker.reset_all()  # Reset all tracker data
    return get_tracker_data()