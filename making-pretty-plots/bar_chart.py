import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


bar_df = pd.read_csv("bar_chart.csv")
bar_df["Country"] = [
    "<b>" + bar_df["Country"].iloc[i] + "</b>"
    if i not in range(3, 8)
    else bar_df["Country"].iloc[i]
    for i in bar_df.index
]

x = list(reversed(bar_df.turnout))
y = list(reversed(bar_df.Country))


fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.update_layout(
    xaxis=dict(automargin=True, showline=False, showgrid=False, showticklabels=False,),
    yaxis=dict(automargin=True, zeroline=False, showline=False, showticklabels=True,),
    plot_bgcolor="white",
    font=dict(family="Roboto Slab"),
)
fig.update_layout(
    width=650,
    height=500,
    yaxis2=dict(fixedrange=True, range=[0, 22], visible=False),
    xaxis2=dict(fixedrange=True, range=[0, 100], overlaying="x", visible=False),
    xaxis=dict(fixedrange=True, range=[0, 100]),
)


for Y in range(2, 2 * len(x), 2):
    fig.add_trace(
        go.Scatter(
            y=[Y, Y],
            x=[-100, 100],
            mode="lines",
            hoverinfo="none",
            showlegend=False,
            line=dict(color="#c5c5c5", width=0.5),
        ),
        secondary_y=True,
    )
    fig.data[-1].update(xaxis="x2")


fig.add_trace(
    go.Bar(
        x=[100] * len(y),
        y=y,
        marker=dict(color="#f4f4f4", line_width=0),
        orientation="h",
        showlegend=False,
        hoverinfo="none",
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Bar(
        x=x[:3],
        y=y[:3],
        text=x[:3],
        textposition="inside",
        insidetextanchor="start",
        texttemplate="%{text}%",
        name="European countries with the lowest <br> turnout in the last federal election",
        marker=dict(color="#257d88", line_width=0),
        orientation="h",
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Bar(
        x=x[3:8],
        y=y[3:8],
        text=x[3:8],
        textposition="inside",
        insidetextanchor="start",
        texttemplate="%{text}%",
        name="For comparison",
        marker=dict(color="#c5c5c5", line_width=0),
        orientation="h",
    ),
    secondary_y=False,
)
fig.add_trace(
    go.Bar(
        x=x[8:],
        y=y[8:],
        text=x[8:],
        textposition="inside",
        insidetextanchor="start",
        texttemplate="%{text}%",
        name="...with highest turnout",
        marker=dict(color="#c71817", line_width=0),
        orientation="h",
    ),
    secondary_y=False,
)


fig.update_layout(
    title=dict(
        text="<b>European countries with lowest & highest voter turnout</b>",
        font=dict(size=20, color="black",),
        x=0.02,
    ),
    legend=dict(x=-0.4, y=1.14, font=dict(size=12, color="black",), orientation="h"),
    showlegend=True,
    yaxis=dict(color="black"),
    bargap=0.4,
    margin=dict(pad=10),
    barmode="overlay",
    uniformtext=dict(minsize=13),
)

text = "<i>Voting in Luxembourg and Belgium is compulsory.</i>"
fig.update_layout(
    annotations=[
        dict(
            xref="paper",
            yref="paper",
            x=-0.35,
            y=-0.03,
            xanchor="left",
            yanchor="top",
            text=text,
            align="left",
            font=dict(size=12, color="rgb(100,100,100)"),
            showarrow=False,
            bgcolor="white",
            width=350,
        )
    ]
)


fig.show()
fig.write_image("bar_chart.svg")

