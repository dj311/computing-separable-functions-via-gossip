# Computing Separable Functions via Gossip

Implementation of the algorithm in "Computing separable functions via gossip." [1] applied to the mixing of colours in a network. See our [presentation](Computing Separable Functions via Gossip.pdf) for a quick explanation, though it's missing key parts which were otherwise delivered via speech.

The paper [1] itself is probably worth a read. It provides an algorithm for calculating (separable) functions over a network when each node starts with a single part of the function we want to calculate. In this scenario, nodes are only aware of (and can only communicate with) there direct neighbours, and they don't have unique identifiers. The authors developed an algorithm that each node in the network runs to share information, and calculate the function. They then prove that this algorithm completes in a bounded time. The algorithm utilises a property of exponential random variables in a pretty cool way!

_Note:_ This was written on a tight deadline ahead of presentation and it's code quality reflects that. Unfortunately that means the code should be understandable if you already grok the algorithm in the paper, but it is unlikely that reading this will help you understand it. One day I'd like to rewrite this algorithm with a focus on individual nodes as actors in the simulation. I reckon reading the algorithm from the point of view of an individual node _would_ help with understanding.

## Demo

In these demonstrations the color of each node is represented by a single value ranging from 0 (yellow) to 1 (blue). At each iteration nodes spread information about their color to direct neighbours. Each node then updates their local estimate of the networks average color. Calculating an average is not actually separable so we estimate two separate values that are. The first is the number of nodes and the second is the sum of all nodes color values. These are both separable, and we can calculate the average color with `<total color value>/<number of nodes>`. 

This first demo shows a group of nodes arranged in a grid/lattice. As time goes on, the nodes estimates converge on an accurate value. 

[<img src="./demo-image.png">](https://daniel.wilshirejones.com/res/animation_light.mp4)
[(dark)](https://daniel.wilshirejones.com/res/animation_dark.mp4)

### Handling Network Partitions
[This visualisation](https://daniel.wilshirejones.com/res/animation_partitions.mp4) shows a grid network which has been partitioned and split across it's diagonal. Once the inidividual partitions are close to consensus, a bridge forms between them. It shows the following properties quite nicely:
  1. The blue partition displays some perturbations despite all of it's nodes starting with the exact same colour. 
      - This demonstrates the stochastic nature of using the emperical mean of a random variable to transfer information.
      - In the simulation, blue is represented by the number 1, and yellow the number 255. Since the estimation is made by taking the inverse of the emperical mean, it is possible that similar sized fluctuations in blue and yellow have a bigger relative effect on blue.
  2. Despite there only being two connections between the partitions, they are able to reach a (visual) consensus relatively quickly.
  3. The algorithm (running on individual nodes) is resilient to network partitions and failures. 
      - Since the method described in the paper _does_ have a significant performance penalty compared to a centralised approach, it is important to demonstrate it's advantages.
  
## Setup
For the video output to work, [ffmpeg](https://www.ffmpeg.org/) should be installed and working on your system. Besides that, it's the usual Python affair:
  1. Make a virtualenv: `python3 -m venv env`.
  2. Activate the virtualenv in your fave shell: `source ./env/bin/activate`.
  3. Install dependencies: `pip install -r requirements.txt`.

## Generating the Demo
  1. Make sure the the virtualenv is active: `source ./env/bin/activate`.
  2. Run the demo script: `python3 ./averaging_colors.py`.
  3. Wait a couple of minutes and the file `./animation.mp4` should appear.

## Usage
The code for the demo (averaging colors over a grid network) is separated out from the main algorithm implementation, which can be found in `algorithm.py`. You can import those functions in your own scripts if you're keen to play around.

## References

[1]: Mosk-Aoyama, Damon, and Devavrat Shah. "Computing separable functions via gossip." Proceedings of the twenty-fifth annual ACM symposium on Principles of distributed computing. ACM, 2006. [DOI: 10.1145/1146381.1146401](https://scholar.google.com/scholar?q=10.1145%2F1146381.1146401)
