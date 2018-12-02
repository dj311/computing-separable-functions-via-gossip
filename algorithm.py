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
         W_min_estimate(i, l) the of the minimum:

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

    # Create and populare W, an n by r array mapping [node][l]
    W = [[None] * r] * n]
    for node in nodes:
        for l in range(r):
            W[node][l] = scipy.stats.expon





def spread():
    """
    The SPREAD algorithm as described in "Computing Seperable Functions via
    Gossip". Takes in ... . Returns ... .

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

    pass
