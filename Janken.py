from enum import Enum
import re

import settings
from game import Game


class JankenGesture(Enum):
    ROCK = 0
    SCISSORS = 1
    PAPER = 2

class GameResult(Enum):
    DRAW = 0
    LOSE = 1
    WIN = 2

class Janken(Game):
    def __init__(self, connectThread, totalRoundNum):
        super().__init__(connectThread)
        self.__totalRoundNum = totalRoundNum
        self.__currentRoundNum = 0
        self.__resultList = []


    def whole_game(self):
        self.__currentRoundNum = 1
        while self.__currentRoundNum <= self.__totalRoundNum:
            print('Round %d', self.__currentRoundNum)
            self.one_round()
            self.__currentRoundNum += 1
        self.show_result()


    def show_result(self):
        winNum = 0
        loseNum = 0
        for result in self.__resultList:
            if result == GameResult.WIN:
                winNum += 1
            elif result == GameResult.LOSE:
                loseNum += 1
        print('Game finished')
        print('Win: %d, Lose: %d, Draw: %d', (winNum, loseNum, self.__totalRoundNum - winNum - loseNum))


    def one_round(self):
        inputStr = input("Choose your gesture (0-Rock, 1-Scissors, 2-Paper): ")
        while inputStr not in ('0', '1', '2'):
            inputStr = input("Your input is not of a correct form, please enter again: ")
        myGesture = JankenGesture(int(inputStr))
        self.__thread.send_message(('\janken ' + inputStr).encode('utf-8'))
        opponentGesture = self.get_opponent_gesture()
        result = self.round_result(myGesture, opponentGesture)
        self.__resultList.append(result)


    def get_opponent_gesture(self):
        message = self.__thread.get_message()
        messageWords = re.split(r'\s', message)
        assert messageWords[0] == r'\janken', 'Recevied message with incorrect format in janken'
        return JankenGesture(int(messageWords[1]))


    def round_result(self, myGesture, opponentGesture):
        result = GameResult((myGesture.value - opponentGesture.value) % 3)
        gestureDisplayDict = {JankenGesture.ROCK: 'Rock',
                       JankenGesture.SCISSORS: 'Scissors',
                       JankenGesture.PAPER: 'Paper'}
        resultDisplayDict = {GameResult.DRAW: ('-X-', 'Draw'),
                             GameResult.WIN: ('-->', 'You Win!'),
                             GameResult.LOSE: ('<--', 'You Lose')}
        print('%s: %s %s %s :%s', (settings.username, gestureDisplayDict[myGesture], resultDisplayDict[result][0], gestureDisplayDict[opponentGesture], self.__opponentNickname))
        print(resultDisplayDict[result][1])
        return result