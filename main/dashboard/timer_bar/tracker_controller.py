from datetime import datetime

def manual_entry(tracker, day, h, m):
    try:
        tracker.set_day(day, float(h) + (float(m)/60))
        return True
    except:
        return False

def stop_timer(tracker, timer):
    current_day = datetime.now().strftime('%a') 
    
    timer.stop()
    tracker.add_time(current_day, timer.hours())
    timer.reset()
    return current_day 

def reset_data(tracker):
    tracker.reset_all()