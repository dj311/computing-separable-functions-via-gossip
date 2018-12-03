import copy
import math
import numpy
import scipy


def comp(graph, values, functions, updated_estimates_callback):
    """
    The COMP algorithm as described in "Computing Separable Functions via
    Gossip".
    - Takes in a list of per node measurements (values) and per node
      functions (functions).
    - Returns a list of F(values) estimates: the estimated summation of the
      f(i, xi)'s, one estimate for each node.

    These two lists are implicitly indexed by their node identifier (the
    numbers 1...n).

    Algorithm:
      0. Initially, for i={1, ..., n}, node i has the value f(i, xi) ≥ 1.

      1. Each node i generates r independent random numbers
         W(i, 1) , ..., W(i, r), where the distribution of each W(i, l) is
         exponential with rate f(i, xi) i.e. with mean 1/f(i, xi).

      2. Each node i computes, for l={1, ..., r} an estimate
         W_min_estimate(i, l) of the minimum W defined as:

             W_min(l) = min(i=1...n)[W(i, l)].

         This computation can be done using an information spreading algorithm
         like SPREAD below.

      3. Each node i computes
                                     r
           f(i, xi) = ----------------------------------
                       sum(l=1...r)[W_min_estimate(i, l)]

         as it's estimate of sum(i=1...n)[f(i, xi)]
    """

    # Ensure one-to-one mapping from node to value and function
    assert len(values) == len(functions)
    # Ensure values estimates are >= 1
    assert all(value >= 1 for value in values)

    # Setup parameters
    n = len(graph.nodes)
    r = n  # arbitrarly selected for ease
    error_threshold = 0.05  # epsilon in the paper
    allowed_failure_prob = 0.05  # delta in the paper

    n_values = [1]*n

    # Step 0: Nothing to do since we've been given the values list

    # Step 1: Create and populate W, an n by r array which maps each
    # W[node][l=1...r] to a sample from Exp with rate f(i, xi)).
    W = [None] * n
    for node in graph.nodes:
        # Generate f_i(x_i)
        f = functions[node]
        x = values[node]

        rate = f(x)
        mean = 1.0/rate  # numpy parameterizes exp by it's mean (= 1/rate)
        samples = numpy.random.exponential(mean, r)

        W[node] = samples

    n_W = [None] * n
    for node in graph.nodes:
        x = n_values[node]
        rate = x
        mean = 1.0/rate  # numpy parameterizes exp by it's mean (= 1/rate)
        samples = numpy.random.exponential(mean, r)

        n_W[node] = samples

    # Step 2: Spread the information using magic

    # messages contains the message m(i) for each node i which it starts at time
    # 0. This is node i's set of r samples from it's Exp(f(i, xi)) distribution.
    messages = [W[node] for node in graph.nodes]
    n_messages = [n_W[node] for node in graph.nodes]

    # our starting estimates are just the values (xi) of each node
    estimates = [values[node] for node in graph.nodes]
    n_estimates = [n_values[node] for node in graph.nodes]

    # calculate the upper bound of time to run and stop on that
    max_time = upper_bound_on_grid(2, n, error_threshold, allowed_failure_prob)
    for time in range(100): #max_time):
        messages = spread(graph, messages, r)

        estimates = [
            node_estimate(messages[node], r) for node in graph.nodes
        ]

        n_messages = spread(graph, n_messages, r)
        n_estimates = [
            node_estimate(n_messages[node], r) for node in graph.nodes
        ]

        updated_estimates_callback(estimates, n_estimates)

    # w(node, time) maps each node to an r-length vector of
    # w = [W[node] for node in nodes]


def spread(graph, messages, r):
    """
    The SPREAD algorithm as described in "Computing Seperable Functions via
    Gossip". It's a randomized gossip algorithm which aims to ...

    Takes in:
      - nodes :: list of nodes indexed 1...n.
      - edges :: list of graph edges mapping nodes to one another.
      - messages :: list indexed by node, containing the list of messages the
        node has received.

    Returns ... .

    Algorithm:
        When a node i initiates a communication at time t:

        1. Node i chooses a node u at random, and contacts u.

            The choice of the communication partner u is made
            independently of all other random choices, and the
            probability that node i chooses any node j is P(i, j).

        2. Node u sends all of the messages it has to node i, so
            that: M(i, t+) = M(i, t-) ∪ M(u, t-).

        Where t- represents the time immediately before t
        and t+ represents the time immediately after t.
    """
    previous_messages = [
        [Wl for Wl in node_messages]
        for node_messages in messages
    ]

    for receiver in graph.nodes:
        # Step 1: Pick node to sends it's messages to the receiver.
        # Select this node uniformly from all nodes sharing edge with the
        # receiver node.
        neighbours = list(graph.neighbors(receiver))
        sender = numpy.random.choice(neighbours)

        for l in range(r):
            messages[receiver][l] = min(
                previous_messages[receiver][l],
                previous_messages[sender][l],
            )

    return messages


def upper_bound_on_grid(dimensions, num_nodes, error_threshold, failure_prob):
    """
    Calculates the upper bound of time steps required for a <dimensions>-d grid
    network, consisting of <num_nodes> nodes to compute the value of a function
    with probability less...

    Based on analysis in section 5.3 of the paper.

    TODO: this could be plotted as error_threshold and failure_prob vary
    """
    return math.ceil(
        math.pow(error_threshold, -2)
        * (1 + math.pow(math.log(failure_prob), -1))
        * (math.log(num_nodes) + math.pow(math.log(failure_prob), -1))
        * dimensions
        * math.pow(num_nodes, 1/dimensions)
    )

def node_estimate(node_messages, r):
    min_Ws = node_messages
    F_estimate = r/sum(min_Ws)
    return F_estimate
