from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import lvl

# Create your views here.
h, w = 20, 11
pole = [[61 for _ in range(h)] for _ in range(w)]
pole_p = [[0 for _ in range(h)] for _ in range(w)]
go_help = []


def p1(q):
    i = 53
    if q[3]:
        i = 53
    elif q[2]:
        i = 53
    elif q[1]:
        i = 60
    elif q[0]:
        i = 60
    return i


def p2(q):
    i = 53
    if q[3] == q[2] == 1:
        i = 53
    if q[0] == q[1] == 1:
        i = 60

    if q[0] == q[3] == 1:
        i = 54
    if q[1] == q[3] == 1:
        i = 70
    if q[0] == q[2] == 1:
        i = 52
    if q[1] == q[2] == 1:
        i = 68
    return i


def go(x, y):
    global pole, pole_p, h, w, go_help
    if pole_p[x][y] == 1:
        q = [pole_p[x + 1][y], pole_p[x - 1][y], pole_p[x][y + 1], pole_p[x][y - 1]]
        if sum(q) == 0:
            pole[x][y] = 53
        elif sum(q) == 2:
            pole[x][y] = p2(q)
        elif sum(q) == 1:
            pole[x][y] = p1(q)

        if q[0] and [x + 1, y] not in go_help:
            go_help.append([x + 1, y])
            go(x + 1, y)
        if q[1] and [x - 1, y] not in go_help:
            go_help.append([x - 1, y])
            go(x - 1, y)
        if q[2] and [x, y + 1] not in go_help:
            go_help.append([x, y + 1])
            go(x, y + 1)
        if q[3] and [x, y - 1] not in go_help:
            go_help.append([x, y - 1])
            go(x, y - 1)
    return pole


@method_decorator(csrf_exempt, name='dispatch')
class CellGen(View):
    def get(self, req, key):
        global pole, pole_p, h, w, go_help
        x, y = list(map(int, key.split('.')))
        pole_p[x][y] = 1

        go_help = []
        pole = go(x, y)
        data = {
            'pole': pole,
        }
        return JsonResponse(data)


def GoOr(enemy, pole):
    i = [0, 0, '']
    y, x = enemy[0], enemy[1]
    if x < 0:
        i[0] = 1
    elif y < 0:
        i[1] = 1
    elif pole[x + 1][y] and enemy[3] != 'u':
        i[0] = 1
        i[2] = 'd'
    elif pole[x - 1][y] and enemy[3] != 'd':
        i[0] = -1
        i[2] = 'u'
    elif pole[x][y + 1] and enemy[3] != 'l':
        i[1] = 1
        i[2] = 'r'
    elif pole[x][y - 1] and enemy[3] != 'r':
        i[1] = -1
        i[2] = 'l'
    if i[0] == i[1] == 0 and i[2] == '':
        i[2] = 'dead'
    return i


@method_decorator(csrf_exempt, name='dispatch')
class EnemyGo(View):
    def get(self, req, key):
        enemy = [[int(i[0]), int(i[1]), int(i[2]), i[3], int(i[4])] if len(i) != 1 else i
                 for i in list(dict(req.GET).values())]
        lvl_go = enemy[0][0]
        enemy = enemy[1:]
        if len(enemy) != 0:
            enemy_new = []
            if len(lvl.lvl['lvl' + lvl_go]['enemy']) > key:
                for i in range(len(enemy)):
                    e = GoOr(enemy[i], pole_p)
                    if e[2] != 'dead' and enemy[i][3] != 'dead':
                        x = enemy[i][0] + e[1]
                        y = enemy[i][1] + e[0]
                        enemy_new.append([x, y, enemy[i][2], e[2], enemy[i][4]])
        else:
            enemy_new = lvl.lvl['lvl' + lvl_go]['enemy'][key]
        data = {
            'enemy': enemy_new,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class Towers(View):
    def get(self, req, key):
        towers = [list(map(int, i)) for i in list(dict(req.GET).values())]
        x, y = list(map(int, key.split('.')))
        if pole_p[x][y] == 0:
            for i, tower in enumerate(towers):
                if tower[0] == x and tower[1] == y:
                    if tower[2] < 2:
                        towers[i][2] += 1
                    break
            else:
                towers.append([x, y, 0, 1])

        data = {
            'towers': towers,
        }
        return JsonResponse(data)


def main(req):
    global pole, pole_p, h, w
    pole_p = lvl.lvl['lvl1']['pole'].copy()
    pole = go(*lvl.lvl['lvl1']['begin'])
    return render(req, 'td/main_game.html', {'h': h, 'w': w, 'pole': pole,
                                             'castle': lvl.lvl['lvl1']['castle']})
