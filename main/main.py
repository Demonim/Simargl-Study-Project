import sys
import os
from pydoc import Helper

from PySide6.QtWidgets import (
    QTextBrowser,
    QApplication,
    QComboBox,
    QPushButton, 
    QLabel,
    QLineEdit
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from concurrent.futures import ThreadPoolExecutor
import simargl

# =========================
# THEMES
# =========================

DARK_THEME = """
QWidget {
background-color: qlineargradient(spread:pad,x1:10, y1:0, x2:0, y2:1,
    stop:0.00 rgba(2, 7, 15, 255),

    stop:0.07 rgba(0, 255, 120, 220),
    stop:0.11 rgba(2, 7, 15, 255),

    stop:0.18 rgba(80, 255, 140, 200),
    stop:0.23 rgba(2, 7, 15, 255),

    stop:0.30 rgba(0, 220, 100, 220),
    stop:0.35 rgba(2, 7, 15, 255),

    stop:0.42 rgba(120, 255, 160, 190),
    stop:0.47 rgba(2, 7, 15, 255),

    stop:0.54 rgba(0, 255, 140, 230),
    stop:0.59 rgba(2, 7, 15, 255),

    stop:0.66 rgba(90, 255, 130, 200),
    stop:0.71 rgba(2, 7, 15, 255),

    stop:0.78 rgba(0, 230, 110, 220),
    stop:0.83 rgba(2, 7, 15, 255),

    stop:0.90 rgba(120, 255, 160, 210),
    stop:0.95 rgba(2, 7, 15, 255),

    stop:1.00 rgba(2, 7, 15, 255)
);
font-family: Unispace;
}




QLabel#Login {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Password{
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QCalendarWidget QComboBox {
    background-color: #333;
    color: white;
}

QLabel {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 20pt;
}

QLineEdit#PasswordLine {
    background-color: 255, 255, 255
}

QLineEdit#LoginLine {
    background-color: 255, 255, 255
}

QCheckBox#CheckBox_1 {
    color: rgb(102, 255, 140);
    background-color: rgb(255, 255, 255, 0);
    font-size: 10pt
}

QPushButton {
    border: 2px solid #00ff88;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(102, 255, 140);
    font-size: 15pt;
}

QPushButton:hover {
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}

QComboBox#ThemeBox {
    background-color:  #02070f;
    color: #00ff88;        
    border: 2px solid #00ff88;
    padding: 5px;
}

QComboBox#ThemeBox QAbstractItemView {
    background-color: #02070f; 
    color: white;             
    selection-background-color: #00ff88;
    selection-color: black;
}

QPushButton#Help {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: transparent;
	color: rgb(0, 0, 0);
	font-size: 10pt;
}

QLabel#Error {
	color: rgb(0, 0, 0);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Error_2 {
	color: rgb(0, 0, 0);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QPushButton#Error_Button {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}


QPushButton#Back_Button{
    background-color: rgb(23, 130, 22);
    border: 2px solid #000000;
    border-radius: 6px;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}

QPushButton#Back_Button:hover{
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}



QLabel#Help {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 25pt;
}

QTextBrowser {
    color: rgb(102, 255, 140);
    background-color: rgb(0, 0, 0);
    font: 15pt;
}

QLineEdit#Help_Search {
    background-color: rgba(255, 255, 255);
}



QCalendarWidget QWidget{
	alternate-background-color: rgb(17, 148, 28);
}

QCalendarWidget QAbstractItemView {
    background-color: rgb(33, 125, 60);
    color: white;
    selection-background-color: #00ff88;
    selection-color: black;
    gridline-color: #00ff88;
}

QCalendarWidget QToolButton {
    color: white;
    background: rgb(15, 59, 28);;
}

QCalendarWidget QToolButton:hover {
    background: #444;
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #3daee9;
    selection-color: black;
}

QCalendarWidget QAbstractItemView::item:disabled {
    color: gray;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(15, 59, 28);
}

QCalendarWidget QToolButton QMenu {
     background-color: rgb(15, 59, 28);
     color: white
}




QLabel#Ecampus{
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QTableView {
    background-color: rgba(255, 255, 255, 0);
}

QPushButton#Exit_Button {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}




QPushButton#Exit_Button1 {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}
"""

LIGHT_THEME = """
QWidget {
background-color:qlineargradient(spread:pad, x1:10, y1:0, x2:0, y2:1,
    stop:0.00 rgba(240, 247, 255, 255),

    stop:0.07 rgba(114, 163, 242, 220),
    stop:0.11 rgba(240, 247, 255, 255),

    stop:0.18 rgba(114, 163, 242, 200),
    stop:0.23 rgba(240, 247, 255, 255),

    stop:0.30 rgba(114, 163, 242, 220),
    stop:0.35 rgba(240, 247, 255, 255),

    stop:0.42 rgba(114, 163, 242, 190),
    stop:0.47 rgba(240, 247, 255, 255),

    stop:0.54 rgba(114, 163, 242, 230),
    stop:0.59 rgba(240, 247, 255, 255),

    stop:0.66 rgba(114, 163, 242, 200),
    stop:0.71 rgba(240, 247, 255, 255),

    stop:0.78 rgba(114, 163, 242, 220),
    stop:0.83 rgba(240, 247, 255, 255),

    stop:0.90 rgba(114, 163, 242, 210),
    stop:0.95 rgba(240, 247, 255, 255),

    stop:1.00 rgba(240, 247, 255, 255)
);
font-family: Unispace;
}



QLabel#Login {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QLabel#Password{
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
}

QCalendarWidget QComboBox {
    background-color: #333;
    color: white;
}

QLabel {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 20pt;
}

QLineEdit {
    background-color: 255, 255, 255
}

QCheckBox#CheckBox_1 {
    color: rgb(79, 149, 255);
    background-color: rgb(255, 255, 255, 0);
    font-size: 10pt
}

QPushButton {
    border: 2px solid #4f95ff;
    border-radius: 6px;
    background-color: transparent;
	color: rgb(79, 149, 255);
	font-size: 15pt;
}

QPushButton:hover {
    border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QComboBox#ThemeBox {
    background-color: #f0f7ff;
    color: #4f95ff;        
    border: 2px solid #4f95ff;
    padding: 5px;
}
QComboBox#ThemeBox QAbstractItemView {
    background-color: rgb(114, 163, 242);
    color: #f0f7ff;               
    selection-background-color: #00ff88;
    selection-color: white;
}

QPushButton#Help {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: transparent;
	color: rgb(0, 0, 0);
	font-size: 10pt;
}



QPushButton#Back_Button{
	border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QPushButton#Back_Button:hover{
    border: 2px solid rgb(0,0,0);
    border-radius: 6px;
    background-color: rgb(20,111,161);
	color: rgb(79, 149, 255);
	font-size: 15pt;
}

QLabel#Help {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 25pt;
}

QTextBrowser {
    color: rgb(0, 0, 0);
    background-color: rgb(255, 255, 255);
    font: 25pt;
}


QLineEdit#Help_Search {
    background-color: rgba(255, 255, 255);
}







QCalendarWidget QWidget{
	alternate-background-color: rgb(74, 222, 252);
}

QCalendarWidget QAbstractItemView {
    background-color: #ffffff;
    color: black;
    selection-background-color: #4f95ff;
    selection-color: white;
    gridline-color: #4f95ff;
}

QCalendarWidget QToolButton {
    color: rgb(46, 45, 45);
    background: rgb(79, 149, 255);
	border: 2px solid #4f95ff;
    border-radius: 6px;
}

QCalendarWidget QToolButton:hover {
    background: rgb(199, 199, 199);
}

QCalendarWidget QAbstractItemView {
    selection-background-color: #3daee9;
    selection-color: black;
}

QCalendarWidget QAbstractItemView::item:disabled {
    color: white;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(79, 149, 255) ;
}

QCalendarWidget QToolButton QMenu {
     background-color: rgb(79, 149, 255);
     color: black
}




QLabel#Ecampus{
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QTableView {
    background-color: rgba(255, 255, 255, 0);
}

QPushButton#Exit_Button {
    border: 2px solid #ffffff;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}





QPushButton#Exit_Button1 {
    border: 2px solid #ffffff;
    border-radius: 6px;
    background-color: rgb(243, 70, 70);
    color: white;
}
"""

# =========================
# UI LOADER
# =========================

def load_ui(path: str):
    loader = QUiLoader()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    ui_path = os.path.join(base_dir, path)

    ui_file = QFile(ui_path)
    if not ui_file.open(QFile.ReadOnly):
        print(f"CRITICAL ERROR: Could not find or open UI file at: {ui_path}")
        print(f"Qt Error: {ui_file.errorString()}")
        sys.exit(-1)
    
    window = loader.load(ui_file)
    ui_file.close()
    return window


# =========================
# THEME HANDLING
# =========================

def change_theme(app: QApplication, theme: str):
    if theme == "Dark Theme":
        app.setStyleSheet(DARK_THEME)
    elif theme == "Light Theme":
        app.setStyleSheet(LIGHT_THEME)


# =========================
# WINDOW SWITCH
# =========================


def open_courses(menu_window):
    courses_window = load_ui("courses.ui")

    # кнопка выхода обратно в menu
    exit_button = courses_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(courses_window)
    )

    courses_window.show()
    menu_window.close()

    menu_window.courses_window = courses_window

