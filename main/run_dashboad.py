import matplotlib.pyplot as plt

from user import schedule
from utils_time import hour_str
from dashboard import subject_hours_pie

# =========================
# PIE CHART: subjects + hours
# =========================

subject_hours = subject_hours_pie(schedule)

values = list(subject_hours.values())

labels = [
    f"{subject}\n{hour_str(hours)}"
    for subject, hours in subject_hours.items()
]

plt.figure()
plt.pie(
    values,
    labels=labels,
    startangle=90
)
plt.title("Study load by subject")
plt.show()
