# Breakout Game

A simple implementation of the classic Breakout game using Pygame.

## Contents
The repository contains the following files and folders:

- main.py: The main file containing the game loop and entry point of the game.
- classes.py: This file contains all the required classes for the game, including the Player, Ball, Block, Laser, and Upgrade classes.
- settings.py: This file contains all the fixed variables and settings for the game.
- PNG/: A folder containing images used in the game, sourced from [OpenGameArt](https://OpenGameArt.org.)

## Introduction

This repository contains the source code and assets for a Breakout game. The game is built using the Pygame library, and it features a player-controlled paddle, a bouncing ball, and blocks to break. The goal of the game is to destroy all the blocks by bouncing the ball off the paddle and hitting the blocks with it.

## Features

- Player-controlled paddle: Move the paddle horizontally to bounce the ball and prevent it from falling.
- Bouncing ball: The ball moves around the screen, bouncing off the walls, paddle, and blocks.
- Blocks: Destroy the blocks by hitting them with the ball. Each block has its own health, and it takes multiple hits to destroy some blocks.
- Power-ups: Collect power-ups that drop from destroyed blocks to gain special abilities, such as slower paddle movement, faster ball speed, extra lives, and laser shooting.
- Game over condition: The game ends when the player loses all lives by allowing the ball to fall off the screen.

## Requirements

- Python 3.x
- Pygame library

## How to Play

1. Install Python 3.x on your machine if you haven't already.
2. Install the Pygame library.
3. Clone this repository or download the source code and assets.
4. Open a terminal or command prompt and navigate to the directory where the source code is located.
5. Run the main.py file to start the game.
6. Use the left and right arrow keys to move the paddle and prevent the ball from falling off the screen.
7. Hit the blocks with the ball to destroy them and earn points.
8. Collect power-ups to gain special abilities and improve your chances of clearing the level.
9. Try to destroy all the blocks before losing all your lives.

## Acknowledgements

This game was developed as a learning project and is inspired by the classic Breakout game.

## License

This project is licensed under the [MIT License](LICENSE).
