# Flappy Bird AI
Flappy Bird remade in &lt;300 lines and an AI to play it

## Requirements

```pip install pygame neat-python```

## How to play

Run `flap.py` to play Flappy Bird yourself. Press `Up Arrow` to flap, `Space` to reset the game. You can adjust the simulation rate, gravity strength, pipe spacing, and flap impulse in the code if you wish.

Run `flappy_ml.py` to use Neuro Evolution of Augmenting Topologies (NEAT), an evolutionary algorithm, to evolve an AI to play the game! It is highly likely that the AI becomes perfect at the game by the 10th generation.

Can you beat the AI? Probably not! :grin:
___

NEAT is an algorithm that [evolves neural network topologies along with its weights to maximize a fitness function](http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf). I made this as a practice project to learn the basics of genetic algorithms and game development. Inspired by Tech With Tim's [video series](https://www.youtube.com/watch?v=OGHA-elMrxI).
