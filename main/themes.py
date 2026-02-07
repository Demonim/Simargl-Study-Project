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






/* === Main.ui === */
QLabel#Ecampus{
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QLabel#Login, QLabel#Password{
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

QLineEdit#PasswordLine, #LoginLine {
    background-color: 255, 255, 255
}

QCheckBox#Check_Remember {
    color: rgb(102, 255, 140);
    background-color: rgb(255, 255, 255, 0);
    font-size: 10pt
}

QPushButton {
    border: 2px solid #00ff88;
    border-radius: 6px;
    background-color: black;
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
    background-color: rgb(23, 130, 22);
    border: 2px solid #000000;
    border-radius: 6px;
    color: rgb(0, 0, 0);
    font-size: 15pt;
}

QPushButton#Help:hover{
    border: 2px solid rgb(145, 207, 111);
    border-radius: 6px;
    background-color: rgb(22, 107, 31);
	color: rgb(145, 207, 111);
	font-size: 15pt;
}

QWidget#CourseItem {
    background-color: rgb(40, 112, 42); 
    border-radius: 5px;
}





/* === Error Window === */
QLabel#Error, QLabel#Error_2 {
	color: rgb(255, 255, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 14pt;
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






/* === Help Window === */
QLabel#Help {
    color: rgb(102, 255, 140);
    background-color: rgba(255, 255, 255, 0);
    font-size: 30pt;
}

QTextBrowser {
    color: rgb(102, 255, 140);
    border: 10px solid rgb(102, 255, 140);
    background-color: rgb(0, 0, 0);
    font: 15pt;
}






/* === Menu Window === */
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

QTableView {
    background-color: rgba(255, 255, 255, 0);
}


/* === Courses Window === */
QTableWidget#Table{
    background-color: black;
    color: rgb(102, 255, 140);
    gridline-color: rgb(102, 255, 140);
    font-size: 10pt;
    border: 4px solid green; border-radius: 5px
}

QHeaderView::section {
    background-color: #02070f;
    color: #00ff88;
    padding: 8px;
    border: 1px solid #00ff88;
    font-weight: bold;
}


/* === Calendar Window === */
QWidget#Calenadar{
    background-color: rgba(0, 0, 0, 200)
}


/* === Notes Window === */
QListWidget#NotesList{
    background-color: rgb(0, 0, 0);
    color: rgb(102, 255, 140);
    font-size: 14pt;

}

QTextEdit#NotesText{
    background-color: rgb(0, 0, 0);
    color: rgb(102, 255, 140);
    font-size: 14pt;
    border: 5px solid green; border-radius: 5px
}


/* === Dashboard Window === */
QLabel#Dashboard {
    font-size: 24pt;
}

QWidget#Dashboard_1, #Dashboard_2, #Dashboard_3{
    background-color: rgb(0, 0, 0);
    border: 2px solid green; border-radius: 5px
}

QLineEdit{
    background-color: rgb(0, 0, 0);
    border: 2px solid green; border-radius: 5px
}
"""

DARK_Minimalistic = """
/* === GLOBAL SETTINGS === */
QWidget {
    background-color: rgb(18, 18, 18);
    color: rgb(225, 225, 225);
    font-family: Unispace;
    selection-background-color: rgb(70, 70, 70);
    selection-color: white;
}



/* === Main.ui === */
QLabel {
    color: rgb(225, 225, 225);
    background-color: transparent;
    font-size: 16pt;
}

QLabel#Ecampus {
    color: white;
    font-size: 40pt;
    font-weight: bold;
}

QLabel#Login,#Password,#Name_label {
    color: rgb(180, 180, 180);
    font-size: 14pt;
}

QLineEdit {
    background-color: rgb(30, 30, 30);
    color: white;
    border: 1px solid rgb(60, 60, 60);
    border-radius: 4px;
    padding: 5px;
    font-size: 12pt;
    border: 2px solid white;
}

QLineEdit:focus {
    border: 1px solid rgb(150, 150, 150);
}

QCheckBox {
    color: rgb(180, 180, 180);
    spacing: 5px;
}

QComboBox#ThemeBox {
    background-color: black;
    color: white;      
    border: 2px solid white;
    padding: 5px;
}


QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: rgb(30, 30, 30);
    border: 1px solid rgb(80, 80, 80);
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: rgb(150, 150, 150);
    border: 1px solid rgb(200, 200, 200);
}



/* === Buttons === */
QPushButton {
    background-color: rgb(30, 30, 30);
    border: 1px solid rgb(60, 60, 60);
    border-radius: 6px;
    color: rgb(225, 225, 225);
    padding: 6px;
    font-size: 13pt;
    border: 2px solid white;

}

