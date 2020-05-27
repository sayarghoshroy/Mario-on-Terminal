from colorama import *
import get_ip as take_input
import background as bd
import person
import numpy as np
import time
import os
import subprocess
import time

score = 0

color_map = {
    1: Back.GREEN,
    2: Back.RED,
    3: Back.RED,
    9: Back.MAGENTA,
    6: Fore.WHITE,
    5: Back.YELLOW,
    4: Back.GREEN,
    8: Back.WHITE,
    7: Back.CYAN
}

char_map = {
    1: '-',
    2: 'X',
    3: 'X',
    9: 'X',
    6: 'O',
    5: 'M',
    8: 'V',
    7: '^',
    4: '-'
}


def level_Up_minions():
    for bad_boy in bg.minions:
        bad_boy.increment_move()


def print_colored(n):
    print(color_map.get(n) + str(char_map.get(n)), end='')


def update_score(x, y):
    global score
    for i in range(x, x+4):
        for j in range(y, y+3):
            if bg.total_bg[j, i] == 6:
                score = score + 10
                subprocess.Popen(["aplay", "-q", "./ding.wav"])
            elif bg.total_bg[j, i] == 8:
                score = score + 500
                subprocess.Popen(["aplay", "-q", "./ding.wav"])


def check_boss():
    if bg.boss.get_state() == 0:
        return 1
    X = bg.boss.get_X()
    Y = bg.boss.get_Y()
    if bg.total_bg[Y, X] == 5 or bg.total_bg[Y, X+3] == 5 or bg.total_bg[Y+3, X] == 5 or bg.total_bg[Y+3, X+3] == 5:
        return -1
    else:
        return 1


def update_enemies():
    for bad_boy in bg.minions:
        l = bad_boy.get_left_limit()
        r = bad_boy.get_right_limit()
        move = bad_boy.get_movement()
        x = bad_boy.get_X()
        if x + move < l or x + move > r:
            move = move * (-1)
            bad_boy.set_movement(move)
        bg.total_bg[27:30, x:x+4] = np.zeros((3, 4), dtype=int)
        x = x + move
        bad_boy.set_X(x)
        if bg.total_bg[27, x] == 5 or bg.total_bg[27, x+4] == 5:
            return -1
        bg.total_bg[27:30, x:x+4] = 9
    return 1


def find_collisions():
    for bad_boy in bg.minions:
        l = bad_boy.get_left_limit()
        r = bad_boy.get_right_limit()
        move = bad_boy.get_movement()
        x = bad_boy.get_X()
        x = x + move
        if bg.total_bg[27, x] == 5 or bg.total_bg[27, x+4] == 5:
            return -1
    return 1


def find_and_kill_enemy(x):
    global score
    for bad_boy in bg.minions:
        pos = bad_boy.get_X()
        if (x <= pos and pos <= (x+3)) or (x <= (pos+3) and (pos+3) <= (x+3)):
            bg.total_bg[27:30, pos:pos+4] = 0
            bg.minions.remove(bad_boy)
            subprocess.Popen(["aplay", "-q", "./ding.wav"])
            score = score + 1000
            break


def activate_jump():
    global jump_active
    global jump_state

    x = player.get_X()
    y = player.get_Y()
    if (bg.total_bg[y+3, x] == 1 or bg.total_bg[y+3, x+4] == 1 or bg.total_bg[y+3, x] == 4 or bg.total_bg[y+3, x+4] == 4) and jump_active == 0:
        # you can begin the jump
        subprocess.Popen(["aplay", "-q", "./jump.wav"])
        jump_active = 1
        jump_state = 0


def find_height():
    global jump_active
    global jump_state
    global jump_states

    x = player.get_X()
    y = player.get_Y()

    if jump_active == 0:
        if bg.total_bg[y+3, x] == 0 and bg.total_bg[y+3, x+3] == 0:
            jump_active = 1
            jump_state = 6
        else:
            return y

    if jump_state == 0 and (bg.total_bg[y-1, x] == 4 or bg.total_bg[y-1, x+3] == 4):
        jump_active = 0
        return y

    if (bg.total_bg[y+3, x] == 4 or bg.total_bg[y+3, x+3] == 4) and jump_state > 0:
        jump_active = 0
        return y

    bg.total_bg[y:y+3, x:x+4] = np.zeros((3, 4), dtype=int)

    y = y - jump_states[jump_state]
    player.set_Y(y)
    jump_state = jump_state + 1

    if bg.total_bg[y, x] == 2 or bg.total_bg[y, x+3] == 2:
        return -1

    if bg.total_bg[y+1, x] == 9 or bg.total_bg[y+1, x+3] == 9 or bg.total_bg[y, x+3] == 9 or bg.total_bg[y, x] == 9:
        find_and_kill_enemy(x)

    if bg.total_bg[y+4, x] == 3 or bg.total_bg[y+4, x+3] == 3:
        return -10

    if jump_state == 7:
        jump_active = 0
    return y


# Initializing Game States

level = 1
go_on = 1

