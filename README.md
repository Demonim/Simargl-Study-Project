# Simargl: A ECampus Helper

Simargl is a study project aimed at enhancing and streamlining the ECampus experience for students. It provides a modern, customizable interface and powerful tools for managing digital academic routines.

### Description
The default ECampus interface is often overloaded, slow, and lacks customization. Simargl addresses these issues by allowing users to track essential aspects of their digital routine, such as ECampusMail and StudIP, through a modern GUI. Data is retrieved using APIs or IMAP/SMTP protocols and presented in a user-friendly, customizable dashboard. Key libraries are used to render the most useful information, making Simargl a valuable tool for every student.

---

# Functionalities

### Data Storage
- Uses SQL databases to securely store local user data, calendar events from StudIP, notes, and more.
- Login credentials are hashed and databases are protected for user security.
- Supports both persistent and session-based data storage.

### User Management
- Local user profiles store credentials for ECampusMail and StudIP accounts.
- Users can add, switch, or delete local accounts at any time.
- Secure authentication and credential management.

### Interface
- Modern, responsive GUI built with PySide.
- Switchable dark and light themes, with additional theme options.
- Help button and contextual guidance available throughout the app.
- UI templates and layouts designed for clarity and ease of use.

### Visualizations
- Advanced visualizations for calendar, study statistics, and more using PySide and custom plotting modules.
- Interactive graphs: heatmap, pie chart, scatter plot, timer bar, and others.
- Flexible period selection and filtering options for all visualizations.
- Visualization modules are extensible for future features.

---

# Table for self-check

4 out of the 7 categories are fulfilled.

| Category                     | Details                                                                           | Mark with ✔️ |
|:-----------------------------|:----------------------------------------------------------------------------------|--------------|
| 1. Data Storage and Handling | Management system                                                                 |      ✔️      |
|                              | No plaintext passwords                                                            |      ✔️      |
| 2. User Management           | Login with username, pw                                                           |      ✔️      |
|                              | Four user accounts userID, name, user_name, and password, one admin               |      ✔️      |
|                              | Logout with timeout                                                               |      ✔️      |
|                              | Admin privileges                                                                  |      ✔️      |
| 3. Interface                 | CLI, GUI or Web interface for users                                               |      ✔️      |
|                              | Extensive interface functions (account management, queries, analysis, help)       |      ✔️      |
|                              | Visualizations in the interface, dashboard style                                  |      ✔️      |
| 4. Visualisations            | Visualizations displayed                                                          |      ✔️      |
|                              | Dashboard with several graphs composed together                                   |      ✔️      |
|                              | The visualizations offer interactivity                                            |      ✔️      |
| Always mandatory             | Project proposal with incorporated feedback from tutor                            |      ✔️      |
|                              | GitHub repo with sensible commit messages, template README, contributions section |      ✔️      |
|                              | Frequent commenting                                                               |      ✔️      |
|                              | Docstrings for every function/class                                               |      ✔️      |
|                              | Testing of relevant functionalities to avoid crashing                             |      ✔️      |
|                              | Help page for system                                                              |      ✔️      |
|                              | Milestone presentation                                                            |      ✔️      |
|                              | AI-Usage Cards                                                                    |      ✔️      |

----

# Installation

1. **Clone the repository:**
	```bash
	git clone https://github.com/Demonim/Simargl.git
	cd Simargl
	```

2. **Create a virtual environment:**
	```bash
	python -m venv venv
	# Activate the virtual environment:
	# On Windows:
	venv\Scripts\activate
	# On macOS/Linux:
	source venv/bin/activate
	```

3. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```

# Running the Project

To start the application, run:

```bash
python main/main.py
```

## Project Structure

- `main/` — Main application code
- `main/UI/` — UI files (.ui)
- `main/dashboard/` — Dashboard logic and visualizations
- `main/storage/` — Data storage
- `unit_tests/` — Unit tests

---

For any issues, please open an issue on the repository or contact the maintainer.

----

# Project Timeline

Week-by-week schedule:

**Week 1-2:** Project proposal, repository setup, initial planning, requirements gathering, initial design, UI improvements.

**Week 3-4** ECampus and StudIP integration, implementation of local login and database.

**Weeks 5-8:** Dashboard core logic and main visualizations (heatmap, pie, scatter, timer bar).

**Week 4-10:** UI improvements, styles, and themes.

**Week 4-5:** Admin features and user management.

**Week 5-6:** Calendar, notes, and courses modules. Help, localization, and support windows.

**Week 7-8:** Unit tests and bug fixes.

**Week 9-10:** Final polish and presentation preparation, and visualization (scatter plot). Final README updates.

----

# Group Details
- **Group name:** Data Sorcerers
- **Repository:** https://github.com/Demonim/Simargl
- **Tutor Responsible:** Tobias Kristoffer Mark
- **Team Leader:** Dmytro "Demonim" Kutsak
- **Group Members:** Nichita "Nikityu2" Licov, Diana "dibardyk" Bardyk

---

# Contributions
- **Demonim:** Led backend development, including the integration with StudIP and ECampusMail, and architected the login storage system. Implemented ECampusMail notification features, database management, and core backend logic. Provided numerous code and comment fixes, wrote docstrings and unit tests for the main and simargl modules, and contributed ideas for new themes. Handled localization updates, and ensured code quality through frequent refactoring and bug fixes.
- **Nikityu2:** Designed and implemented the full GUI interface, including UI logic, visual design, and user experience improvements. Created and organized UI templates and styles, developed storage classes (Notes and CourseDays), and contributed to login storage improvements. Integrated calendar features, managed theme switching, and optimized interface responsiveness. Developed and refined multiple windows (Admin, Email, Help, Notes, Courses, etc.), and ensured seamless integration of all UI components. Enhanced error handling and user guidance throughout the application.
- **dibardyk:** Developed and implemented all dashboard features, being fully responsible for the dashboard’s logic, structure, and every visualization module (heatmap, pie chart, scatter plot, timer bar). Wrote unit tests for dashboard_logic and weekly_study_tracker. Designed templates and layouts for the program. Improved data handling and error management, refactored and optimized code for readability and maintainability, and added comprehensive comments and docstrings. Enhanced user interaction by refining the interface and ensuring robust connections between UI components and backend logic. Introduced new functions for timer and diagram features, and contributed to the overall improvement of data visualization and user experience in the application.

---

# Acknowledgments
### Websites
- StudIP Göttingen: https://www.studip.uni-goettingen.de/dispatch.php/start
- ECampusMail Göttingen: https://email.gwdg.de/owa/auth/logon.aspx
...

### Libraries
- **PySide6**: For building the modern, cross-platform graphical user interface (GUI).
- **studipy**: Used for interacting with StudIP, retrieving calendar events, course information, and user data. See: https://github.com/FrederikRichter/studipy
- **matplotlib**: Used for creating advanced visualizations such as heatmaps, pie charts, scatter plots, and timer bars.
- **pandas**: For efficient data manipulation, analysis, and handling of tabular data.
- **requests**: To interact with web APIs and retrieve data from external services.
- **sqlite3**: For secure and lightweight local SQL database storage.
- **email, imaplib, smtplib**: For handling ECampusMail integration and communication.
- **json**: For configuration, data storage, and communication between modules.
- **datetime**: For managing and processing time-related data, especially in calendar and timer features.
- **numpy**: Used for numerical operations and supporting data analysis in visualizations.
- **os, sys**: For file and environment management, and application control.

For more detailed infomation check requirements.txt.