# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 22:01:42 2018

@author: thaneig
"""

import numpy as np
from collections import Counter
import warnings
from random import shuffle
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

colors = ["white", "black", "yellow", "orange", "green", "blue", "red", "brown"]

def checkAnswer(input, solution, shuffle_output=True, option_brown=False):
    if len(input) != len(solution):
        warnings.warn("input and solution don't have the same length")
        return None
    if input == solution:
        return ["black"] * len(solution)
    else:
        # find non equal colors
        input_neq, solution_neq = zip(*((inp, sol) for inp, sol in zip(input, solution) if inp != sol))
        # find number of black pins
        n_black = len(solution) - len(solution_neq)
        # counter number of each color
        input_counts, solution_counts = (Counter(input_neq), Counter(solution_neq))
        # count how often color equals
        n_white = 0
        for color in solution_counts:
            if color in input_counts: n_white += min(input_counts[color], solution_counts[color])
        n_empty = len(solution) - n_black - n_white

        pins = ["black"] * n_black + ["white"] * n_white
        if shuffle_output and len(pins) > 0:
            shuffle(pins)
        if option_brown:
            pins = pins + ["brown"] * n_empty
        else:
            pins = pins + ["empty"] * n_empty
        return pins


class Game:
    entries = 0
    state = 0
    solution = []
    moves = []
    answers = []

    def __init__(self, entries, colors):
        self.solution = list(np.random.choice(colors, size=entries, replace=True))
        self.entries = len(self.solution)

    def gameOver(self):
        for answer in self.answers:
            if all(pin == "black" for pin in answer):
                return True
        return False

    def makeMove(self, input):
        if self.state == 0 and len(input) == self.entries:
            answer = checkAnswer(input, self.solution, True, True)
            self.moves.append(input)
            self.answers.append(answer)
            # check if game is over
            if all(pin == "black" for pin in answer):
                self.state = 1
                return 1
            return answer
        if self.state == 0 and len(input) != self.entries:
            return print("you entered too many or too few moves")
        if self.state == 1:
            return -1

    def getallMoves(self, number=0):
        if number <= 0:
            return self.moves
        else:
            return self.moves[-number:]

    def getallAnswers(self, number=0):
        if number <= 0:
            return self.answers
        else:
            return self.answers[-number:]

    def numberofMovesTaken(self):
        return len(self.inputs)

    def stringGame(self):
        all = []
        middle_bar = ["brown"] * 2
        for answer, move in zip(self.answers, self.moves):
            all.append(answer + middle_bar + move)
        return all

def terminalPlay(colors,number):
    game = Game(number,colors)
    while game.state == 0:
        print("Please enter the next "+str(number)+" colors you want to try:")
        cols = []
        cols_temp = ""
        for i in range(number):
            cols_temp = input("Enter the "+str(i+1)+". color:")
            cols_temp = cols_temp.replace('\n', ' ').replace('\r', '')
            cols.append(cols_temp)
            if cols_temp == "quit":
                return 0
        game.makeMove(cols)
        answer = game.getallAnswers(1)
        print(answer)
    print("You have finished the Game! Bravo!!!")
    return 0

def plotGame(gameString,number):
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

    # Sort colors by hue, saturation, value and name.
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                    for name, color in colors.items())
    sorted_names = [name for hsv, name in by_hsv]

    color_map = {"brown": "saddlebrown",
                 "green": "seagreen",
                 "blue": "dodgerblue",
                 "red": "orangered",
                 "yellow": "gold",
                 "white": "lavender",
                 "black": "black"}

    n_entries = number
    n_games = 12
    ncols = 2 * n_entries + 3
    nrows = n_games + 2

    fig, ax = plt.subplots(figsize=(8, 5))

    # Get height and width
    X, Y = fig.get_dpi() * fig.get_size_inches()
    fig.set_xlim(0, X)
    #plt.set_ylim(0, Y)
    #plt.set_axis_off()
    h = Y / (nrows + 1)
    w = X / ncols

    h = Y / nrows
    w = X / ncols
    for i in range(nrows):
        y_bottom = i * h
        for j in range(ncols):
            x_left = j * w
            x_right = (j + 1) * w
            plt.hlines(y_bottom, x_left, x_right, color=colors[color_map["brown"]], linewidth=h)
    if len(gameString) > 0:
        for i in range(len(gameString)):
            y_bottom = (i + 1) * h
            line = gameString[i]
            line = ["brown"] + line + ["brown"]
            for j in range(len(line)):
                x_left = j * w
                x_right = (j + 1) * w
                plt.hlines(y_bottom, x_left, x_right, color=colors[color_map[line[j]]], linewidth=h)
    #fig.subplots_adjust(left=0, right=1,
    #                    top=1, bottom=0,
    #                    hspace=0, wspace=0)
    plt.show()
    #return plt.show()

def plotplay(colors,number):
    game = Game(number,colors)
    while game.state == 0:
        print("Please enter the next "+str(number)+" colors you want to try:")
        cols = []
        cols_temp = ""
        for i in range(number):
            cols_temp = input("Enter the "+str(i+1)+". color:")
            cols_temp = cols_temp.replace('\n', ' ').replace('\r', '')
            cols.append(cols_temp)
            if cols_temp == "quit":
                return 0
        game.makeMove(cols)
        #answer = game.getallAnswers(1)
        gameString = game.stringGame()
        plotGame(gameString, number)
    print("You have finished the Game! Bravo!!!")
    return 0


#example
terminalPlay(["blue","green","red"],3)
