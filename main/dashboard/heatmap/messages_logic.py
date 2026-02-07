from weeks import week_offset


TOPICS = {
    "exam": {
        "keywords": ["klausur", "test", "presentation", 
                     "prüfung", "prüfungsergebnis", "prüfungsleistungen",
                     "prüfungsanmeldung", "anmeldung", "abmeldung", "prüfungsanmeldung"],
        "label": "Exam"
    },
    "termin": {
        "keywords": ["termin", "meeting"],
        "label": "Termin"
    },
    "news": {
        "keywords": ["news", "uninews", "newsletter"],
        "label": "News"
    },
    "updates": {
        "keywords": ["updates", "verschiebung", "neue"],
        "label": "Updates"
    },
    "events": {
        "keywords": ["events", "einladung", "event"],
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

def topics_week_matrix(messages):
    matrix = {
        topic_id: [0, 0, 0, 0, 0]
        for topic_id in TOPICS
    }

    for msg in messages:
        topic_id = detect_topic(msg.subject)
        if topic_id is None:
            continue

        week = week_offset(msg.date)
        if 0 <= week < 5:
            matrix[topic_id][4 - week] +=1
    
    return matrix

def topic_labels():
    return [TOPICS[t]["label"] for t in TOPICS]
  
