from sys import stdin
from termios import tcgetattr, ICANON, ECHO, tcsetattr, TCSAFLUSH, tcflush
from termios import TCIFLUSH, TCSANOW
from select import select


class Input:

    def __init__(self):
        self.__fd = stdin.fileno()
        self.__new = tcgetattr(self.__fd)
        self.__old = tcgetattr(self.__fd)
        self.__new[3] = (self.__new[3] & ~ICANON & ~ECHO)
        tcsetattr(self.__fd, TCSAFLUSH, self.__new)

    def checkStream(self):
        X, Y, Z = select([stdin], [], [], 0)
        return len(X) != 0

    def getFromStream(self):
        return stdin.read(1)

    def clearStream(self):
        tcflush(self.__fd, TCIFLUSH)

    def __del__(self):
        tcsetattr(self.__fd, TCSANOW, self.__old)