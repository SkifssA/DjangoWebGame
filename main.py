import shutil
import os

def main():
    shutil.rmtree('GamePazzle/Game/static/GamePuzzle/img')
    os.mkdir('GamePazzle/Game/static/GamePuzzle/img')
    shutil.rmtree('GamePazzle/media/imgs')
    os.mkdir('GamePazzle/media/imgs')
    os.remove('GamePazzle/db.sqlite3')




if __name__ == '__main__':
    main()