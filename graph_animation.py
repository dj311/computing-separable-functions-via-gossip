import matplotlib
import matplotlib.animation
import matplotlib.pyplot
import networkx


class GraphAnimation(object):
    def __init__(self, fps=30):
        self.figure = matplotlib.pyplot.figure(figsize=(10, 10), dpi=150)
        self.frames = []
        self.fps = fps

    def add_frame(self, graph, node_positions, node_colors):
        # convert node colors to black and white
        node_colors = [
            matplotlib.colors.to_rgb((color/255, color/255, color/255))
            for color in node_colors
        ]

        axes = matplotlib.axes.Axes(self.figure, (0, 0, 1, 1))
        self.figure.add_axes(axes)

        # use nodes as their own positions, but scale into range -1 to 1:
        max_x = max(x for x, y in node_positions)
        max_y = max(x for x, y in node_positions)

        pos = {
            node: (position[0]/max_x, position[1]/max_y)
            for node, position in zip(graph.nodes, node_positions)
        }

        networkx.draw_networkx(
            graph,
            pos,
            arrows=False,
            ax=axes,
            with_labels=False,
            node_color=node_colors,
        )

        self.frames.append([axes])

    def render(self, filename):
        animation = matplotlib.animation.ArtistAnimation(self.figure, self.frames)
        animation.save(filename, fps=self.fps, extra_args=['-vcodec', 'libx264'])


if __name__ == '__main__':
    # Example ------------------------------------------------------------------

    # Use NetworkX for graphs
    #   https://networkx.github.io/documentation/stable/tutorial.html
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

    # For this example, just cycle the colors on each frame

    animation = GraphAnimation()
    animation.add_frame(graph, node_colors)

    for _ in range(300):
        node_colors = [node_colors[-1]] + node_colors[0:-1]
        animation.add_frame(graph, node_colors)

    animation.render('animation.mp4')
