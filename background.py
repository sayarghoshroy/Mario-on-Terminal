import random
import numpy as np
import person


class background:
    def __init__(self):
        self.height = 35
        self.width = 1028
        self.total_bg = np.zeros((35, 1028), dtype=int)
        self.minions = []
        # renders the level
        # the moats and treasures are placed at random locations within a certain region
        # such that playability is not compromised

        i = 20
        self.total_bg[30:35, 0:20] = np.ones((5, 20), dtype=int)
        while i <= 750:
            start_moat = random.randint(i, i+50)

            start_coins = random.randint(i+60, i+75)

            start_pipe = random.randint(start_moat+12, i+65)
            self.total_bg[30:35, i:start_moat] = 1
            self.total_bg[30:35, start_moat+6:i+100] = 1
            self.total_bg[20:22, start_coins:start_coins+25] = 6
            self.total_bg[26:30, start_pipe:start_pipe+5] = 2

            mini = person.Minions(start_pipe+10, 27, start_pipe+8, i+90)
            self.total_bg[27:30, start_pipe+10:start_pipe+14] = 9

            self.minions.append(mini)
            start_bridge = random.randint(start_pipe+10, i+75)
            listed = []
            for j in range(0, 11):
                listed.append(4)

            self.total_bg[26, start_bridge:start_bridge+11] = np.matrix(listed)
            self.total_bg[16, start_bridge+5] = 8
            # putting up the gems
            start_cloud = random.randint(i+10, i+70)
            self.total_bg[3:7, start_cloud:start_cloud+18] = [[0, 0, 0, 7, 7, 0, 0, 7, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0],
                                                              [0, 0, 7, 7, 7, 7, 7, 7, 7,
                                                                  7, 7, 7, 7, 7, 7, 0, 0, 0],
                                                              [0, 7, 7, 7, 7, 7, 7, 7, 7,
                                                                  7, 7, 7, 7, 7, 7, 7, 0, 0],
                                                              [0, 0, 7, 7, 0, 7, 7, 7, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0]]
            start_garden = random.randint(i+10, i+70)
            self.total_bg[10:14, start_garden:start_garden+7] = [[1, 1, 1, 1, 1, 1, 1],
                                                                 [0, 1, 1, 1, 1, 1, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0]]
            i = i+100

        self.total_bg[30:35, 830:930] = 1

        self.boss = person.Commander(905, 26, 834, 1014)

        self.total_bg[26:30, 905:909] = 3