QPushButton:hover {
    background-color: rgb(50, 50, 50);
    border: 1px solid rgb(100, 100, 100);
    color: white;
}

QPushButton:pressed {
    background-color: rgb(70, 70, 70);
}



/* === Error Window === */
QLabel#Error,QLabel#Error_2 {
    color: rgb(255, 80, 80);
    font-size: 14pt;
}

QPushButton#Error_Button {
    background-color: rgb(30, 30, 30);
    border: 1px solid rgb(80, 80, 80);
    color: white;
}



/* === Help Window === */
QLabel#Help {
    font-size: 30pt;
}

QTextBrowser {
    background-color: rgb(25, 25, 25);
    border: 1px solid rgb(50, 50, 50);
    color: rgb(220, 220, 220);
    font-size: 14pt;
}


/* === Menu Window === */
QCalendarWidget QWidget {
    background-color: rgb(25, 25, 25);
    alternate-background-color: rgb(30, 30, 30);
    color: white;
}

QCalendarWidget QToolButton {
    color: white;
    background-color: rgb(35, 35, 35);
    border: none;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(30, 30, 30);
}

QCalendarWidget QAbstractItemView {
    background-color: rgb(25, 25, 25);
    color: white;
    selection-background-color: rgb(60, 60, 60);
    selection-color: white;
}



/* === Tables / Lists === */
QTableWidget,QListWidget,QTextEdit {
    background-color: rgb(25, 25, 25);
    border: 1px solid rgb(50, 50, 50);
    color: rgb(220, 220, 220);
    border-radius: 4px;
}

QHeaderView::section {
    background-color: rgb(35, 35, 35);
    color: white;
    padding: 6px;
    border: 1px solid rgb(50, 50, 50);
}

/* === Notes Window === */
QListWidget#NotesList{
    background-color: rgb(0, 0, 0);
    color: white;
    font-size: 15pt;

}

QTextEdit#NotesText{
    background-color: rgb(0,0,0);
    color: white;
    font-size: 15pt;
}

/* === Dashboard === */
QLabel#Dashboard {
    font-size: 24pt;
}

QWidget#Dashboard_1,#Dashboard_2,#Dashboard_3 {
    background-color: rgb(25, 25, 25);
    border: 1px solid rgb(50, 50, 50);
    border-radius: 5px;

QLineEdit{
    background-color: rgb(255, 255, 255);
    border: 2px solid black; border-radius: 5px
}
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







/* === Main.ui === */
QLabel#Ecampus{
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 40pt;
}

QLabel#Login, QLabel#Password{
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

QLineEdit#PasswordLine {
    background-color: 255, 255, 255
}

QLineEdit#LoginLine {
    background-color: 255, 255, 255
}

QCheckBox#Check_Remember {
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
	border: 2px solid rgb(63, 72, 204);
    border-radius: 6px;
    background-color: rgb(0, 167, 240);
	color: rgb(63, 72, 204);
	font-size: 15pt;
}

QPushButton#Help:hover{
    border: 2px solid rgb(0,0,0);
    border-radius: 6px;
    background-color: rgb(20,111,161);
	color: rgb(79, 149, 255);
	font-size: 15pt;
}

QWidget#CourseItem {
    background-color: rgb(64, 50, 195); 
    border-radius: 5px;
}





/* === Error Window === */
QLabel#Error, QLabel#Error_2 {
	color: rgb(0, 0, 0);
    background-color: rgba(255, 255, 255, 0);
    font-size: 14pt;
}

QPushButton#Error_Button {
    border: 2px solid #000000;
    border-radius: 6px;
    background-color: transparent;
    color: rgb(0, 0, 0);
    font-size: 15pt;
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






/* === Help Window === */
QLabel#Help {
    color: rgb(79, 149, 255);
    background-color: rgba(255, 255, 255, 0);
    font-size: 30pt;
}

QTextBrowser {
    color: rgb(79, 149, 255);
    border: 10px solid rgb(102, 255, 140);
    background-color: rgb(255, 255, 255);
    font: 15pt;
}






/* === Menu Window === */
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

QTableView {
    background-color: rgba(255, 255, 255, 0);
}


/* === Courses Window === */
QTableWidget#Table{
    background-color: white;
    color: rgb(79, 149, 255);
    gridline-color: rgb(79, 149, 255);
    font-size: 10pt;
    border: 4px solid blue; border-radius: 5px
}

QHeaderView::section {
    background-color: rgb(249,243,246);
    color: rgb(79, 149, 255);
    padding: 8px;
    border: 1px solid rgb(79, 149, 255);
    font-weight: bold;
}



