import sys
import matplotlib.pyplot as plt
from main.dashboard.timer_bar.weekly_study_tracker import WeeklyStudyTracker
from main.dashboard.timer_bar.study_timer import Study_Timer
from main.dashboard.timer_bar.create_bar import create_stacked_bar, update_stacked_bar, show_chart
import main.dashboard.timer_bar.tracker_controller as actions

def main():
    login = input('Login: ')
    tracker = WeeklyStudyTracker(filename=f"storage/{login}_study_data.json") 
    timer = Study_Timer()
    
    plt.ion()
    fig = create_stacked_bar(tracker.all())
    show_chart(fig, title=f"Tracker: {login}")

    while True:
        plt.pause(0.1)
        cmd = input("\n1-Manual, 2-Timer, 3-Reset, 4-Exit: ")

        if cmd == '1':
            d = input("Day: ").capitalize()[:3]
            if actions.manual_entry(tracker, d, input("H: "), input("M: ")):
                update_stacked_bar(fig, tracker.all())

        elif cmd == '2':
            input("Enter to Start")
            timer.start()
            
            input("Enter to Stop")
            
            recorded_day = actions.stop_timer(tracker, timer)
            
            update_stacked_bar(fig, tracker.all())
            print("Done")

        elif cmd == '3':
            if input("Reset? (y/n): ").lower() == 'y':
                actions.reset_data(tracker)
                update_stacked_bar(fig, tracker.all())

        elif cmd == '4':
            break

    sys.exit(0)

if __name__ == "__main__":
    main()