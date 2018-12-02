import numpy
import scipy


def comp(values, functions):
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
    nodes = range(len(values))
    n = len(nodes)
    r = n  # arbitrarly selected for ease

    # Step 0: Nothing to do since we've been given the values list

    # Step 1: Create and populate W, an n by r array which maps each
    # W[node][l=1...r] to a sample from Exp with rate f(i, xi)).
    W = [None] * n
    for node in nodes:
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
    messages = [W[node] for node in nodes]

    estimates = [values[node] for node in nodes]

    for _ in range(1000):
        num_inaccurate_estimates = len([
            estimate for estimate in estimates
            if (1+epsilon)* <= estimate <= (1-epsilon)*
        ])


        spread(nodes, edges, messages)




    # w(node, time) maps each node to an r-length vector of 
    # w = [W[node] for node in nodes]


def spread(nodes, edges, messages):
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
    n = len(nodes)

    # TODO: figure out how to pick receiver node.
    # For now, pick one uniform random:
    reciever = numpy.random.random_integers(0, n-1)

    # Step 1: Pick node, u, which sends messages
    sender = numpy.random.random_integers(0, n-1)

    pass