def open_calendar(menu_window):
    calendar_window = load_ui("calendar.ui")

    # кнопка выхода обратно в menu
    exit_button = calendar_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(calendar_window)
    )

    calendar_window.show()
    menu_window.close()

    menu_window.courses_window = calendar_window

def open_StudIP(menu_window):
    StudIP_window = load_ui("StudIP.ui")

    # кнопка выхода обратно в menu
    exit_button = StudIP_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(StudIP_window)
    )

    StudIP_window.show()
    menu_window.close()

    menu_window.courses_window = StudIP_window

def open_Email(menu_window):
    Email_window = load_ui("Email.ui")

    # кнопка выхода обратно в menu
    exit_button = Email_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(Email_window)
    )

    Email_window.show()
    menu_window.close()

    menu_window.courses_window = Email_window

def open_Dashboard(menu_window):
    Dashboard_window = load_ui("Dashboard.ui")

    # кнопка выхода обратно в menu
    exit_button = Dashboard_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(Dashboard_window)
    )

    Dashboard_window.show()
    menu_window.close()

    menu_window.courses_window = Dashboard_window

def open_Notes(menu_window):
    Notes_window = load_ui("notes.ui")

    # кнопка выхода обратно в menu
    exit_button = Notes_window.findChild(QPushButton, "Exit_Button1")
    exit_button.clicked.connect(
        lambda: open_menu(Notes_window)
    )

    Notes_window.show()
    menu_window.close()

    menu_window.courses_window = Notes_window

