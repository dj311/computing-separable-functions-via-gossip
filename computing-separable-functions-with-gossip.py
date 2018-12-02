import itertools
import matplotlib
import matplotlib.pyplot
import networkx
import numpy
import random
import scipy


def draw_frame(figure, graph, node_colors):
    axes = matplotlib.axes.Axes(figure, (0, 0, 1, 1))
    figure.add_axes(axes)

    # use nodes as their own positions, but scale into range -1 to 1:
    max_x = max(x for x, y in graph.nodes)
    max_y = max(x for x, y in graph.nodes)

    pos = {
        (x, y): (x/max_x, y/max_y)
        for x, y in graph.nodes
    }

    networkx.draw_networkx(
        graph,
        pos,
        arrows=False,
        node_color=node_colors,
        ax=axes,
        with_labels=False,
    )

    return axes


# Use NetworkX for graphs (https://networkx.github.io/documentation/stable/tutorial.html)
graph = networkx.generators.grid_2d_graph(20, 20)

# Give nodes starting colors:
b = matplotlib.colors.to_rgb('#1b3fae')
g = matplotlib.colors.to_rgb('#3b9e1c')
y = matplotlib.colors.to_rgb('#ffff00')
r = matplotlib.colors.to_rgb('#ab1717')

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

figure = matplotlib.pyplot.figure(figsize=(10, 10), dpi=150)

frames = []
for _ in range(200):
    random.shuffle(node_colors)
    frames.append(
        [draw_frame(figure, graph, node_colors)]
    )

animation = matplotlib.animation.ArtistAnimation(figure, frames)
animation.save('animation.mp4', fps=5, extra_args=['-vcodec', 'libx264'])

# Exponential Variable:
# scipy.stats.expon (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html)
