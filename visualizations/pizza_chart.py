import streamlit as st
from mplsoccer import PyPizza
from matplotlib.patches import Patch,Circle
import matplotlib.pyplot as plt
from utilities.utils import get_metrics_by_position
from utilities.utils import get_player_metrics_percentile_ranks
from utilities.utils import custom_fontt


def create_pizza_chart(complete_data,league_name,season, player_name, position, api="statbomb"):

    position_specific_metric = get_metrics_by_position(position, api)

    if position == 'Number 6' and api=='statbomb':
        position = 'Number 8'

    if league_name not in ['All', '']:
        complete_data = complete_data[complete_data['League'] == league_name]    
    if season!='':
        complete_data = complete_data[complete_data['Season']==season]

    player_df_before = complete_data[complete_data['Player Name'] == player_name]    

    player_df = get_player_metrics_percentile_ranks(complete_data, player_name, position, position_specific_metric)
    if player_df is None or player_df.empty:
        st.error(f'Player {player_name} not found.')
        return None

    available_metrics = position_specific_metric
    metric_values = player_df[available_metrics].iloc[0].values.tolist()
    # Ensure that metrics and values match
    if len(available_metrics) != len(metric_values):
        st.error("Metric mismatch error.")
        return None

    slice_colors = []
    for metric in metric_values:
        if metric >=70:
            slice_colors.append("#58AC4E")
        elif metric >=50:
            slice_colors.append("#1A78CF")
        else:
            slice_colors.append("#aa42af")
 
    baker = PyPizza(
        params=available_metrics,                  # list of parameters
        background_color="#222222",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=4,               # linewidth for last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    if api == "statbomb" :
        font_size = 12
    else:
        font_size = 8

    fig, ax = baker.make_pizza(
        metric_values,
        figsize=(9.5, 11),
        color_blank_space="same",
        blank_alpha=0.1,
        slice_colors=slice_colors,
        kwargs_slices=dict(edgecolor="#000000", zorder=2, linewidth=2),
        kwargs_params=dict(color="#F2F2F2", fontsize=font_size, fontproperties=custom_fontt, va="center"),
        kwargs_values=dict(color="#F2F2F2", fontsize=0, alpha=0, fontproperties=custom_fontt, zorder=-5)
    )

    fig.text(
        0.08, 0.94, f"{player_name}", size=25,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2"
    )

    fig.text(
        0.08, 0.92, f"Club: {str(player_df.iloc[0]['Team'])}", 
        size=10,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    fig.text(
        0.08, 0.90,
        "Percentile Rank vs. Positional Peers",
        size=10,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    # Convert 'Minutes Played' to an integer to remove decimals

    fig.text(
        0.08, 0.88,
        f"Minutes Played: {int(player_df_before['Minutes'])}  |  Age: {int(player_df_before['Age'])}",
        size=10,
        ha="left", fontproperties=custom_fontt, color="#F2F2F2", alpha=0.8
    )

    colors_list = ["#58AC4E", "#1A78CF", "#aa42af"]
    legend_elements = [
        Patch(facecolor=colors_list[0], edgecolor='white', label='>=70%'),
        Patch(facecolor=colors_list[1], edgecolor='white', label='50 - 69%'),
        Patch(facecolor=colors_list[2], edgecolor='white', label='<50%')
    ]
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(1.25, 0), fontsize=12, frameon=False, labelcolor='white')


    # Add a horizontal line at the top with the team's primary color
    fig.add_artist(plt.Line2D((0, 1.2), (0.87, 0.87), color='white', linewidth=2, alpha=0.8, transform=fig.transFigure))
       
    # Coordinates for the circles
    circle1_center_x, circle1_center_y = 0.5, 0.5  # Circle 1 center
    circle2_center_x, circle2_center_y = 0.5, 0.5  # Circle 2 center
    circle3_center_x, circle3_center_y = 0.5, 0.5  # Circle 3 center
    circle4_center_x, circle4_center_y = 0.5, 0.5  # Circle 4 center
    
    # Add circles
    circle_params = [
        (0.415, circle1_center_x, circle1_center_y),  # Circle 1
        (0.330, circle2_center_x, circle2_center_y),  # Circle 2
        (0.245, circle3_center_x, circle3_center_y),  # Circle 3
        (0.160, circle4_center_x, circle4_center_y)   # Circle 4
    ]
    
    for radius, x, y in circle_params:
        circle = Circle((x, y), radius, color='black', alpha=0.25, fill=False, zorder=50, linewidth=1.75, transform=ax.transAxes)
        ax.add_patch(circle)
    
    # Add text above circles
    # Add text '80' above circle 1
    ax.text(circle1_center_x, circle1_center_y + 0.395, '80',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '60' above circle 2
    ax.text(circle2_center_x, circle2_center_y + 0.31, '60',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '40' above circle 3
    ax.text(circle3_center_x, circle3_center_y + 0.225, '40',
            ha='center', va='center', fontsize=13, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)
    
    # Add text '20' above circle 4
    ax.text(circle4_center_x, circle4_center_y + 0.14, '20',
            ha='center', va='center', fontsize=13, zorder=80, color='white', alpha=0.325, fontproperties=custom_fontt, transform=ax.transAxes)

    return fig