def open_Help(main_window):
    Help_window = load_ui("help.ui")

    textBrowser = Help_window.findChild(QTextBrowser, "textBrowser")

    exit_button = Help_window.findChild(QPushButton, "Back_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(Help_window)
    )
    FAQ_button = Help_window.findChild(QPushButton, "FAQ")
    FAQ_button.clicked.connect(
        lambda: textBrowser.setText("What is this app for? \n- This app is designed to help students during their university studies.\nIs my personal data saved?\n- No, the app does not store any user personal data.\nHow can I change my password?\n- After logging into my account, go to the Account Settings tab.")
    )
    Instructions_button = Help_window.findChild(QPushButton, "Instruction")
    Instructions_button.clicked.connect(
        lambda: textBrowser.setText("Информация")
    )
    Support_button = Help_window.findChild(QPushButton, "Support")
    Support_button.clicked.connect(
        lambda: textBrowser.setText("Информация")
    )
    App_button = Help_window.findChild(QPushButton, "App")
    App_button.clicked.connect(
        lambda: textBrowser.setText("The Idea: Dmytro Kutsak.\nDesigned by: Nichita Licov and Diana Bardyk ")
    )

    Help_window.show()
    main_window.close()

    main_window.courses_window = Help_window

def open_menu(main_window):
    menu_window = load_ui("menu.ui")
    with ThreadPoolExecutor(max_workers=2) as executor:
        mail_notifications = menu_window.findChild(QLabel,"Ecampus_Mail")
        executor.submit(mail_notifications.setText(f"ECampus Mail ({simargl.mail_notifications(mail)})"), 1)
        message_notifications = menu_window.findChild(QLabel,"StudIP_Messages")
        executor.submit(message_notifications.setText(f"StudIP ({len(simargl.get_my_messages(client)[1])})"), 2)

    courses_button = menu_window.findChild(QPushButton, "Courses")
    courses_button.clicked.connect(
        lambda: open_courses(menu_window)
    )
    calendar_button = menu_window.findChild(QPushButton, "Calendar")
    calendar_button.clicked.connect(
        lambda: open_calendar(menu_window)
    )
    StudIP_button = menu_window.findChild(QPushButton, "Messages")
    StudIP_button.clicked.connect(
        lambda: open_StudIP(menu_window)
    )
    Email_button = menu_window.findChild(QPushButton, "Email")
    Email_button.clicked.connect(
        lambda: open_Email(menu_window)
    )
    Dashboard_button = menu_window.findChild(QPushButton, "Dashboard")
    Dashboard_button.clicked.connect(
        lambda: open_Dashboard(menu_window)
    )
    Notes_button = menu_window.findChild(QPushButton, "Notes")
    Notes_button.clicked.connect(
        lambda: open_Notes(menu_window)
    )
    exit_button = menu_window.findChild(QPushButton, "Exit_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(menu_window)
    )


    menu_window.show()
    main_window.close()

    main_window.menu_window = menu_window




