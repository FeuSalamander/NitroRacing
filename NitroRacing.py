from p5 import *
import random
import winsound

timer = -1
cooldown = 0
refresh = 0
speed = 30

started = False
elements = [
    {
        "name": "air",
        "texture": 1,
        "collision": False
    },
    {
        "name": "car",
        "texture": 6,
        "collision": True
    },
    {
        "name": "player",
        "texture": 1,
        "collision": False
    },
    {
        "name": "hole",
        "texture": 7,
        "collision": False
    }

]
weight = [0, 0, 0, 0, 0, 0, 1, 3]
matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
player_cords = 1
line_cords = [256, 400, 550, 678]
sounds = [
    "assets/Stal.wav",
    "assets/kerosene.wav"
]
colors = [[0, 255, 25], [0, 162, 16], [201, 207, 83], [201, 126, 85], [255, 95, 95], [180, 67, 67]]


def paste_main():
    background(assets[0])
    image(assets[1], 1250, 465)


def start():
    global started
    if started:
        return
    started = True
    global timer
    timer = 0
    winsound.PlaySound(sounds[1], winsound.SND_ASYNC)


def end():
    return
    global started
    global cooldown
    global refresh
    global matrix
    global speed
    if not started:
        return
    started = False
    cooldown = 0
    refresh = 0
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    speed = 30
    winsound.PlaySound(sounds[0], winsound.SND_ASYNC)


def clock():
    global refresh
    global cooldown
    background(assets[2])
    if cooldown > 0:
        cooldown -= 1
    if refresh > 1200//speed:
        refresh = 0
        move()
    refresh += 1

    for i in range(4):
        for j in range(10):
            item = matrix[i][j]
            if item == 0:
                continue
            x = 30 + 150 * j
            y = line_cords[i]
            image(assets[elements[item]["texture"]], x, y)

    text(str(speed)+"\nkm/h", 77, 863)


def move():
    for i in range(4):
        for j in range(9):
            if matrix[i][j] == 2:
                if matrix[i][j+1] != 0:
                    end()
                continue
            matrix[i][j] = matrix[i][j + 1]
        r = random.choice(weight)
        matrix[i][9] = r
    global speed
    speed += 1

    if speed < 50:
        fill(colors[0][0], colors[0][1], colors[0][2])
    elif speed < 70:
        fill(colors[1][0], colors[1][1], colors[1][2])
    elif speed < 90:
        fill(colors[2][0], colors[2][1], colors[2][2])
    elif speed < 130:
        fill(colors[3][0], colors[3][1], colors[3][2])
    elif speed < 150:
        fill(colors[4][0], colors[4][1], colors[4][2])
    elif speed < 180:
        fill(colors[5][0], colors[5][1], colors[5][2])
    if speed == 140:
        winsound.PlaySound(sounds[1], winsound.SND_ASYNC)


def load_images():
    global assets
    assets = [load_image("assets/main.jpg"),
              load_image("assets/mustang.png"),
              load_image("assets/road.jpg"),
              load_image("assets/count1.jpg"),
              load_image("assets/count2.jpg"),
              load_image("assets/count3.jpg"),
              load_image("assets/car.png"),
              load_image("assets/hole.png")]


def setup():
    size(1600, 1024)
    background("white")
    title("Nitro Drive")
    load_images()
    global pixel_font
    pixel_font = create_font("assets/font.ttf", 50)
    text_font(pixel_font)
    fill(colors[0][0], colors[0][1], colors[0][2])
    winsound.PlaySound(sounds[0], winsound.SND_ASYNC)


def draw():
    if not started:
        paste_main()
        return
    global timer
    if not timer == -1:
        background(assets[5 - (timer // 60)])
        timer += 1
        if timer >= 2:  # 180
            timer = -1
        return
    clock()


def mouse_released():
    if started:
        return
    if 138 < mouse_x < 436 and 425 < mouse_y < 600:
        start()


def key_pressed():
    global player_cords
    global cooldown
    if not started:
        return
    if key == "UP" and cooldown < 1:
        if player_cords > 0:
            if matrix[player_cords-1][0] != 0:
                if elements[matrix[player_cords-1][0]]["collision"]:
                    return
                else:
                    end()
            matrix[player_cords][0] = 0
            player_cords += -1
            matrix[player_cords][0] = 2
            cooldown = 8
    if key == "DOWN" and cooldown < 1:
        if player_cords < 3:
            if matrix[player_cords+1][0] != 0:
                if elements[matrix[player_cords+1][0]]["collision"]:
                    return
                else:
                    end()
            matrix[player_cords][0] = 0
            player_cords += 1
            matrix[player_cords][0] = 2
            cooldown = 8


if __name__ == "__main__":
    run()