jump_states = [4, 2, 1, 0, -1, -2, -4]
jump_state = 0
jump_active = 0

while level <= 2:
    if go_on == 0:
        break
    go_on = 0

    bg = bd.background()
    ip = take_input.Input()
    player = person.Mario(2, 27)

    # generating mario
    bg.total_bg[27:30, 2:6] = 5

    # specifying screen display portions
    left_end = 0
    right_end = 160
    mid = (int)((left_end + right_end) / 2)

    if level == 2:
        level_Up_minions()
        color_map[5] = Back.BLUE

    process_id = (subprocess.Popen(["aplay", "-q", "./sound.wav"]))
    boss_active = 0

    while(1):

        y = player.get_Y()
        x = player.get_X()

        if x > 831 and boss_active == 0:
            bg.boss.activate()
            boss_active = 1
            if level == 2:
                bg.boss.decrement_contained()

        check = find_collisions()

        if bg.boss.get_state() == 1:
            bg.total_bg[bg.boss.get_Y():(bg.boss.get_Y()+4),
                        bg.boss.get_X():(bg.boss.get_X()+4)] = 0
            bg.boss.update(x, y)
            bg.total_bg[bg.boss.get_Y():(bg.boss.get_Y()+4),
                        bg.boss.get_X():(bg.boss.get_X()+4)] = 3

        if ip.checkStream() == True:
            key = ip.getFromStream()

            if key == 'w':
                activate_jump()
                # jump up

            elif key == 'a':
                x = player.get_X()
                y = player.get_Y()

                bg.total_bg[y:y+3, x:x+4] = np.zeros((3, 4), dtype=int)
                if x-3 > left_end and bg.total_bg[y, x-3] != 2 and bg.total_bg[y, x-6] != 2:
                    x = x-3
                    player.set_X(x)
                    # check for items collected
                    update_score(x, y)
                    # go left

            elif key == 'd':
                x = player.get_X()
                y = player.get_Y()

                bg.total_bg[y:y+3, x:x+4] = np.zeros((3, 4), dtype=int)
                if bg.total_bg[y, x+3] != 2 and bg.total_bg[y, x+6] != 2:
                    x = x+3
                if x > mid and x < 860:
                    left_end = left_end + x - mid
                    right_end = right_end + x - mid
                    mid = x
                player.set_X(x)
                # check for items collected
                update_score(x, y)
                # go right

            elif key == 'q':
                level = 100
                process_id.kill()
                print("Bye Bye")
                break
                # end gameplay

        ip.clearStream()

        check_again = update_enemies()

        x = player.get_X()
        y = find_height()
        update_score(x, y)
        flag = 0
        # check if the player has landed on the fiery pipe
        if y == -1:
            flag = 1
            y = player.get_Y()

        elif y == -10:
            flag = 2
            y = player.get_Y()

        bg.total_bg[y:(y+3), x:(x+4)] = 5

        battle_result = check_boss()

        os.system('clear')

        for j in range(0, 35):
            for i in range(left_end, right_end):
                if bg.total_bg[j, i] != 0:
                    print_colored(bg.total_bg[j, i])
                else:
                    if j > 25:
                        if level == 1:
                            print(Back.BLUE + " ", end='')
                        else:
                            print(Back.YELLOW + " ", end='')
                    else:
                        print(" ", end='')
                print(Style.RESET_ALL, end='')

            print("")
        print("")
        print("Score : ", score)
        print("You only have ONE LIFE", flush=True)

        if flag == 2:
            # the boss has been hit
            subprocess.Popen(["aplay", "-q", "./ding.wav"])
            time.sleep(0.8)
            bg.total_bg[bg.boss.get_Y():(bg.boss.get_Y()+4),
                        bg.boss.get_X():(bg.boss.get_X()+4)] = 0
            x = player.get_X()
            y = player.get_Y()
            bg.total_bg[y:y+3, x:x+4] = np.zeros((3, 4), dtype=int)
            bg.boss.set_X(905)
            bg.boss.set_Y(26)
            player.set_X(831)
            player.set_Y(27)
            jump_state = 0
            jump_active = 0
            bg.boss.update_lives()
            if bg.boss.get_lives() == 0:
                bg.boss = 1
                score = score + 10000
                go_on = 1

                if level == 2:
                    print("U win!")
                    print("Final Score : ", score)
                else:
                    print("You Finished Level 1. Get Ready for Level 2")
                process_id.kill()
                ip = 0
                subprocess.Popen(["aplay", "-q", "./win.wav"])
                time.sleep(7)
                level = level + 1
                break

        if (y == 27 and (bg.total_bg[y+4, x] == 0 or bg.total_bg[y+4, x+3] == 0)) or y == -1 or flag == 1 or check == -1 or check_again == -1 or battle_result == -1 or (bg.total_bg[y+3, x] == 2 or bg.total_bg[y+3, x+3] == 2):
            print("Dead :(")
            process_id.kill()
            subprocess.Popen(["aplay", "-q", "./dead.wav"])
            break

        time.sleep(0.2)