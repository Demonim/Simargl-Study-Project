import pandas as pd
from datetime import datetime, timedelta

# Configuration dictionary defining study-related topics and their keyword triggers
TOPICS = {
    "exam": {"keywords": ["klausur", "test", "presentation", "exam",
                     "prüfung", "prüfungsergebnis", "prüfungsleistungen",
                     "prüfungsanmeldung", "anmeldung", "abmeldung", "prüfungszulassung"], "label": "Exams"},
    "termin": {"keywords": ["termin", "meeting", "appointment"], "label": "Appointments"},
    "news": {"keywords": ["news", "uninews", "newsletter"], "label": "News"},
    "updates": {"keywords": ["updates", "verschiebung", "neue", "changed"], "label": "Updates"},
    "events": {"keywords": ["events", "einladung", "event", "invitation", "marketplace"], "label": "Events"}
}

def detect_topic(subject: str) -> str | None:
    """
    Categorizes a message subject based on predefined keywords.

    Args:
        subject (str): The subject line of the email.

    Returns:
        str | None: The topic ID if a match is found, otherwise None.
    """
    if subject is None:
        return None
    
    # Normalize subject to lowercase string
    subject = str(subject).lower()

    # Check each topic for keyword match
    for topic_id, data in TOPICS.items():
        if "keywords" in data and any(word in subject for word in data["keywords"]):
            return topic_id
    return None

def create_messages_df(subjects, dates):
    """
    Processes raw email data into a cleaned Pandas DataFrame with calendar week offsets.

    This function normalizes timestamps to a Monday-to-Sunday calendar week system
    and calculates how many weeks ago a message was received relative to today.

    Args:
        subjects (list): A list of email subject strings.
        dates (list): A list of email date strings or datetime objects.

    Returns:
        pd.DataFrame: A processed DataFrame containing cleaned dates, detected topics,
                      and calculated week offsets.
    """
    if not subjects or not dates:
        return pd.DataFrame(columns=['subject', 'date', 'topic_id', 'week_offset'])
    
    # Ensure subjects and dates are same length
    if len(subjects) != len(dates):
        min_len = min(len(subjects), len(dates))
        subjects = subjects[:min_len]
        dates = dates[:min_len]
        
    # Build DataFrame from subjects and dates
    df = pd.DataFrame({'subject': subjects, 'date': dates})

    # Convert date column to datetime, drop invalid
    df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.tz_localize(None)
    df = df.dropna(subset=['date'])
   
    if df.empty:
        return pd.DataFrame(columns=['subject', 'date', 'topic_id', 'week_offset'])
    
    # Detect topic for each subject
    df['topic_id'] = df['subject'].apply(detect_topic)

    # Get current week's Monday
    now = datetime.now()
    current_monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate Monday of each message's week
    df['monday_of_week'] = df['date'].apply(lambda x: x - timedelta(days=x.weekday()))
    df['monday_of_week'] = df['monday_of_week'].dt.normalize()

    # Calculate week offset from current week
    df['week_offset'] = ((current_monday - df['monday_of_week']).dt.days // 7)

    return df

def topics_week_matrix_df(subjects, dates):
    """
    Creates a 5-week frequency matrix of message topics.

    Args:
        subjects (list): Raw list of subjects.
        dates (list): Raw list of dates.

    Returns:
        DataFrame: A pivot table where rows are topics and columns are week indices.
    """
    df = create_messages_df(subjects, dates)

    # Define all possible topic rows and week columns
    full_index = list(TOPICS.keys())
    full_columns = range(5)

    # Filter messages to last 5 weeks and valid topics
    mask = (df['week_offset'] >= 0) & (df['week_offset'] < 5) & (df['topic_id'].notna())

    filtered_df = df[mask].copy()
    if filtered_df.empty:
        return pd.DataFrame(0, index=full_index, columns=full_columns)
    
    # Calculate week index for heatmap (0 = oldest, 4 = current)
    filtered_df['week_idx'] = 4 - filtered_df['week_offset']

    # Build pivot table: rows=topic, columns=week, values=count
    matrix_df = filtered_df.pivot_table(
        index='topic_id',
        columns='week_idx',
        aggfunc='size',
        fill_value=0
    )
    # Ensure all topics and weeks are present, fill missing with zero
    matrix_df = matrix_df.reindex(index=full_index, columns=full_columns, fill_value=0)

    return matrix_df