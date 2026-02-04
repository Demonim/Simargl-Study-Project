import pyqtgraph as pg
import numpy as np

#stacked diagram for manual+timer data
def create_stacked_bar(study_data):

    plot = pg.PlotWidget()
    plot.setBackground("w")
    plot.addLegend()

    days = list(study_data.keys())
    x = np.arange(len(days))

    manual = [study_data[d]["manual"] for d in days]
    timer  = [study_data[d]["timer"]  for d in days]

    bar_width = 0.6

    manual_bar = pg.BarGraphItem(
        x=x,
        height=manual,
        width=bar_width,
        brush="skyblue",
        name="Manual"
    )

    timer_bar = pg.BarGraphItem(
        x=x,
        height=timer,
        width=bar_width,
        brush="orange",
        x0=x,
        y0=manual,  
        name="Timer"
    )

    plot.addItem(manual_bar)
    plot.addItem(timer_bar)

    plot.getAxis("bottom").setTicks([list(enumerate(days))])
    plot.setLabel("left", "Hours")

    return plot
