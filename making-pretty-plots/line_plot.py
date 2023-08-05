import plotly.graph_objects as go
import pandas as pd

line_df = pd.read_csv("line_plot.csv")

line_attrs = {
    k: {"width": 1, "color": "rgb(190, 190, 190)",} for k in line_df.columns[1:]
}
line_attrs["United States"]["width"] = 4
line_attrs["United States"]["color"] = "#c71e1d"
line_attrs["France"]["width"] = 2
line_attrs["France"]["color"] = "#18a1cd"
line_attrs["Germany"]["width"] = 2
line_attrs["Germany"]["color"] = "#15607a"


fig = go.Figure()

for i, col in enumerate(line_df.columns[1:]):
    fig.add_trace(
        go.Scatter(
            x=line_df["country"],
            y=line_df[col],
            mode="lines",
            line=line_attrs[col],
            name=col,
        )
    )

fig.update_layout(
    xaxis=dict(
        automargin=True,
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor="black",
        linewidth=1,
        ticks="outside",
        tickfont=dict(family="Arial", size=14, color="rgb(82, 82, 82)",),
    ),
    yaxis=dict(
        automargin=True,
        showgrid=True,
        zeroline=False,
        showline=False,
        showticklabels=True,
        range=[0, 12],
        tickvals=[0, 2, 4, 6, 8, 10],
        gridcolor="rgb(190, 190, 190)",
        tickfont=dict(family="Arial", size=14, color="rgb(120, 120, 120)",),
    ),
    showlegend=False,
    plot_bgcolor="white",
)
fig.update_layout(width=900, height=500)

text = "<br>".join(["sold cigarettes", "per day per adult"])
fig.update_layout(
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=0.001,
            y=0.85,
            xanchor="left",
            yanchor="top",
            text=text,
            align="left",
            font=dict(family="Arial", size=14, color="rgb(100,100,100)"),
            showarrow=False,
            bgcolor="white",
            width=110,
        )
    ]
)


fig.show()
# fig.write_image("line_plot.svg")
