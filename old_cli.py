while True:
        if pictures:
            pass
        else:
            print('Нет файлов в папке input.')
            break
        x = input("Вы хотите отредактировать все эти фотографии?"
                  + "Y/n/c2 (c2-e, c2-s, c2-se): ")
        if x == 'y' or x == "":
            for pic in pictures:
                cut_and_rotate(pic)
            break
        elif x == 'c2':
            for pic in pictures:
                cut_in_half_and_rotate(pic)
            break
        elif x == 'c2-s':
            cut_and_rotate(pictures[0])
            for pic in pictures[1:]:
                cut_in_half_and_rotate(pic)
            break
        elif x == 'c2-e':
            cut_and_rotate(pictures[-1])
            for pic in pictures[:-1]:
                cut_in_half_and_rotate(pic)
            break
        elif x == 'c2-se':
            cut_and_rotate(pictures[0])
            for pic in pictures[1:-1]:
                cut_in_half_and_rotate(pic)
            cut_and_rotate(pictures[-1])
            break
        elif x == "n":
            break
        else:
            print('Нужно ввести y(YES) (default) или n(NO)')
            continue

while True:
        x = 'n'
        pictures = [str(pathlib.Path('output', x))
                    for x in os.listdir('output')
                    if os.path.splitext(x)[1] != '.pdf'
                    and x != '.gitkeep']
        if pictures:
            x = input("Вы хотите создать PDF файл из этих фотографий? Y/n: ")
        else:
            print('Нет файлов в папке output')
        if x == 'y' or x == "":
            convert_to_pdf(pictures)
            break
        elif x == "n":
            break
        else:
            print('Нужно ввести y(YES) (default) или n(NO)')
            continue

while True:
        x = input("Вы хотите удалить временные файлы из папки output? y/N: ")
        if x == 'y':
            for x in os.listdir('output'):
                if os.path.splitext(x)[1] != '.pdf' and x != '.gitkeep':
                    print('Удаление', pathlib.Path('output', x))
                    os.remove(pathlib.Path('output', x))
            break
        elif x == "n" or x == "":
            break
        else:
            print('Нужно ввести y(YES) или n(NO) (default)')
            continue

while True:
    x = input("Вы хотите удалить изначальные файлы из папки input? y/N: ")
    if x == 'y':
        for x in os.listdir('input'):
            if os.path.splitext(x)[1] != '.pdf' and x != '.gitkeep':
                print('Удаление', pathlib.Path('input', x))
                os.remove(pathlib.Path('input', x))
        break
    elif x == "n" or x == "":
        break
    else:
        print('Нужно ввести y(YES) или n(NO) (default)')
        continue