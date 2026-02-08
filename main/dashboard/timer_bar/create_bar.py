import pyqtgraph as pg
import numpy as np

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [f"{int(v)}:{int((v % 1) * 60):02d}" for v in values]

def create_stacked_bar(study_data):

    plot = pg.PlotWidget(axisItems={'left': TimeAxisItem(orientation='left')})
    plot.setBackground("w")
    plot.addLegend()

    days = list(study_data.keys())
    x = np.arange(len(days))

    manual = [study_data[d]["manual"] for d in days]
    timer  = [study_data[d]["timer"]  for d in days]

    y_axis = plot.getAxis("left")
    y_axis.enableAutoSIPrefix(False) 
    

    total_hours_per_day = [m + t for m, t in zip(manual, timer)]
    max_val = max(total_hours_per_day) if any(total_hours_per_day) else 0

    if max_val <= 10:
        plot.setYRange(0, 10, padding=0.02) 
    else:
        plot.setYRange(0, max_val, padding=0.05)
    
    plot.enableAutoRange(axis='y', enable=False)

    bar_width = 0.6
    manual_bar = pg.BarGraphItem(
        x=x, height=manual, width=bar_width, 
        brush="skyblue", name="Manual"
    )
    
    timer_bar = pg.BarGraphItem(
        x=x, height=timer, width=bar_width, 
        brush="orange", y0=manual, name="Timer"
    )

    plot.addItem(manual_bar)
    plot.addItem(timer_bar)

    plot.getAxis("bottom").setTicks([list(enumerate(days))])
    plot.setLabel("left", "Study Time", units="HH:MM")

    return plot

def update_stacked_bar(plot_widget, study_data):
    """Оновлює дані в уже існуючому графіку"""
    plot_widget.clear()

    days = list(study_data.keys())
    x = np.arange(len(days))
    manual = [study_data[d]["manual"] for d in days]
    timer  = [study_data[d]["timer"]  for d in days]

    total_hours_per_day = [m + t for m, t in zip(manual, timer)]
    max_val = max(total_hours_per_day) if any(total_hours_per_day) else 0
    
    if max_val<=10:
        plot_widget.setYRange(0, 10, padding=0.02)
    else:
        plot_widget.setYRange(0, max_val, padding=0.05)

    bar_width = 0.6
    manual_bar = pg.BarGraphItem(x=x, height=manual, width=bar_width, brush="skyblue", name="Manual")
    timer_bar = pg.BarGraphItem(x=x, height=timer, width=bar_width, brush="orange", y0=manual, name="Timer")

    plot_widget.addItem(manual_bar)
    plot_widget.addItem(timer_bar)