/* === Notes Window === */
QListWidget#NotesList{
    background-color: rgb(255, 255, 255);
    color: rgb(79, 149, 255);
    font-size: 14pt;
    border: 5px solid blue; border-radius: 5px

}

QTextEdit#NotesText{
    background-color: rgb(255, 255, 255);
    color: rgb(79, 149, 255);
    font-size: 14pt;
    border: 5px solid blue; border-radius: 5px
}

/* === StudIP Window === */
QTextEdit#bodyText{
    color: rgb(0, 0, 0);
}


/* === Dashboard Window === */
QLabel#Dashboard {
    font-size: 24pt;
}

QWidget#Dashboard_1, #Dashboard_2, #Dashboard_3{
    background-color: rgb(255, 255, 255);
    border: 2px solid blue; border-radius: 5px
}

QLineEdit{
    background-color: rgb(255, 255, 255);
    border: 2px solid blue; border-radius: 5px
}
"""

LIGHT_Minimalistic = """
/* === GLOBAL SETTINGS === */
QWidget {
    background-color: rgb(248, 249, 250);
    color: rgb(33, 37, 41);
    font-family: Unispace;
    selection-background-color: rgb(200, 200, 200);
    selection-color: black;
}



/* === Main.ui === */
QLabel {
    color: rgb(33, 37, 41);
    background-color: transparent;
    font-size: 16pt;
}

QLabel#Ecampus {
    color: rgb(33, 37, 41);
    font-size: 40pt;
    font-weight: bold;
}

QLabel#Login,#Password,#Name_label {
    color: rgb(108, 117, 125);
    font-size: 14pt;
}

QLineEdit {
    background-color: rgb(255, 255, 255);
    color: rgb(33, 37, 41);
    border: 1px solid rgb(206, 212, 218);
    border-radius: 4px;
    padding: 5px;
    font-size: 12pt;
    border: 2px solid black;
}

QLineEdit:focus {
    border: 1px solid rgb(100, 100, 100);
}

QCheckBox {
    color: rgb(108, 117, 125);
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(180, 180, 180);
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: rgb(230, 230, 230);
    border: 1px solid rgb(150, 150, 150);
}

QComboBox#ThemeBox {
    background-color: white;
    color: black;      
    border: 2px solid black;
    padding: 5px;
}



/* === Buttons === */
QPushButton {
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(206, 212, 218);
    border-radius: 6px;
    color: rgb(33, 37, 41);
    padding: 6px;
    font-size: 13pt;
    border: 2px solid black;
}

QPushButton:hover {
    background-color: rgb(233, 236, 239);
    border: 1px solid rgb(180, 180, 180);
}

QPushButton:pressed {
    background-color: rgb(210, 210, 210);
}



/* === Error Window === */
QLabel#Error,QLabel#Error_2 {
    color: rgb(220, 53, 69);
    font-size: 14pt;
}

QPushButton#Error_Button {
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(180, 180, 180);
    color: black;
}



/* === Help Window === */
QLabel#Help {
    font-size: 30pt;
}

QTextBrowser {
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(206, 212, 218);
    color: rgb(33, 37, 41);
    font-size: 15pt;
}



/* === Menu Window === */
QCalendarWidget QWidget {
    background-color: rgb(255, 255, 255);
    alternate-background-color: rgb(245, 245, 245);
    color: black;
}

QCalendarWidget QToolButton {
    color: black;
    background-color: rgb(240, 240, 240);
    border: none;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(240, 240, 240);
}

QCalendarWidget QAbstractItemView {
    background-color: rgb(255, 255, 255);
    color: black;
    selection-background-color: rgb(220, 220, 220);
    selection-color: black;
}



/* === Tables / Lists === */
QTableWidget,QListWidget,QTextEdit {
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(206, 212, 218);
    color: rgb(33, 37, 41);
    border-radius: 4px;
}

QHeaderView::section {
    background-color: rgb(240, 240, 240);
    color: rgb(33, 37, 41);
    padding: 6px;
    border: 1px solid rgb(200, 200, 200);
}

/* === Notes Window === */
QListWidget#NotesList{
    background-color: rgb(255, 255, 255);
    color: rgb(33, 37, 41);
    font-size: 15pt;

}

QTextEdit#NotesText{
    background-color: rgb(255, 255, 255);
    color: rgb(33, 37, 41);
    font-size: 15pt;
}

/* === Dashboard === */
QLabel#Dashboard {
    font-size: 24pt;
}

QWidget#Dashboard_1,#Dashboard_2,#Dashboard_3 {
    background-color: rgb(255, 255, 255);
    border: 1px solid rgb(206, 212, 218);
    border-radius: 5px;

QLineEdit{
    background-color: rgb(0, 0, 0);
    border: 2px solid black; border-radius: 5px
}
}
"""