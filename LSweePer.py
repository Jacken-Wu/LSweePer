import pygame
import sys
import time
import random
import os

pygame.init()

gray = 200, 200, 200                                 # 开始背景颜色
black = 0, 0, 0               # 字体

title = pygame.image.load('others/title.png')
size_text = pygame.image.load('others/size_text.png')
size_30 = pygame.image.load('choice/size_30.png')
size_40 = pygame.image.load('choice/size_40.png')
mask_layer = pygame.image.load('background/mask_layer.png')
black_mask = pygame.image.load('background/black_mask.png')

easy = pygame.image.load('choice/easy.png')
middle = pygame.image.load('choice/middle.png')
hard = pygame.image.load('choice/hard.png')
exit0 = pygame.image.load('choice/exit.png')
once_again = pygame.image.load('choice/once_again.png')
boom = pygame.image.load('others/BOOM.png')
win = pygame.image.load('others/WIN.png')
menu = pygame.image.load('choice/menu.png')
record0 = pygame.image.load('choice/record.png')
more = pygame.image.load('choice/more.png')

flag_sound = pygame.mixer.Sound('sound/flag.wav')
flag_sound.set_volume(0.5)
open_sound = pygame.mixer.Sound('sound/open.wav')
open_sound.set_volume(0.5)
boom_sound = pygame.mixer.Sound('sound/boom.wav')

names = locals()


def create_mines(x_input, y_input):  # 生成雷
    while len(mines_list) < mines_num:
        x_mine = random.randint(0, mines_x_around - 1)
        y_mine = random.randint(0, mines_y_around - 1)
        mine_coordinate = (x_mine, y_mine)
        if mine_coordinate != (x_input, y_input) and mine_coordinate not in mines_list:
            mines_list.append(mine_coordinate)


def open_block(x_input, y_input):  # 翻开
    if 0 <= x_input < mines_x_around and 0 <= y_input < mines_y_around and (x_input, y_input) not in flag_list:
        if (x_input, y_input) in list0 and (x_input, y_input) not in opened_list:
            need_openaround_list.append((x_input, y_input))

        if (x_input, y_input) not in opened_list:
            opened_list.append((x_input, y_input))

        for list_num in range(9):
            if (x_input, y_input) in names['list%d' % list_num]:
                names['have_opened_list%d' % list_num].append((x_input, y_input))


def open_blocks():  # 自动翻开该翻开的方块
    while len(need_openaround_list) != 0:
        for coordinate in need_openaround_list:
            need_openaround_list.remove(coordinate)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x_open = coordinate[0] + i
                    y_open = coordinate[1] + j
                    open_block(x_open, y_open)


def update_screen():  # 游戏的显示更新
    screen.blit(background_1, (mod, 0))
    screen.blit(mask_layer, (0, 0))
    for coordinate in all_list:
        if coordinate in flag_list:
            x_screen = coordinate[0] * block_size
            y_screen = coordinate[1] * block_size
            screen.blit(flag, (x_screen, y_screen))

        elif coordinate in opened_list:
            x_screen = coordinate[0] * block_size
            y_screen = coordinate[1] * block_size
            screen.blit(background_2, (x_screen, y_screen), (x_screen - mod, y_screen, block_size, block_size))
            screen.blit(mask_layer, (x_screen, y_screen), (x_screen, y_screen, block_size, block_size))

        else:
            x_screen = coordinate[0] * block_size
            y_screen = coordinate[1] * block_size
            screen.blit(mask_layer, (x_screen, y_screen), (x_screen, y_screen, block_size, block_size))
            screen.blit(blockup, (x_screen, y_screen))

    for list_num in range(9):
        for coordinate in names['have_opened_list%d' % list_num]:
            x_screen = coordinate[0] * block_size
            y_screen = coordinate[1] * block_size
            screen.blit(names['blockopen_%d' % list_num], (x_screen, y_screen))


title_font = pygame.font.Font('ARIALN.TTF', 30)
pygame.mixer.music.load('sound/bgm.wav')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

