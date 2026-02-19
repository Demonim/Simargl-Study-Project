import pandas as pd
from datetime import datetime

TOPICS = {
    "exam": {"keywords": ["klausur", "test", "presentation", "exam",
                     "prüfung", "prüfungsergebnis", "prüfungsleistungen",
                     "prüfungsanmeldung", "anmeldung", "abmeldung"], "label": "Exams"},
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

    subject = str(subject).lower()
    for topic_id, data in TOPICS.items():
        if any(word in subject for word in data["keywords"]):
            return topic_id
    return None


def create_messages_df(subjects, dates):
    """
    Processes raw lists into a cleaned Pandas DataFrame for time-series analysis.

    Args:
        subjects (list): List of subject strings.
        dates (list): List of date strings/objects.

    Returns:
        DataFrame: A structured dataframe with normalized dates and topic IDs.
    """

    if not subjects or not dates:
        return pd.DataFrame(columns=['subject', 'date', 'topic_id', 'week_offset'])
    
    df = pd.DataFrame({'subject': subjects, 'date': dates})
   
    df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.tz_localize(None)
    df = df.dropna(subset=['date'])
   
    df['topic_id'] = df['subject'].apply(detect_topic)
   
    now = datetime.now()
    df['week_offset'] = (now - df['date']).dt.days // 7
   
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
   
    full_index = list(TOPICS.keys())
    full_columns = range(5)

    mask = (df['week_offset'] >= 0) & (df['week_offset'] < 5) & (df['topic_id'].notna())
    filtered_df = df[mask].copy()

    if filtered_df.empty:
        return pd.DataFrame(0, index=full_index, columns=full_columns)

    filtered_df['week_idx'] = 4 - filtered_df['week_offset']
   
    matrix_df = filtered_df.pivot_table(
        index='topic_id',
        columns='week_idx',
        aggfunc='size',
        fill_value=0
    )
   
    matrix_df = matrix_df.reindex(index=full_index, columns=full_columns, fill_value=0)
   
    return matrix_df