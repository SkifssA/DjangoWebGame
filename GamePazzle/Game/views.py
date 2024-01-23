from django.shortcuts import render
from .forms import ImageForm
from django.http import HttpResponseRedirect
import os
import shutil
import PIL
from .models import Image


# Create your views here.
def game(req, key_id):
    open_img = list(Image.objects.filter(id=key_id).values_list('file'))[0][0]
    img = PIL.Image.open(f'media/{open_img}')
    type_file = open_img[open_img.find('.') + 1:]
    w, h = img.size
    w_n, h_n = w + (0 if w % 100 == 0 else (100 - w % 100)), h + (0 if h % 100 == 0 else (100 - h % 100))
    print(w_n, h_n)
    if w_n != w or h_n != h:
        img = img.resize((w_n, h_n))
        img.save(f'media/{open_img}')
        img = PIL.Image.open(f'media/{open_img}')
        w, h = w_n, h_n
    shutil.rmtree('Game/static/GamePuzzle/img')
    os.mkdir('Game/static/GamePuzzle/img')
    q = 1
    for i in range(0, h, 100):
        for j in range(0, w, 100):
            cell_img = img.crop((j, i, j + 100, i + 100))
            cell_img.save(f'Game/static/GamePuzzle/img/{q}.{type_file}')
            q += 1

    img = PIL.Image.open(f'Game/static/GamePuzzle/img/1.{type_file}')
    w_cell, h_cell = img.size
    width = w // 100
    data = {
        'width': width,
        'files': len(os.listdir(path='Game/static/GamePuzzle/img')),
        'width_cell': w_cell,
        'height_cell': h_cell,
        'type_file': type_file,
    }
    return render(req, 'GamePuzzle/main_game.html', data)


def upload_img(req):
    if req.method == 'POST':
        form = ImageForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            open_img = list(Image.objects.filter(name=req.POST['name']).values_list('id'))[0][0]
            return HttpResponseRedirect(f'game&={open_img}')
    else:
        form = ImageForm
    return render(req, 'GamePuzzle/upload.html', {'form': form})


def show_all_img(req):
    img = Image.objects.all()
    return render(req, 'GamePuzzle/all_img.html', {'img': img})
