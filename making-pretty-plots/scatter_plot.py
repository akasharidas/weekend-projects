# %%
from re import T
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# %%
scatter_df = pd.read_csv("scatter_plot.csv").sort_values(by="country")
scatter_df = scatter_df[scatter_df["country"] != "Taiwan"]

df_1800 = scatter_df[scatter_df["year"] == 1800].set_index("country", drop=True)
df_2015 = scatter_df[scatter_df["year"] == 2015].set_index("country", drop=True)

x_1800 = df_1800["Income (GDP per capita)"]
x_2015 = df_2015["Income (GDP per capita)"]
y_1800 = df_1800["Life expectancy in years"]
y_2015 = df_2015["Life expectancy in years"]

scale_factor_1800 = 1e7
scale_factor_2015 = 3e7
min_size = 2
size_1800 = df_1800["population"] / scale_factor_1800
size_2015 = df_2015["population"] / scale_factor_2015
size_1800 = size_1800.clip(lower=min_size)
size_2015 = size_2015.clip(lower=min_size)


colours = {
    "India": "#19647e",
    "China": "#ae0108",
    "United States": "#9b753d",
    "Somalia": "#ca6900",
}

# %%
fig = go.Figure()

fig.update_layout(
    xaxis=dict(automargin=True, showline=True, showgrid=True),
    yaxis=dict(automargin=True, zeroline=True, showline=True, color="black"),
    # plot_bgcolor="white",
    # font=dict(family="Roboto Slab"),
    showlegend=False,
)
fig.update_layout(
    width=600, height=600,
)


for country in df_1800.index:
    fig.add_trace(
        go.Scatter(
            x=[x_1800[country], x_2015[country]],
            y=[y_1800[country], y_2015[country]],
            mode="lines+markers",
            marker=dict(
                size=[size_1800[country], size_2015[country]],
                color=[colours.get(country, "#b0b0b0")] * 2,
            ),
            line=dict(color="#b0b0b0", width=0.1),
            name=country,
        ),
    )


fig.update_xaxes(type="log", range=[np.log10(x_1800.min()), np.log10(x_2015.max())])
fig.update_yaxes(range=[0, 95])

# fig.update_layout(
#     title=dict(
#         text="<b>European countries with lowest & highest voter turnout</b>",
#         font=dict(size=20, color="black",),
#         x=0.02,
#     ),
#     legend=dict(x=-0.4, y=1.14, font=dict(size=12, color="black",), orientation="h"),
#     showlegend=True,
#     yaxis=dict(color="black"),
#     bargap=0.4,
#     margin=dict(pad=10),
#     barmode="overlay",
#     uniformtext=dict(minsize=13),
# )


# text = "<i>Voting in Luxembourg and Belgium is compulsory.</i>"
# fig.update_layout(
#     annotations=[
#         dict(
#             xref="paper",
#             yref="paper",
#             x=-0.35,
#             y=-0.03,
#             xanchor="left",
#             yanchor="top",
#             text=text,
#             align="left",
#             font=dict(size=12, color="rgb(100,100,100)"),
#             showarrow=False,
#             bgcolor="white",
#             width=350,
#         )
#     ]
# )


fig.show()
# fig.write_image("scatter_plot.svg")


# %%
