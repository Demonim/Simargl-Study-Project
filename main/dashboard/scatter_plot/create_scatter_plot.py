from matplotlib.figure import Figure


def generate_scatter_figure(df, medians, math_stats, color='black'):
    """
    High-level function to prepare data and generate a scatter plot of course activity.
   
    This function processes course metrics and maps them onto a theme-adaptive
    intensity matrix. It visualizes the relationship between study hours and
    communication levels using a quadrant-based analysis.


    Args:
        df (DataFrame): Processed data containing hours, messages, quadrants,
                        and engagement scores for each course.
        medians (tuple): Calculated median values (med_x, med_y) used to
                         center the quadrant grid.
        math_stats (dict): Dictionary containing mathematical insights like
                           Mean Ratio (mu) and Standard Deviation (sigma).
        color (str): Theme-compliant color for text, labels, and plot boundaries.


    Returns:
        Figure: A Matplotlib Figure object representing the scatter plot,
                complete with interactive tooltips and statistical footer.
    """

    required_columns = {'name', 'hours', 'messages', 'insight', 'engagement_score', 'quadrant'}
    if df is None or not hasattr(df, 'empty') or df.empty or not required_columns.issubset(df.columns):
        fig = Figure(figsize=(8, 6), tight_layout=True)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, 'No valid data for scatter plot', ha='center', va='center', color=color)
        return fig

    try:
        med_x, med_y = medians
        mu = math_stats.get('mean_ratio', 0)
        sigma = math_stats.get('std_dev', 0)
        fig = Figure(figsize=(10, 8), facecolor='none')
        ax = fig.add_subplot(111)
        ax.set_facecolor('none')

        quadrant_colors = {
            "Active Ecosystem": "#FF6B81",
            "Live Discussion": "#6AB04C",  
            "Routine Lectures": "#4834D4",
            "Inactive Course": "#F0932B",  
        }

        scatters = []
        for q_type, q_color in quadrant_colors.items():
            sub = df[df['quadrant'] == q_type]
            if not sub.empty:
                point_sizes = 150 + (sub['engagement_score'] * 80).clip(-100, 300)
                sc = ax.scatter(sub['hours'], sub['messages'], c=q_color, s=point_sizes,
                               label=q_type, edgecolors='white', linewidth=0.6, alpha=0.9, zorder=3)
               
                sc.course_data = sub[['name', 'hours', 'messages', 'insight', 'engagement_score']].values
                scatters.append(sc)

        ax.axhline(y=med_y, color=color, linestyle='--', alpha=0.6, zorder=1)
        ax.axvline(x=med_x, color=color, linestyle='--', alpha=0.6, zorder=1)

        for spine in ax.spines.values():
            spine.set_edgecolor(color)

        annot = ax.annotate("", xy=(0,0), xytext=(10, 10),
                            textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.5", fc="#333333", ec="white", lw=1),
                            color="white", fontsize=9, fontweight='bold', zorder=10)
        annot.set_visible(False)
    except Exception as e:
        fig = Figure(figsize=(8, 6), tight_layout=True)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, f'Error in scatter plot: {str(e)}', ha='center', va='center', color=color)
        return fig

    def update_annot(sc, ind):
        """
        Internal event handler to update the tooltip's content and visual positioning.
       
        Args:
            sc (PathCollection): The scatter plot object being hovered over.
            ind (dict): Dictionary containing the index of the specific point
                        intersected by the mouse cursor.
        """
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
       
        name, hrs, msg, insight, score = sc.course_data[ind["ind"][0]]
        text = (f"{name}\n"
                f"───────────────────\n"
                f"Time: {hrs:.1f}h | Msg: {int(msg)}\n"
                f"Score: {score:+.1f} ({insight})")
       
        annot.set_text(text)
       
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
       
        if pos[0] > (xlim[0] + xlim[1]) / 2:
            offset_x = -15  
            annot.set_ha('right')
        else:
            offset_x = 15  
            annot.set_ha('left')

        if pos[1] > ylim[1] * 0.8:
            offset_y = -50  
        else:
            offset_y = 10  

        annot.set_position((offset_x, offset_y))

    def hover(event):
        """
        Main event listener to manage the interactive lifecycle of tooltips.
       
        Args:
            event (MouseEvent): The Matplotlib event object containing mouse
                                coordinates and axis information.
        """

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

    stats_text = (
        f"Sector Centers: {med_x:.1f}h / {med_y:.1f} msg. "
        f"Math metrics: Mean Ratio = {mu:.2f}, Std Deviation = {sigma:.2f}.\n"
        f"Score: Relative intensity (Z-score). Calculated as (Ratio - Mean Ratio) / Std Deviation. "
        f"Bubble size reflects this intensity."
    )

    fig.text(0.05, 0.02, stats_text, color=color, fontsize=8, style='italic', wrap=True)

    ax.text(ax.get_xlim()[1]*0.7, ax.get_ylim()[1]*0.9, 'ECOSYSTEMS',
            color='#FF6B81', alpha=0.3, fontsize=12, fontweight='bold')
    discussions_x = ax.get_xlim()[0] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.07
    ax.text(discussions_x, ax.get_ylim()[1]*0.9, 'DISCUSSIONS',
            color='#6AB04C', alpha=0.3, fontsize=12, fontweight='bold')

    ax.set_title('Study Intensity Matrix (Hours vs Messages)', color=color, fontsize=14, pad=5)
    ax.set_xlabel('Study Hours', color=color)
    ax.set_ylabel('Interaction Level (Messages)', color=color)
    ax.tick_params(colors=color)
   
    legend = ax.legend(
        loc='lower right',
        facecolor='none',
        edgecolor=color,
        labelcolor=color,
        fontsize=9,
        scatterpoints=1
    )

    for handle in legend.legend_handles:
        handle.set_sizes([100.0])

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2)
   
    return fig