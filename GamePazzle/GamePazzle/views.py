from django.shortcuts import render


def main(req):
    return render(req, 'main_web/pattern.html')
