import matplotlib
import matplotlib.animation
import matplotlib.pyplot
import networkx

import algorithm
import graph_animation


graph = networkx.generators.grid_2d_graph(20, 20)

# Give nodes starting colors:
b = 1.0
g = 1.0
y = 255.0
r = 255.0

node_colors = [
    b, b, g, g, y, y, y, y, b, b, b, r, b, r, b, b, b, y, y, y,
    b, b, g, g, y, y, y, y, b, b, b, b, b, b, b, b, b, y, y, y,
    b, b, r, r, y, y, y, r, b, b, b, b, b, r, b, b, b, b, b, b,
    b, b, r, r, y, y, y, y, y, y, b, b, b, b, b, b, b, b, b, b,
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

functions = [lambda x: x] * 20 * 20

# algorithm assumes nodes are identified by the numbers 1...n
# but networkx generates node names as (x, y) tuples.
node_positions = list(graph.nodes.keys())
graph = networkx.convert_node_labels_to_integers(graph)

# steal the tuples as position values, then rename the nodes

animation = graph_animation.GraphAnimation(fps=10)
animation.add_frame(graph, node_positions, node_colors)

def handle_estimate_update(node_colors):
    animation.add_frame(graph, node_positions, node_colors)

algorithm.comp(
    graph,
    node_colors,
    functions,
    handle_estimate_update,
)

animation.render('animation.mp4')
