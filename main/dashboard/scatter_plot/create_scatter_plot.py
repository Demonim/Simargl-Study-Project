import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def generate_scatter_figure(df, medians, excluded=None):

    med_x, med_y = medians
    fig = Figure(figsize=(10, 8), facecolor='#121212')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#121212')

    colors = {
        "Active Ecosystem": "#FF6B81",
        "Live Discussion": "#6AB04C",  
        "Routine Lectures": "#4834D4",
        "Inactive Course": "#F0932B",  
    }

    scatters = []
    for q_type, color in colors.items():
        sub = df[df['quadrant'] == q_type]
        if not sub.empty:
            point_sizes = 150 + (sub['engagement_score'] * 80).clip(-100, 300)
            sc = ax.scatter(sub['hours'], sub['messages'], c=color, s=point_sizes,
                           label=q_type, edgecolors='white', linewidth=0.6, alpha=0.9, zorder=3)
           
            sc.course_data = sub[['name', 'hours', 'messages', 'insight', 'engagement_score']].values
            scatters.append(sc)

    ax.axhline(y=med_y, color='#555555', linestyle='--', alpha=0.6, zorder=1)
    ax.axvline(x=med_x, color='#555555', linestyle='--', alpha=0.6, zorder=1)

    annot = ax.annotate("", xy=(0,0), xytext=(10, 10),
                        textcoords="offset points",
                        bbox=dict(boxstyle="round,pad=0.5", fc="#333333", ec="white", lw=1),
                        color="white", fontsize=9, fontweight='bold', zorder=10)
    annot.set_visible(False)

    def update_annot(sc, ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
       
        name, hrs, msg, insight, score = sc.course_data[ind["ind"][0]]
        text = (f"{name}\n"
                f"───────────────────\n"
                f"Time: {hrs:.1f}h | Msg: {int(msg)}\n"
                f"Score: {score:+.1f} ({insight})")
       
        annot.set_text(text)
    
        xlim = ax.get_xlim()
        if pos[0] > (xlim[0] + xlim[1]) / 2:
            annot.set_ha('right')
            annot.set_position((-15, 10))
        else:
            annot.set_ha('left')
            annot.set_position((15, 10))

    def hover(event):
        if event.inaxes == ax:
            for sc in scatters:
                cont, ind = sc.contains(event)
                if cont:
                    update_annot(sc, ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                    return
        if annot.get_visible():
            annot.set_visible(False)
            fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    ax.text(ax.get_xlim()[1]*0.7, ax.get_ylim()[1]*0.9, 'ECOSYSTEMS',
            color='#FF6B81', alpha=0.3, fontsize=12, fontweight='bold')
    ax.text(ax.get_xlim()[0], ax.get_ylim()[1]*0.9, 'DISCUSSIONS',
            color='#6AB04C', alpha=0.3, fontsize=12, fontweight='bold')

    ax.set_title('Study Intensity Matrix (Hours vs Messages)', color='white', fontsize=14, pad=15)
    ax.set_xlabel('Study Hours', color='#AAAAAA')
    ax.set_ylabel('Interaction Level (Messages)', color='#AAAAAA')
    ax.tick_params(colors='#888888')
   
    legend = ax.legend(
        loc='lower right', 
        facecolor='#1e1e1e', 
        edgecolor='#444444', 
        labelcolor='white', 
        fontsize=9,
        scatterpoints=1 
    )

    for handle in legend.legend_handles:
        handle.set_sizes([100.0])

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.15)
   
    return fig