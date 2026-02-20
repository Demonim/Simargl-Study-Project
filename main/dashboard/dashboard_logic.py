from main.dashboard.pie.create_pie import create_pie
from main.dashboard.pie.subjects_logic import subject_hours
from main.dashboard.heatmap.create_heatmap import create_heatmap
from .timer_bar.weekly_study_tracker import WeeklyStudyTracker
from .timer_bar.create_bar import create_stacked_bar, update_stacked_bar
from .scatter_plot.scatter_logic import prepare_scatter_data
from .scatter_plot.create_scatter_plot import generate_scatter_figure 
from datetime import datetime

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
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 6), tight_layout=True)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No schedule data available', ha='center', va='center', color=text_color)
            return fig
        
        subject_data = subject_hours(schedule)
        pie_chart = create_pie(subject_data, text_color)
        return pie_chart
    except Exception as e:
        from matplotlib.figure import Figure
        fig = Figure(figsize=(8, 6), tight_layout=True)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f'Error generating pie chart: {str(e)}', ha='center', va='center', color=text_color)
        return fig

def get_scatter_plot(schedule, messages):
    """
    High-level function to prepare data and generate a scatter plot of course activity.
   
    Args:
        schedule: The user's schedule object with lesson entries.
        messages: List of tuples with course names and message counts.


    Returns:
        Figure: A Matplotlib Figure object representing the scatter plot.  
    """
   
    df, medians, excluded = prepare_scatter_data(subject_data, messages)
    scatter_chart = generate_scatter_figure(df, medians, excluded)
    return scatter_chart

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
            from matplotlib.figure import Figure
            fig = Figure(figsize=(8, 6), tight_layout=True)
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No email data available', ha='center', va='center', color=color, transform=ax.transAxes)
            ax.set_axis_off()
            return fig
        
        subjects_data, dates_data = ecampusmail.show_subjects(last_n=300)
        heatmap_chart = create_heatmap(subjects_data, dates_data, color)
        return heatmap_chart
    except Exception as e:
        from matplotlib.figure import Figure
        fig = Figure(figsize=(8, 6), tight_layout=True)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f'Error generating heatmap: {str(e)}', ha='center', va='center', color=color, transform=ax.transAxes)
        ax.set_axis_off()
        return fig

def refresh_stacked_bar(canvas_bar, manual_inputs=None):
    """
    High-level function to refresh the bar chart from UI.
    Moves visualization calls away from main.py.
    """
    try:
        if not _tracker:
            return

        if canvas_bar is None or not hasattr(canvas_bar, 'figure') or canvas_bar.figure is None:
            return

        if manual_inputs:
            process_manual_input(manual_inputs)

        current_data = get_tracker_data()
        update_stacked_bar(canvas_bar.figure, current_data)
    except Exception:
        pass

_tracker = None

def initialize_tracker(login: str):
    global _tracker
    _tracker = WeeklyStudyTracker(login=login)

def get_weekly_bar_chart():
    current_data = get_tracker_data()
    return create_stacked_bar(current_data)

def process_manual_input(day_inputs):
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
            except Exception:
                continue
           
            if not h_str and not m_str:
                continue
               
            try:
                total_hours = float(h_str or 0) + (float(m_str or 0) / 60.0)
                if total_hours < 0:
                    total_hours = 0
                _tracker.set_day(day, total_hours)
            except (ValueError, TypeError):
                continue
               
        return _tracker.all()
    except Exception:
        return _tracker.all() if _tracker else {}

def get_tracker_data():
    return _tracker.all() if _tracker else {}

def start_study_session():
    """Returns the current day of week in English format (Mon, Tue, etc.)"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return days[datetime.now().weekday()]

def stop_study_session(day_code, hours):
    try:
        if _tracker and day_code:
            try:
                hours = float(hours) if hours is not None else 0.0
                if hours < 0:
                    hours = 0.0
                _tracker.add_time(day_code, hours)
            except (ValueError, TypeError):
                pass
        return _tracker.all() if _tracker else {}
    except Exception:
        return _tracker.all() if _tracker else {}

def clear_all_data():
    """
    Resets all stored study sessions in the tracker and returns the empty state.
    """
    if _tracker:
        _tracker.reset_all()
    return get_tracker_data()