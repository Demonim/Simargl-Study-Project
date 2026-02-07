from main.dashboard.heatmap.weeks import week_offset

TOPICS = {
    "exam": {
        "keywords": ["klausur", "test", "presentation", "exam",
                     "prüfung", "prüfungsergebnis", "prüfungsleistungen",
                     "prüfungsanmeldung", "anmeldung", "abmeldung"],
        "label": "Exams"
    },
    "termin": {
        "keywords": ["termin", "meeting", "appointment"],
        "label": "Appointments"
    },
    "news": {
        "keywords": ["news", "uninews", "newsletter"],
        "label": "News"
    },
    "updates": {
        "keywords": ["updates", "verschiebung", "neue", "changed"],
        "label": "Updates"
    },
    "events": {
        "keywords": ["events", "einladung", "event", "invitation", "marketplace"],
        "label": "Events"
    }
}

def detect_topic(subject: str) -> str | None:
    subject = subject.lower()
    for topic_id, data in TOPICS.items():
        for word in data["keywords"]: 
            if word in subject:
                return topic_id
    return None

def topics_week_matrix(subjects, dates):
    matrix = {
        topic_id: [0, 0, 0, 0, 0]
        for topic_id in TOPICS
    }

    for subj, dt in zip(subjects, dates):
        if dt is None: 
            continue
            
        topic_id = detect_topic(subj)
        if topic_id is None:
            continue

        week = week_offset(dt)
        if 0 <= week < 5:
            matrix[topic_id][4 - week] += 1
    
    return matrix

def topic_labels():
    return [TOPICS[t]["label"] for t in TOPICS]