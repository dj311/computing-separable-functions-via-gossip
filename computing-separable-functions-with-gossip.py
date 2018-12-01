import random
import itertools
import matplotlib
import networkx
import numpy
import scipy

from plotly.offline import plot


def plot_figure(graph):
    nodes = {
        'type': 'scatter',
        'x': [x for x, y in graph.nodes],
        'y': [y for x, y in graph.nodes],
        'mode': 'markers',
        'marker': {
            'size': 10,
            'color': [node_attributes['color'] for node_attributes in graph.nodes.values()],
        },
        'hoverinfo': 'none',
    }

    edge_xs = sum(
        [[start[0], end[0], None] for start, end in graph.edges],
        [],
    )
    edge_ys = sum(
        [[start[1], end[1], None] for start, end in graph.edges],
        [],
    )

    edges = {
        'type': 'scatter',
        'mode': 'lines',
        'x': edge_xs,
        'y': edge_ys,
        'line': {
            'width': 2,
            'color': '#eee',
        },
        'hoverinfo': 'none',
    }

    figure = {'data': [edges, nodes]}

    return figure


if __name__ == '__main__':
    # Setup the graph ----------------------------------------------------------------

    # Use NetworkX for graphs (https://networkx.github.io/documentation/stable/tutorial.html)
    graph = networkx.generators.grid_2d_graph(20, 20)

    # Give nodes starting colors:
    b = '#1b3fae'
    g = '#3b9e1c'
    y = '#ffff00'
    r = '#ab1717'

    node_colors = [
        b, b, b, b, y, y, y, y, b, b, b, r, b, r, b, b, b, y, y, y,
        b, b, b, b, y, y, y, y, b, b, b, b, b, b, b, b, b, y, y, y,
        b, b, b, b, y, y, y, r, b, b, b, b, b, r, b, b, b, b, b, b,
        b, b, b, b, y, y, y, y, y, y, b, b, b, b, b, b, b, b, b, b,
        b, b, b, b, y, y, y, y, y, y, b, b, b, b, b, b, b, b, b, b,
        b, b, b, b, y, y, y, y, y, y, y, y, y, y, b, b, b, b, g, g,
        b, b, b, b, y, y, y, y, y, y, y, y, y, y, y, b, b, g, g, g,
        b, b, b, b, b, b, y, y, y, y, y, y, y, y, y, b, b, g, g, g,
        b, b, b, b, b, b, y, y, y, y, y, y, y, b, b, b, b, b, g, g,
        b, b, b, b, b, b, y, r, y, y, y, b, b, b, b, b, b, b, b, b,
        b, b, b, b, b, b, y, y, y, y, y, b, b, b, b, b, b, b, b, b,
        b, b, b, b, y, y, y, y, y, y, b, b, b, r, b, b, b, r, b, b,
        b, b, b, b, y, y, y, r, y, y, b, b, b, b, b, b, b, b, b, b,
        b, b, b, b, y, y, y, y, y, y, b, b, b, b, b, b, b, b, y, b,
        b, g, g, b, y, y, y, y, y, b, b, b, b, b, b, b, b, y, y, y,
        b, g, g, b, y, y, y, y, b, b, b, b, b, b, b, b, y, y, y, y,
        b, b, b, b, y, y, y, y, b, b, b, r, b, y, y, y, y, y, y, b,
        b, b, b, b, y, y, y, y, b, b, b, y, y, y, y, y, y, b, b, b,
        y, y, y, y, y, y, y, y, b, b, b, b, y, y, y, b, b, b, r, r,
        y, y, y, y, y, y, y, y, b, b, b, b, b, b, b, b, b, b, r, r,
    ]

    for node_attributes, color in zip(graph.nodes.values(), node_colors):
        node_attributes['color'] = color


    axis = {
        'showline': False, # hide axis line, grid, ticklabels and  title
        'zeroline': False,
        'showgrid': False,
        'showticklabels': False,
        'title': '',
    }

    layout = {
        'title':  'Averaging Colours Over a Network with Gossip',
        'font':  {'family': 'Lora'},
        'autosize': True,
        'showlegend': False,
        'xaxis': axis,
        'yaxis': axis,
        'updatemenus': [
            {
                'type': 'buttons',
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [
                            None,
                            {
                                'frame': {'duration': 1000, 'redraw': False},
                                'mode': 'immediate',
                                'fromcurrent': True,
                                'transition': {'duration': 0, 'easing': 'linear'}
                            }
                        ],
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [
                            None,
                            {
                                'frame': {'duration': 0, 'redraw': False},
                                'mode': 'immediate',
                                'transition': {'duration': 0, 'easing': 'linear'},
                            }
                        ],
                    }
                ],
                'pad': {'r': 10, 't': 87},
                'showactive': False,
            }
        ],
    }

    frames = [plot_figure(graph)]
    for _ in range(20):
        random.shuffle(node_colors)
        for node_attributes, color in zip(graph.nodes.values(), node_colors):
            node_attributes['color'] = color
        frames.append(plot_figure(graph))


    figure = {
        'data': frames[0]['data'],
        'layout': layout,
        'frames': frames,
    }

    plot(figure)

    # Exponential Variable:
    # scipy.stats.expon (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html)
