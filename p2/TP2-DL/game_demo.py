#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 07:35:58 2021
Updated on Fri May 12 07:35:00 2023

"""
import matplotlib.pyplot as plt
import numpy as np
from snake_game import SnakeGame
from matplotlib.animation import FuncAnimation


def plot_board(file_name,board,text=None):
    plt.figure(figsize=(10,10))
    plt.imshow(board)
    plt.axis('off')
    if text is not None:
        plt.gca().text(3, 3, text, fontsize=45,color = 'yellow')
    plt.savefig(file_name,bbox_inches='tight')
    plt.close()

def snake_demo(actions):
    game = SnakeGame(30,30,border=1)
    board,reward,done,info = game.reset()    
    action_name = {-1:'Turn left',0:'Straight ahead',1:'Turn right'}    
    plot_board('0.png',board,'Start')
    for frame,action in enumerate(actions):
        board,reward,done,info = game.step(action)
        plot_board(f'{frame+1}.png',board,action_name[action])


def test_heuristic(steps = 1000):
    board_heuristic = []
    actions_heuristic = []
    game = SnakeGame(30,30,border=1)
    board,reward,done,info = game.reset()
    board_heuristic.append(board.copy())
    for step in range(steps):

        action = game.heuristic_step()
        board, reward, done, info = game.step(action)
        board_heuristic.append(board.copy())
        actions_heuristic.append(action)

        if done:
            break

    return board_heuristic, actions_heuristic
                         
images = []
actions = []
for i in range(100):
    images, actions = test_heuristic()
    if len(images) < 250:
        print(len(images))

#     if len(images) < 250:
#         print(len(images))
#         print(actions)
#         print("shape: ", images[0].shape)
#         break

# # Define the update function for the animation
# def update(frame):
#     plt.clf()  # Clear the current frame
#     plt.imshow(images[frame])  # Display the current image
#     plt.axis('off')  # Hide the axes for a cleaner look

# fig = plt.figure()

# # Create the animation
# ani = FuncAnimation(fig, update, frames=len(images), interval=10, repeat=True)

# # Display the animation
# plt.show()
