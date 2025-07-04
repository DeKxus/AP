#!/usr/bin/env python3
# Updated on Fri May 12 07:35:03 2023
# -*- coding: utf-8 -*-

import numpy as np
from numpy.random import randint

class SnakeGame:
    " Implements the snake game core"

    def __init__(self, width, height, food_amount=1,
                 border = 0, grass_growth = 0,
                 max_grass = 0):
        "Initialize board"
        self.width = width
        self.height = height
        self.board = np.zeros( (height,width,3),dtype = np.float32)
        self.food_amount = food_amount
        self.border = border
        self.grass_growth = grass_growth
        self.grass = np.zeros( (height,width) ) + max_grass
        self.max_grass = max_grass
        self.reset()

    def create_apples(self):
        "create a new apple away from the snake"
        while len(self.apples)<self.food_amount:
            apple = ( randint(0,self.height-1), randint(0,self.width-1) )
            while apple in self.snake:
                apple = ( randint(0,self.height-1), randint(0,self.width-1) )
            self.apples.append(apple)

    def create_snake(self):
        "create a snake, size 3, at random position and orientation"
        x = randint( 5, self.width-5 )   # not t0o close to border
        y = randint( 5, self.height-5 )
        self.direction = randint(0,4)
        self.snake = []
        for i in range(5):
            if self.direction == 0:
                y = y+1
            elif self.direction==1:
                x = x-1
            elif self.direction==2:
                y = y-1
            elif self.direction==3:
                x = x+1
            self.snake.append( (y,x) )

    def grow_snake(self, d):
        "add one position to snake head (0=up, 1=right, 2=down, 3=left)"
        y,x = self.snake[0]
        if d == 0:
            y = y-1
        elif d == 1:
            x = x+1
        elif d == 2:
            y = y+1
        else:
            x = x-1
        self.snake.insert(0,(y,x))

    def check_collisions(self):
        "check if game is over by colliding with edge or itself"
        # just need to check snake's head
        x,y = self.snake[0]
        if (x == -1 or x == self.height 
            or y == -1 or y == self.width
            or (x,y) in self.snake[1:]):
            self.done = True

    def step(self, action):        
        """
        move snake/game one step 
        action can be -1 (turn left), 0 (continue), 1 (turn rignt)
        """
        direction = int(action)
        assert -1<=direction<=1        
        self.direction+=direction
        if self.direction<0:
            self.direction = 3
        elif self.direction>3:
            self.direction = 0
        self.grow_snake(self.direction)  # two steps: grow+remove last
        if self.snake[0] in self.apples:            
            self.apples.remove(self.snake[0])
            reward = 1
            self.create_apples()     # new apple
        else:
            self.snake.pop()
            self.check_collisions()
            if self.done:
                reward = -1
            else:
                reward = 0
                
        if reward>=0:
            x,y = self.snake[0]
            reward += self.grass[x,y]
            self.grass[x,y] = 0
            self.score+=reward
            self.grass += self.grass_growth 
            self.grass[self.grass>self.max_grass] = self.max_grass
                
        return self.board_state(),reward,self.done, {'score':self.score}

    def get_state(self):
        "easily get current state (score, apple, snake head and tail)"        
        score = self.score
        apple = self.apples
        head = self.snake[0]
        tail = self.snake[1:]
        return score,apple,head,tail,self.direction
        
    def print_state(self):
        "print the current board state"
        for i in range(self.height):
            line='.'*self.width
            for x,y in self.apples:
                if y==i:
                    line = line[:x]+'A'+line[x+1:]
            for s in self.snake:
                x,y=s
                if y==i:
                    line = line[:x]+'X'+line[x+1:]
            print(line)

    def test_step(self, direction):
        "to test: move the snake and print the game state"
        self.step(direction)
        self.print_state()
        if self.done:
            print("Game over! Score=",self.score)
    
    def reset(self):
        "reset state"
        self.score = 0
        self.done = False
        self.create_snake()
        self.apples = []
        self.create_apples()
        self.grass[:,:] =  self.max_grass
        
        return self.board_state(),0,self.done, {'score':self.score}
    
    def board_state(self, mode='human', close=False):
        "Render the environment"
        self.board[:,:,:] = 0
        if self.max_grass>0:
            self.board[:,:,1] = self.grass/self.max_grass * 0.3
        if not self.done:
            x,y = self.snake[0]
            self.board[x,y,:] = 1
        for x,y in self.snake[1:]:
            self.board[x,y,0] = 1
        for x,y in self.apples: 
            self.board[x,y,1] = 1
        if self.border == 0:
            return self.board
        else:
            h,w,_ = self.board.shape
            board = np.full((h+self.border*2,w+self.border*2,3),0.5,np.float32)
            board[self.border:-self.border,self.border:-self.border] = self.board 
            return board
    
    def get_snake_positions_direction(self):
        "gets snakes position and current direction"
        return (self.snake, self.direction) 
    
    def get_food_positions(self):
        "Return the current positions of the food"
        return self.apples
    
    def simulate_snake_grow(self, d):
        "simulate one position to snake head (0=up, 1=right, 2=down, 3=left)"
        y,x = self.snake[0]
        if d == 0:
            y = y-1
        elif d == 1:
            x = x+1
        elif d == 2:
            y = y+1
        else:
            x = x-1
        return (y,x)
    
    def heuristic_check_collisions(self, action):
        """
        check for collisions based on the application of a certain action 
        during the process of heuristic, by colliding with edge or itself
        """

        # Get correspondending direction
        direction = int(action)
        heuristic_direction = self.direction
        assert -1<=direction<=1        
        heuristic_direction+=direction
        if heuristic_direction<0:
            heuristic_direction = 3
        elif heuristic_direction>3:
            heuristic_direction = 0

        # Get the next position where the snake will move to
        x,y = self.simulate_snake_grow(heuristic_direction)

        # just need to check snake's head
        if (x == -1 or x == self.height 
            or y == -1 or y == self.width
            or (x,y) in self.snake[1:]):
            #print("Collision: ", (x,y), " Snake positions: ", self.snake )
            #print("Direction: ", self.direction, " Action: ", action, "Heuristic directon: ", heuristic_direction )
            return True
        #print("Next position: ", (x,y), " Snake positions: ", self.snake )
        #print("Direction: ", self.direction, " Action: ", action, "Heuristic directon: ", heuristic_direction )
        return False
    
    def heuristic_step(self):        
        """
        move snake/game one step using heuristic
        action can be -1 (turn left), 0 (continue), 1 (turn rignt)
        """
        # Action names
        action_name = {-1:'Turn left',0:'Straight ahead',1:'Turn right'}

        # Get positions of snake and food
        food_positions = self.get_food_positions()
        snake_positions, direction = self.get_snake_positions_direction()
        head_y, head_x = snake_positions[0]

        # Determine the closest food
        closest_food = min(food_positions, key=lambda food: abs(food[0] - head_y) + abs(food[1] - head_x))
        food_y, food_x = closest_food

        action = 0

        # Determine action to move towards the closest food
        if direction == 0:  # Up
            if food_x < head_x:
                action = -1  # Turn left
            elif food_x > head_x:
                action = 1   # Turn right
            else:
                action = 0   # Straight ahead
        elif direction == 1:  # Right
            if food_y < head_y:
                action = -1  # Turn left
            elif food_y > head_y:
                action = 1   # Turn right
            else:
                action = 0   # Straight ahead
        elif direction == 2:  # Down
            if food_x < head_x:
                action = 1   # Turn right
            elif food_x > head_x:
                action = -1  # Turn left
            else:
                action = 0   # Straight ahead
        elif direction == 3:  # Left
            if food_y < head_y:
                action = 1   # Turn right
            elif food_y > head_y:
                action = -1  # Turn left
            else:
                action = 0   # Straight ahead

        # Check for collisions
        if self.heuristic_check_collisions(action):
            # Loops all possible actions
            for a in action_name:
                if a is not action and not self.heuristic_check_collisions(a):
                    action = a
                    break
 
        return action

#just run this if this file is the main
if __name__ == '__main__':
    game = SnakeGame(20,20)
    game.print_state()
    
			
