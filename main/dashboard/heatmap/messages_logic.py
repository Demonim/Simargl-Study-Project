from weeks import week_offset


TOPICS = {
    "exam": {
        "keywords": ["klausur", "test", "presentation", "prüfung"],
        "label": "Exam"
    },
    "termin": {
        "keywords": ["termin", "meeting"],
        "label": "Termin"
    },
    "news": {
        "keywords": ["news", "uninews"],
        "label": "News"
    },
    "changes": {
        "keywords": [],
        "label": "Changes"
    },
    "events": {
        "keywords": [],
        "label": "Events"
    }
}                #ДОПИСАТИ

def detect_topic(subject: str) -> str | None:
    subject = subject.lower()

    for topic_id, data in TOPICS.items():
        for word in data:
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
  
