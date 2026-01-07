import sys
import os
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QPushButton, 
    QLabel,
    QLineEdit
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
#import simargl

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
    font-size: 18pt;
}

QLineEdit {
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
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 18pt;
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

def open_menu(main_window):
    """login_box = main_window.findChild(QLineEdit, "LoginLine")
    login = login_box.text()
    password_box = main_window.findChild(QLineEdit, "PasswordLine")
    password = password_box.text()

    try:
        client = simargl.create_client(login,password,simargl.base_url)
        mail = simargl.read_email_init(simargl.SERVER,str("ug-student\\"+login),password)
        server = simargl.write_email_init(simargl.SERVER,str("ug-student\\"+login),password)
    except:
        raiseError("Credentials are not correct!") """

    menu_window = load_ui("menu.ui")
    menu_window.show()
    main_window.close()

    # важно сохранить ссылку
    main_window.menu_window = menu_window


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

    # применяем тему при старте
    change_theme(app, theme_box.currentText())

    # --- enter button ---
    enter_button = main_window.findChild(QPushButton, "Enter")
    enter_button.clicked.connect(
        lambda: open_menu(main_window)
    )

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()