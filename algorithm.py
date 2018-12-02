import math
import numpy
import scipy


def comp(graph, values, functions):
    """
    The COMP algorithm as described in "Computing Seperable Functions via
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
    n = len(nodes)
    r = n  # arbitrarly selected for ease
    error_threshold = 0.05  # epsilon in the paper
    allowed_failure_prob = 0.05  # delta in the paper

    # Step 0: Nothing to do since we've been given the values list

    # Step 1: Create and populate W, an n by r array which maps each
    # W[node][l=1...r] to a sample from Exp with rate f(i, xi)).
    W = [None] * n
    for node in graph.nodes:
        # Generate f(i, xi)
        fi = functions[node]
        xi = values[node]

        rate = fi(xi)
        mean = 1/rate  # numpy parameterizes exp by it's mean (= 1/rate)
        samples = numpy.random.exponential(mean, r)

        W[node] = samples

    # Step 2: Spread the information using magic

    # messages contains the message m(i) for each node i which it starts at time
    # 0. This is node i's set of r samples from it's Exp(f(i, xi)) distribution.
    messages = [
        [W[node]] for node in graph.nodes
    ]
    estimates = [
        values[node] for node in graph.nodes
    ]

    # calculate the upper bound of time to run and stop on that
    max_time = upper_bound_on_grid(2, n, error_threshold, allowed_failure_prob)
    for time in range(max_time):
        messages = spread(graph, messages)

        # so now messages

    # w(node, time) maps each node to an r-length vector of
    # w = [W[node] for node in nodes]


def spread(graph, messages):
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

    # TODO: figure out how to pick receiver node.
    # For now, pick one uniform random:
    reciever = numpy.random.choice(graph.nodes)

    # Step 1: Pick node to sends it's messages to the receiver.
    # Select this node uniformly from all nodes sharing edge with the receiver
    # node.
    neighbours = graph.neighbors(reciever)
    sender = numpy.random.choice(neighbours)

    messages[reciever] += messages[sender]

    return messages


def upper_bound_on_grid(dimensions, num_nodes, error_threshold, failure_prob):
    """
    Calculates the upper bound of time steps required for a <dimensions>-d grid
    network, consisting of <num_nodes> nodes to compute the value of a function
    with probability less...
    """
    return math.ceil(
        math.pow(error_threshold, -2)
        * (1 + math.log2(math.pow(failure_prob, -1)))
        * (math.log2(num_nodes) + math.log2(math.pow(failure_prob, -1)))
        * dimensions
        * math.pow(num_nodes, 1/dimensions)
    )


def calculate_estimate():