while True:
    background_1 = pygame.image.load('background/background_1.png')
    background_2 = pygame.image.load('background/background_2.png')

    blockup = pygame.image.load('mineblock/blockup.png')
    blockready = pygame.image.load('mineblock/blockready.png')
    blockdown = pygame.image.load('mineblock/blockdown.png')
    flag = pygame.image.load('mineblock/flag.png')
    mine = pygame.image.load('mineblock/mine.png')

    blockopen_0 = pygame.image.load('mineblock/blockopen_0.png')
    blockopen_1 = pygame.image.load('mineblock/blockopen_1.png')
    blockopen_2 = pygame.image.load('mineblock/blockopen_2.png')
    blockopen_3 = pygame.image.load('mineblock/blockopen_3.png')
    blockopen_4 = pygame.image.load('mineblock/blockopen_4.png')
    blockopen_5 = pygame.image.load('mineblock/blockopen_5.png')
    blockopen_6 = pygame.image.load('mineblock/blockopen_6.png')
    blockopen_7 = pygame.image.load('mineblock/blockopen_7.png')
    blockopen_8 = pygame.image.load('mineblock/blockopen_8.png')

    screen = pygame.display.set_mode((300, 500))         # 选择界面

    running = True
    while running:                                       # 选择方格大小
        screen.fill(gray)
        screen.blit(title, (25, 10))
        screen.blit(size_text, (40, 110))
        screen.blit(size_30, (50, 150))
        screen.blit(size_40, (50, 220))
        screen.blit(record0, (50, 290))
        screen.blit(exit0, (50, 400))

        pygame.display.update()
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
                sys.exit()
            elif 50 < x < 250 and 400 < y < 440 and event.type == pygame.MOUSEBUTTONDOWN:  # 退出
                pygame.quit()
                sys.exit()
            elif 50 < x < 250 and 150 < y < 190 and event.type == pygame.MOUSEBUTTONDOWN:  # 选择30像素大小方块
                block_size = 30

                myfont = pygame.font.Font('ARIALN.TTF', 25)
                font_h = 4

                blockup = pygame.transform.scale(blockup, (30, 30))
                blockready = pygame.transform.scale(blockready, (30, 30))
                blockdown = pygame.transform.scale(blockdown, (30, 30))
                flag = pygame.transform.scale(flag, (30, 30))
                mine = pygame.transform.scale(mine, (30, 30))

                blockopen_0 = pygame.transform.scale(blockopen_0, (30, 30))
                blockopen_1 = pygame.transform.scale(blockopen_1, (30, 30))
                blockopen_2 = pygame.transform.scale(blockopen_2, (30, 30))
                blockopen_3 = pygame.transform.scale(blockopen_3, (30, 30))
                blockopen_4 = pygame.transform.scale(blockopen_4, (30, 30))
                blockopen_5 = pygame.transform.scale(blockopen_5, (30, 30))
                blockopen_6 = pygame.transform.scale(blockopen_6, (30, 30))
                blockopen_7 = pygame.transform.scale(blockopen_7, (30, 30))
                blockopen_8 = pygame.transform.scale(blockopen_8, (30, 30))

                running = False
            elif 50 < x < 250 and 220 < y < 260 and event.type == pygame.MOUSEBUTTONDOWN:  # 选择40像素大小方块
                block_size = 40

                myfont = pygame.font.Font('ARIALN.TTF', 30)
                font_h = 2

                running = False
            elif 50 < x < 250 and 290 < y < 330 and event.type == pygame.MOUSEBUTTONDOWN:  # 选择查看记录
                with open('record.txt', 'w', encoding='UTF_8') as r:
                    with open('data/easy_recording.txt', 'r', encoding='UTF_8') as f:
                        w = f.readlines()
                        r.write('easy:\n')
                        r.writelines(w)
                    with open('data/middle_recording.txt', 'r', encoding='UTF_8') as f:
                        w = f.readlines()
                        r.write('middle:\n')
                        r.writelines(w)
                    with open('data/hard_recording.txt', 'r', encoding='UTF_8') as f:
                        w = f.readlines()
                        r.write('hard:\n')
                        r.writelines(w)
                os.startfile('record.txt')

    screen.fill(gray)
    screen.blit(easy, (50, 100))
    screen.blit(middle, (50, 200))
    screen.blit(hard, (50, 300))
    screen.blit(exit0, (50, 400))

    pygame.display.update()

    front = block_size // 4                              # "left mines"距前方的距离
    back = block_size * 4                                # "time"距后方的距离

    all_list = []
    wined = 0

    running = True
    while running:                                       # 选择难度
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 退出
                pygame.quit()
                sys.exit()
            elif 50 < x < 250 and 400 < y < 440 and event.type == pygame.MOUSEBUTTONDOWN:  # 退出
                pygame.quit()
                sys.exit()
            elif 50 < x < 250 and 100 < y < 140 and event.type == pygame.MOUSEBUTTONDOWN:  # 初级
                mod = - int(block_size * 56 / 15)
                mods = 'easy'
                screen = pygame.display.set_mode((block_size * 8, block_size * 8 + 40))
                for x_1 in range(8):
                    x_3 = x_1 * block_size
                    for y_1 in range(8):
                        y_3 = y_1 * block_size
                        screen.blit(blockup, (x_3, y_3))
                        all_list.append((x_1, y_1))
                mines_x_around = 8
                mines_y_around = 8
                mines_num = 10
                if block_size == 30:
                    background_1 = pygame.transform.scale(background_1, (450, 240))
                    background_2 = pygame.transform.scale(background_2, (450, 240))
                else:
                    background_1 = pygame.transform.scale(background_1, (600, 320))
                    background_2 = pygame.transform.scale(background_2, (600, 320))
                running = False
            elif 50 < x < 250 and 200 < y < 240 and event.type == pygame.MOUSEBUTTONDOWN:  # 中级
                mod = - int(block_size * 112 / 15)
                mods = 'middle'
                screen = pygame.display.set_mode((block_size * 16, block_size * 16 + 40))
                for x_1 in range(16):
                    x_3 = x_1 * block_size
                    for y_1 in range(16):
                        y_3 = y_1 * block_size
                        screen.blit(blockup, (x_3, y_3))
                        all_list.append((x_1, y_1))
                mines_x_around = 16
                mines_y_around = 16
                mines_num = 40
                if block_size == 30:
                    background_1 = pygame.transform.scale(background_1, (900, 480))
                    background_2 = pygame.transform.scale(background_2, (900, 480))
                else:
                    background_1 = pygame.transform.scale(background_1, (1200, 640))
                    background_2 = pygame.transform.scale(background_2, (1200, 640))
                running = False
            elif 50 < x < 250 and 300 < y < 340 and event.type == pygame.MOUSEBUTTONDOWN:  # 高级
                mod = 0
                mods = 'hard'
                screen = pygame.display.set_mode((block_size * 30, block_size * 16 + 40))
                for x_1 in range(30):
                    x_3 = x_1 * block_size
                    for y_1 in range(16):
                        y_3 = y_1 * block_size
                        screen.blit(blockup, (x_3, y_3))
                        all_list.append((x_1, y_1))
                mines_x_around = 30
                mines_y_around = 16
                mines_num = 99
                if block_size == 30:
                    background_1 = pygame.transform.scale(background_1, (900, 480))
                    background_2 = pygame.transform.scale(background_2, (900, 480))
                else:
                    background_1 = pygame.transform.scale(background_1, (1200, 640))
                    background_2 = pygame.transform.scale(background_2, (1200, 640))
                running = False

        pygame.display.update()

    game = True
    while game:
        mines_list = []
        mines_opened_list = []
        empty_list = []
        opened_list = []
        need_openaround_list = []
        flag_list = []
        flag_list_ready = []
        for num in range(9):
            names['list%d' % num] = []
            names['have_opened_list%d' % num] = []

        running = True
        while running:
            update_screen()
            x, y = pygame.mouse.get_pos()
            x_ready = x//block_size
            y_ready = y//block_size

            x_ready_screen = x_ready * block_size
            y_ready_screen = y_ready * block_size

            screen.blit(background_1, (x_ready_screen, y_ready_screen), (x_ready_screen - mod, y_ready_screen, block_size, block_size))
            screen.blit(blockready, (x_ready_screen, y_ready_screen))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif y > block_size * mines_y_around and event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    open_sound.play()
                    screen.blit(background_1, (x_ready_screen, y_ready_screen), (x_ready_screen - mod, y_ready_screen, block_size, block_size))
                    screen.blit(blockdown, (x_ready_screen, y_ready_screen))
                    create_mines(x_ready, y_ready)
                    time_start = time.time()

                    running = False

            screen.blit(black_mask, (0, block_size * mines_y_around))
            pygame.display.update()

        time_end = time.time()
        time_used = round((time_end - time_start), 3)
        time_used_img = myfont.render('time:' + str(time_used) + 's', True, gray)
        screen.blit(time_used_img, (block_size * mines_x_around - back, block_size * mines_y_around + font_h))

        for empty_coordinate in all_list:
            if empty_coordinate not in mines_list:
                empty_list.append(empty_coordinate)
            else:
                continue

            x_empty = empty_coordinate[0]
            y_empty = empty_coordinate[1]
            num = 0

            for i in range(-1, 2):
                for j in range(-1, 2):
                    x_2 = x_empty + i
                    y_2 = y_empty + j
                    if (x_2, y_2) in mines_list:
                        num += 1

            names['list%d' % num].append(empty_coordinate)

        len_empty_list = len(empty_list)
        open_block(x_ready, y_ready)
        open_blocks()

        left_mines = len(mines_list) - len(flag_list)
        left_mines_img = myfont.render('left mines:' + str(left_mines), True, gray)
        screen.blit(left_mines_img, (front, block_size * mines_y_around + font_h))

        running = True
        while running:
            update_screen()
            x, y = pygame.mouse.get_pos()
            x_ready = x//block_size
            y_ready = y//block_size

            x_ready_screen = x_ready * block_size
            y_ready_screen = y_ready * block_size

            if (x_ready, y_ready) in opened_list:
                screen.blit(blockready, (x_ready_screen, y_ready_screen))
            elif (x_ready, y_ready) not in opened_list and (x_ready, y_ready) not in flag_list:
                screen.blit(background_1, (x_ready_screen, y_ready_screen), (x_ready_screen - mod, y_ready_screen, block_size, block_size))
                screen.blit(blockready, (x_ready_screen, y_ready_screen))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (x_ready, y_ready) in opened_list and event.type == pygame.MOUSEBUTTONDOWN:
                    for num in range(9):
                        if (x_ready, y_ready) in names['have_opened_list%d' % num]:
                            flag_num = 0

                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    x_2 = x_ready + i
                                    y_2 = y_ready + j
                                    if (x_2, y_2) in flag_list:
                                        flag_num += 1

                            if flag_num == num:
                                open_sound.play()
                                for i in range(-1, 2):
                                    for j in range(-1, 2):
                                        x_2 = x_ready + i
                                        y_2 = y_ready + j
                                        if (x_2, y_2) in mines_list and (x_2, y_2) not in flag_list:
                                            screen.blit(mine, (x_2, y_2))
                                            running = False
                                        elif (x_2, y_2) not in opened_list and flag_list:
                                            open_block(x_2, y_2)

                                open_blocks()

                if (x_ready, y_ready) not in opened_list and (x_ready, y_ready) not in flag_list and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if (x_ready, y_ready) not in mines_list:
                            open_sound.play()
                        screen.blit(background_1, (x_ready_screen, y_ready_screen), (x_ready_screen - mod, y_ready_screen, block_size, block_size))
                        screen.blit(blockdown, (x_ready_screen, y_ready_screen))
                        open_block(x_ready, y_ready)
                        open_blocks()

                    elif event.button == 3:
                        flag_sound.play()
                        screen.blit(background_1, (x_ready_screen, y_ready_screen), (x_ready_screen - mod, y_ready_screen, block_size, block_size))
                        screen.blit(flag, (x_ready_screen, y_ready_screen))
                        flag_list_ready.append((x_ready, y_ready))

                if (x_ready, y_ready) in mines_list and (x_ready, y_ready) not in flag_list and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        screen.blit(mine, (x_ready_screen, y_ready_screen))
                        opened_list.remove((x_ready, y_ready))
                        running = False

                if (x_ready, y_ready) in flag_list and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        flag_sound.play()
                        flag_list.remove((x_ready, y_ready))

                if len(flag_list_ready) != 0:
                    flag_list.append(flag_list_ready[0])
                    flag_list_ready = []

            left = len_empty_list - len(opened_list)
            left_mines = len(mines_list) - len(flag_list)
            if left == 0:
                running = False
                wined = 1
            time_end = time.time()
            time_used = round((time_end - time_start), 3)
            time_used_img = myfont.render('time:' + str(time_used) + 's', True, gray)
            screen.blit(black_mask, (0, block_size * mines_y_around))
            screen.blit(time_used_img, (block_size * mines_x_around - back, block_size * mines_y_around + font_h))
            left_mines_img = myfont.render('left mines:' + str(left_mines), True, gray)
            screen.blit(left_mines_img, (front, block_size * mines_y_around + font_h))
            pygame.display.update()

        if wined == 1:
            with open('data/' + mods + '_history.txt', 'r', encoding='UTF_8') as h:
                history = h.readlines()[-1]
            new = 0
            if time_used <= float(history):
                new = 1
            if new:
                with open('data/' + mods + '_recording.txt', 'a', encoding='UTF_8') as record:
                    record.write(time.strftime("%Y-%m-%d %H:%I:%S ", time.localtime(time_end)))
                    record.write(str(time_used))
                    record.write(' s\n')
                with open('data/' + mods + '_history.txt', 'a', encoding='UTF_8') as h:
                    h.write(str(time_used))
                    h.write('\n')
            update_screen()
            screen.blit(black_mask, (0, block_size * mines_y_around))
            time_end = time.time()
            time_used = round((time_end - time_start), 3)
            time_used_img = myfont.render('time:' + str(time_used) + 's', True, gray)
            left_mines = len(mines_list) - len(flag_list)
            left_mines_img = myfont.render('left mines:' + str(left_mines), True, gray)
            x_4 = mines_x_around * block_size // 2
            y_4 = mines_y_around * block_size // 2
            x_5 = x_4 - win.get_width() // 2
            y_5 = y_4 - win.get_height() // 2
            screen.blit(win, (x_5, y_5))
            screen.blit(once_again, (x_4 - 100, y_4 + 50))
            screen.blit(exit0, (x_4 - 100, y_4 + 100))
            screen.blit(menu, (20, 20))
            screen.blit(time_used_img, (block_size * mines_x_around - back, block_size * mines_y_around + font_h))
            screen.blit(left_mines_img, (front, block_size * mines_y_around + font_h))

            pygame.display.update()

            running = True
            while running:
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if x_4 - 100 < x < x_4 + 100 and y_4 + 100 < y < y_4 + 140 and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()
                    if x_4 - 100 < x < x_4 + 100 and y_4 + 50 < y < y_4 + 90 and event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                    if 20 < x < 100 and 20 < y < 60 and event.type == pygame.MOUSEBUTTONDOWN:
                        game = False
                        running = False

        else:
            boom_sound.play()
            screen.fill(black)
            screen.blit(background_1, (mod, 0))
            screen.blit(mask_layer, (0, 0))
            for coordinate in all_list:
                if coordinate in mines_list:
                    x_screen = coordinate[0] * block_size
                    y_screen = coordinate[1] * block_size
                    screen.blit(mine, (x_screen, y_screen))

                if coordinate in flag_list:
                    x_screen = coordinate[0] * block_size
                    y_screen = coordinate[1] * block_size
                    screen.blit(flag, (x_screen, y_screen))

                elif coordinate in opened_list:
                    x_screen = coordinate[0] * block_size
                    y_screen = coordinate[1] * block_size
                    screen.blit(background_2, (x_screen, y_screen), (x_screen - mod, y_screen, block_size, block_size))
                    screen.blit(mask_layer, (x_screen, y_screen), (x_screen, y_screen, block_size, block_size))

                else:
                    x_screen = coordinate[0] * block_size
                    y_screen = coordinate[1] * block_size
                    screen.blit(mask_layer, (x_screen, y_screen), (x_screen, y_screen, block_size, block_size))
                    screen.blit(blockup, (x_screen, y_screen))

            for list_num in range(9):
                for coordinate in names['have_opened_list%d' % list_num]:
                    x_screen = coordinate[0] * block_size
                    y_screen = coordinate[1] * block_size
                    screen.blit(names['blockopen_%d' % list_num], (x_screen, y_screen))

            screen.blit(black_mask, (0, block_size * mines_y_around))
            time_end = time.time()
            time_used = round((time_end - time_start), 3)
            time_used_img = myfont.render('time:' + str(time_used) + 's', True, gray)
            left_mines = len(mines_list) - len(flag_list)
            left_mines_img = myfont.render('left mines:' + str(left_mines), True, gray)
            x_4 = mines_x_around * block_size // 2
            y_4 = mines_y_around * block_size // 2
            x_5 = x_4 - boom.get_width() // 2
            y_5 = y_4 - boom.get_height() // 2
            screen.blit(boom, (x_5, y_5))
            screen.blit(once_again, (x_4 - 100, y_4 + 50))
            screen.blit(exit0, (x_4 - 100, y_4 + 100))
            screen.blit(menu, (20, 20))
            screen.blit(time_used_img, (block_size * mines_x_around - back, block_size * mines_y_around + font_h))
            screen.blit(left_mines_img, (front, block_size * mines_y_around + font_h))

            pygame.display.update()

            running = True
            while running:
                x, y = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if x_4 - 100 < x < x_4 + 100 and y_4 + 100 < y < y_4 + 140 and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()
                    if x_4 - 100 < x < x_4 + 100 and y_4 + 50 < y < y_4 + 90 and event.type == pygame.MOUSEBUTTONDOWN:
                        running = False
                    if 20 < x < 100 and 20 < y < 60 and event.type == pygame.MOUSEBUTTONDOWN:
                        game = False
                        running = False
        wined = 0
