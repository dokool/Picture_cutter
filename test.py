from PIL import Image
import os
import pathlib
import img2pdf


def cut_in_half_and_rotate(pic):

    photo_path = pathlib.Path('input', pic)
    print("Редактирование: ", photo_path)
    photo = Image.open(photo_path)
    width, height = photo.size

    first_photo = photo.crop((0, height / 2, width, height))
    first_photo_output = first_photo.rotate(270, expand=True)
    first_output_photo_name = "cutted_" + pic
    first_photo_path = pathlib.Path('output', first_output_photo_name)
    first_photo_output.save(first_photo_path)
    print("Сохранено ", first_photo_path)

    second_photo = photo.crop((0, 0, width, height / 2))
    second_photo_output = second_photo.rotate(270, expand=True)
    second_photo_filename, second_photo_extension = os.path.splitext(pic)
    second_output_photo_name = "cutted_" +\
        second_photo_filename + '_2' + second_photo_extension
    second_photo_path = pathlib.Path('output', second_output_photo_name)
    second_photo_output.save(second_photo_path)
    print("Сохранено ", second_photo_path)


def cut_and_rotate(pic):

    photo_path = pathlib.Path('input', pic)
    print("Редактирование: ", photo_path)
    photo = Image.open(photo_path)
    width, height = photo.size
    cutted_photo = photo.crop((0, 0, width, height / 2))
    output_photo = cutted_photo.rotate(270, expand=True)
    output_photo_name = "cutted_" + pic
    output_photo.save(pathlib.Path('output', output_photo_name))
    print("Сохранено ", pathlib.Path('output', output_photo_name))


def convert_to_pdf(pictures):
    while True:
        x = input("Как назвать файл (default: pdf_output): ")
        if x != '' and '+*/#%^><&?/\\}{@:;\'\"|`=!~' not in x:
            output_filename = x + '.pdf'
            break
        elif '+*/#%^><&?/\\}{@:;\'\"|`=!~' in x:
            print("Недопустимые символы в имени файла.")
            continue
        else:
            output_filename = "pdf_output.pdf"
            break

    if pictures:
        print(pictures)
        print('Преобразование в pdf файл...')
        with open(pathlib.Path('output', output_filename), "wb") as f:
            f.write(img2pdf.convert(pictures))
        print('Фотограции преобразованы в pdf файл.')
        print('Результат находится в', pathlib.Path('output', output_filename))
    else:
        print('Нет файлов в папке output.')


def main():

    dir_path = pathlib.Path.cwd()
    path = pathlib.Path(dir_path, "input")
    output_path = pathlib.Path(dir_path, "output")
    pictures = os.listdir(path)
    print('Всего найдено {0} фотографий:'.format(len(pictures)), pictures)

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
        x = input("Вы хотите создать PDF файл из этих фотографий? Y/n: ")
        if x == 'y' or x == "":
            pictures = [str(pathlib.Path('output', x))
                        for x in os.listdir(output_path)
                        if os.path.splitext(x)[1] != '.pdf']
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
                if os.path.splitext(x)[1] != '.pdf':
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
                if os.path.splitext(x)[1] != '.pdf':
                    print('Удаление', pathlib.Path('input', x))
                    os.remove(pathlib.Path('input', x))
            break
        elif x == "n" or x == "":
            break
        else:
            print('Нужно ввести y(YES) или n(NO) (default)')
            continue


if __name__ == "__main__":
    main()

input("Работа завершена. Нажмите ENTER для выхода.")
