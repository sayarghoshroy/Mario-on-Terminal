class Person:
    def __init__(self, X, Y, height, width):
        self._X = X
        self._Y = Y
        self.height = height
        self.width = width

    def get_X(self):
        return self._X

    def get_Y(self):
        return self._Y

    def set_X(self, X):
        self._X = X

    def set_Y(self, Y):
        self._Y = Y

    def update(self, x, y):
        self.set_X(x)
        self.set_Y(y)


class Mario(Person):
    def __init__(self, X, Y):
        Person.__init__(self, X, Y, 4, 3)


class Enemy(Person):
    def __init__(self, X, Y, l_limit, r_limit, height, width):
        Person.__init__(self, X, Y, height, width)
        self._left_lim = l_limit
        self._right_lim = r_limit
        self._move = 4

    def increment_move(self):
        self._move = self._move + 1

    def get_left_limit(self):
        return self._left_lim

    def get_right_limit(self):
        return self._right_lim

    def get_movement(self):
        return self._move

    def set_movement(self, move):
        self._move = move


class Minions(Enemy):
    def __init__(self, X, Y, l_limit, r_limit):
        Enemy.__init__(self, X, Y, l_limit, r_limit, 4, 3)


class Commander(Enemy):
    def __init__(self, X, Y, l_limit, r_limit):
        Enemy.__init__(self, X, Y, l_limit, r_limit, 4, 4)
        self._lives_left = 3
        self._active = 0
        self._contained = 23

    def decrement_contained(self):
        self._contained = self._contained - 1

    def activate(self):
        self._active = 1

    def get_lives(self):
        return self._lives_left

    def update_lives(self):
        self._lives_left = self._lives_left - 1

    def get_state(self):
        return self._active

    def update(self, x, y):
        if self._active == 1:
            X = self.get_X()
            Y = self.get_Y()

            if X > x:
                X = X - max(2, 4 - self._lives_left)
            else:
                X = X + max(2, 4 - self._lives_left)

            if y < Y + 3 and Y > self._contained:
                Y = Y - 1
            elif Y < 25:
                Y = Y + 1
            self.set_X(X)
            self.set_Y(Y)