def back_to_main(menu_window):
    main_window = load_ui("main.ui")

    # theme combobox
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(QApplication.instance(), text)
    )

    # установить тему при запуске
    change_theme(QApplication.instance(), theme_box.currentText())

    # кнопка Enter снова ведёт в menu
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )

    main_window.show()
    menu_window.close()


def error_login(menu_window):
    error_window = load_ui("error.ui")

    # кнопка выхода обратно в menu
    exit_button = error_window.findChild(QPushButton, "Error_Button")
    exit_button.clicked.connect(
        lambda: back_to_main(error_window)
    )

    error_window.show()
    menu_window.close()

    menu_window.courses_window = error_window


def login_from_enter(main_window):
    global client, mail, server
    login_box = main_window.findChild(QLineEdit, "LoginLine")
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    login = login_box.text()
    password = password_box.text()

    try:
        client = simargl.create_client(login,password,simargl.BASE_URL)
        mail = simargl.read_email_init(simargl.SERVER,str("ug-student\\"+login),password)
        server = simargl.write_email_init(simargl.SERVER,str("ug-student\\"+login),password)
    except:
        error_login(main_window)
    else:
        open_menu(main_window)


# =========================
# MAIN
# =========================

def main():
    app = QApplication(sys.argv)

    # --- load main window ---
    main_window = load_ui("main.ui")

    # --- theme combobox ---
    theme_box = main_window.findChild(QComboBox, "ThemeBox")
    theme_box.currentTextChanged.connect(
        lambda text: change_theme(app, text)
    )

    # --- setting theme on the start ---
    change_theme(app, theme_box.currentText())

    # --- enter button ---
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: login_from_enter(main_window)
    )

    help_button = main_window.findChild(QPushButton, "Help")
    help_button.clicked.connect(
        lambda: open_Help(main_window)
    )

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()