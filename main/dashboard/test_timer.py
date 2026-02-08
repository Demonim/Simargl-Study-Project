import sys
import os
from PySide6.QtWidgets import QApplication
import pyqtgraph as pg
from main.dashboard.timer_bar.weekly_study_tracker import WeeklyStudyTracker
from main.dashboard.timer_bar.study_timer import Study_Timer
from main.dashboard.timer_bar.create_bar import create_stacked_bar, update_stacked_bar


def main():
    login = input('Enter your login: ')
    password = input('Enter your password: ')

    app = QApplication(sys.argv)
    
    user_filename = f"storage/{login}_study_data.json"
    tracker = WeeklyStudyTracker(filename=user_filename) 
    timer = Study_Timer()
    
    # вікно графіка
    plot_widget = create_stacked_bar(tracker.all())
    plot_widget.setWindowTitle(f"Simargl Study Tracker - {login}")
    plot_widget.resize(800, 600)
    plot_widget.show()

    print("1 (Manual), 2 (Timer), 3 (Reset), 4 (Exit)")

    while True:
        app.processEvents() 
        choice = input("\nChoice: ")

        if choice == '1':
            day = input("Day (Mon-Sun): ").capitalize()[:3]
            try:
                h = float(input("Hours: "))
                m = float(input("Minutes: "))
                tracker.set_day(day, h + (m/60))
            except ValueError: 
                print("Error")
            
        elif choice == '2':
            day = input("Day for timer: ").capitalize()[:3]
            input("Enter to START")
            timer.start()
            print("Enter to STOP")
            input()
            timer.stop()
            tracker.add_time(day, timer.hours())
            timer.reset()
            
        elif choice == '3':
            confirm = input("Clear all data for this user? (y/n): ")
            if confirm.lower() == 'y': tracker.reset_all()
            
        elif choice == '4':
            break


        update_stacked_bar(plot_widget, tracker.all())
        
        print(f"Data saved to {user_filename}")

    sys.exit(0)

if __name__ == "__main__":
    main()