# Tetris-Ai
AI developed to play Tetris using a neural network and genetic algorithm

## How to Run
If you would like to run the neural network for yourself, simply download Tetris2.py and Neural.py and run Tetris2.py with Python 3. The Tetris AI uses NumPy for array handling, but other than that there are no required packages.

## Intro
Over the March Break Week of 2018, I wanted to delve into machine learning.
I decided to build on my previous project where I created a Tetris clone in C by creating an AI that would play the game. However, I decided to use Python as I thought it'd be a great opportunity to learn a new language. Python also has great neural network libraries that I want to learn in the future, such as OpenAI. So, I had one week to learn python, learn about Neural Networks, and create a neural network from scratch.

## Overview
The Tetris AI uses a three layer neural network with 200 input neurons (each tile of the 20x10 game grid), 24 hidden neurons, and 4 output neurons (rotate, move left, move right, do nothing). To improve, the AI uses a genetic algorithm evolution system with a roulette selection system

### The Neural Network
Each neuron has its own sets of weights - how much it takes into account the value of each of the previous layer's neurons. Using the values of the previous layer and the weights of the specific neuron, each neuron comes up with its own value (between -1 and 1). Each layer  uses and builds upon the previous layer, untill each neuron in the final layer (the output layer) has gotten its value. The neuron in the output layer with the highest value decides the action to be taken.

### Evolution
At the start, each neuron's weights are randomly assigned. But, a random AI won't be very good at Tetris! To improve, the algorithm uses an evolutionary genetic algorithm.

Much like in real life, the algorithm evolves in generations. Each generation consists of a group of 100 individuals, each of whom are independent neural network brains with separate thoughts and weights for each of their neurons. As a result, each individual plays Tetris differently. Everyone then individually plays a Tetris game, and they get a "fitness score".

The fitness score is calculated by taking the [classic tetris score](http://tetris.wikia.com/wiki/Scoring) for clearing lines and adding the number of blocks the individual managed to place. This system promotes individuals who spread their pieces around, and rewards even more individuals that clear lines.

Once each individual has gotten their fitness score, natural selection occurs. In natural selection, the top three individuals stay alive and continue on to the next generation. Each other individual has a 10 percent chance to stay alive. This ten percent is very important as its very easy for an algorithm to get stuck in a local maximum for score - favouring one strategy where it might not be the best one. We use this ten percent to maintain diversity. The rest of the spots (up to 100 individuals per generation) are filled with children. Pairs of individuals are randomly selected to "mate" and produce offspring. The higher an individual's fitness score, the more likely they are selected to mate. Mating involves merging the weights of the two parents, similar to chromozones in meiosis.

Now that the next generation has been populated, the cycle repeats!

## Final Results
During the march break, I successfully created a neural network that could play tetris - sorta. The algorithm did definitely get better over time, though not much better. Here is the best run after over 12 hours of training and 187 generations
![Alt Text](https://media.giphy.com/media/45eLUMADLV3WTXzyIb/giphy.gif)

Honestly not bad! Still, it didn't quite meet my expectations of an AI that could play Tetris indefinitely. I unfortunately have to conclude that Tetris is simply too complicated for such a simple genetic algorithm + neural networ. In the future, I would likely need to implement a more complicated scoring system (maybe encouraging the filling of holes, and giving negative score for having holes that are blocked off) and a better set of data for input. Instead of simply giving the algorithm the entire game board, maybe pick out bits of important data: how much space is there below, to the left, to the right?

Still, it was an amazing and very insightful march break project. I look forwards to working more with AI in the future!
