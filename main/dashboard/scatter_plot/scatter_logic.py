import re
import pandas as pd

def extract_course_from_message(subject_text):
    """
    Parses email subject lines to extract clean course names.
   
    Args:
        subject_text (str): The raw subject string from Stud.IP or email metadata.
       
    Returns:
        str: A normalized, lowercase course title.
    """
    bracket_match = re.search(r'\[(.*?)\]', subject_text)
    if bracket_match:
        return re.sub(r'^\d+:\s*', '', bracket_match.group(1)).strip().lower()
   
    keyword_match = re.search(r'(?:Veranstaltung|Übung|Course):\s*(.*?)(?:\s+(?:zugesagt|abgesagt|cancelled|cancell|$))', subject_text)
    if keyword_match:
        return keyword_match.group(1).strip().lower()
   
    return subject_text.lower()

def prepare_scatter_data(hours_data, messages):
    """
    Aggregates schedule and message data into a statistical DataFrame.
   
    Args:
        hours_data (dict): Mapping of {Course_Title: Study_Hours}.
        messages (list): Collection of message objects containing subject lines.
       
    Returns:
        tuple: (DataFrame, tuple of medians, dict of math_stats).
    """
    if not hours_data:
        return pd.DataFrame(), (0, 0), []

    processed_messages = []
    for m in messages:
        subject = str(getattr(m, 'subject', ''))
        extracted_name = extract_course_from_message(subject)
        processed_messages.append(extracted_name)

    rows = []
    for title, hours in hours_data.items():
        clean_target = re.sub(r'^[A-Z]\.[A-Z\.]+\d+:\s*', '', title).strip().lower()
        clean_target = re.sub(r'^\d+\s*', '', clean_target).strip().lower()
        clean_target = re.sub(r'\(.*\)', '', clean_target).strip()
       
        m_count = sum(1 for msg_name in processed_messages if clean_target in msg_name)
       
        ratio = m_count / (hours + 1) if hours > 0 else 0
   
        rows.append({
            'name': title,
            'hours': float(hours),
            'messages': int(m_count),
            'ratio': ratio
        })

    df = pd.DataFrame(rows)

    r_mean = df['ratio'].mean()
    r_std = df['ratio'].std() if len(df) > 1 else 1

    math_stats = {
        'mean_ratio': r_mean,
        'std_dev': r_std
    }

    df['engagement_score'] = (df['ratio'] - r_mean) / (r_std if r_std != 0 else 1)


    def get_insight(score):
        """
        Translates numerical Z-scores into human-readable engagement insights.
       
        Args:
            score (float): The standardized engagement score (Z-score).
           
        Returns:
            str: Qualitative description of the communication intensity.
           
        Threshold Logic:
            - Score > 1.0: Represents activity more than one standard deviation
              above the mean (Over-communicated).
            - Score < -1.0: Represents activity more than one standard deviation
              below the mean (Under-communicated).
            - Values between -1.0 and 1.0 are considered within the expected
              'Balanced' range for the current semester.
        """
        if score > 1: return "Over-communicated (High focus)"
        if score < -1: return "Under-communicated (Self-study)"
        return "Balanced activity"

    df['insight'] = df['engagement_score'].apply(get_insight)
   
    med_hours = df['hours'].median() if not df.empty else 0
    med_msg = df['messages'].median() if not df.empty else 0


    def classify(row):
        """
        Assigns each course to one of four strategic quadrants using a Median-split.
       
        Args:
            row (pd.Series): A row from the DataFrame containing 'hours' and 'messages'.
           
        Returns:
            str: The name of the quadrant the course belongs to.
           
        Quadrant Matrix:
            1. Active Ecosystem: Above median in both time and communication.
            2. Live Discussion: Efficient engagement (low time, high messages).
            3. Routine Lectures: Traditional study (high time, low messages).
            4. Inactive Course: Below median across both metrics.
        """
        if row['hours'] >= med_hours and row['messages'] >= med_msg:
            return "Active Ecosystem"
        elif row['hours'] < med_hours and row['messages'] >= med_msg:
            return "Live Discussion"
        elif row['hours'] >= med_hours and row['messages'] < med_msg:
            return "Routine Lectures"
        else:
            return "Inactive Course"

    df['quadrant'] = df.apply(classify, axis=1)
    return df, (med_hours, med_msg), math_stats