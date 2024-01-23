from django.shortcuts import render
import random


# Create your views here.
def main(req, w=10, h=10, count_bomb=10):
    pole = [[0 for _ in range(w)] for _ in range(h)]
    i = 0
    while i < count_bomb:
        x, y = random.randint(0, h-1), random.randint(0, w-1)
        if pole[x][y] == 0:
            pole[x][y] = -1
            i += 1
        pass

    for i in range(h):
        for j in range(w):
            b = 0
            for f in range(-1, 2):
                for s in range(-1, 2):
                    if (f != 0 and s != 0) or pole[i][j] != -1:
                        try:
                            if i+f >= 0 and j + s >= 0:
                                if pole[i + f][j + s] == -1:
                                    b += 1
                        except IndexError:
                            pass
            if pole[i][j] != -1:
                pole[i][j] = b

    data = {
        'w': w,
        'h': h,
        'count_bomb': count_bomb,
        'pole': pole,
    }
    return render(req, 'sapper/main_game.html', data)


def setting(req):
    if req.method == 'POST':
        w, h, count_bomb = req.POST['w'], req.POST['h'], req.POST['bomb']
        return main(req, int(h), int(w), int(count_bomb))

    return render(req, 'sapper/setting.html')
