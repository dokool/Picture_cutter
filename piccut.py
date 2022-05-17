import click
import os
import pathlib
import pcut

supported_types = ['.png', '.jpg', '.JPG', '.PNG', '.JPEG', ".jpeg"]


@click.command()
@click.option('--no-cut', '-n', is_flag=True, default=False, show_default=True,
              help='Скопировать фотографии из input в output')
@click.option('--cut-in-half/--right-part-only', '-c/-r', 'cut_type',
              default=True, show_default=True,
              help='Разрезает фотографии из папки input на две части.\n\
                    --right-part-only оставляет только правую часть,\
                    левая удаляется')
@click.option('--angle', '-a', default='right', show_default=True,
              type=click.Choice(['right', 'left', 'no'], case_sensitive=False),
              help='В какую сторону повернуть разраезанные фотографии.')
@click.option('--output-file-name', '-o', 'output_name', default='pdf_output',
              show_default=True, help='Имя выходного файла.')
@click.option('--start-cut', '-s', 'start', is_flag=True, default=False,
              help="Оставляет от первой фотографии только правую сторону.",
              show_default=True)
@click.option('--end-cut', '-e', 'end', is_flag=True, default=False,
              help="Оставляет от последней фотографии только правую сторону.",
              show_default=True)
@click.option('--pdf-convert', '-p', 'convert_to_pdf', is_flag=True,
              default=True, help="Преобразовывает фотографии из папки output \
                                  в pdf файл.",
              show_default=True)
@click.option('--delete', '-d', default='no', show_default=True,
              type=click.Choice(['input', 'output', 'all', 'no'],
                                case_sensitive=False),
              help='Удаляет исходные/промежуточные/все/(не удалять) файлы.')
def pcut_cli(cut_type, angle, output_name, start, end, convert_to_pdf,
             delete, no_cut):
    f"""Программа разрезает и поворачивает фотографии.
        Делает из этих фотографий pdf файл.
        Поддерживает форматы фотографий: {supported_types}
    """
    coinfirmation_text = generate_coinfirmation_text(cut_type, angle,
                                                     output_name,
                                                     convert_to_pdf,
                                                     delete, no_cut)
    click.echo(coinfirmation_text)
    if click.confirm('Вы хотите продолжить?'):
        pass
    else:
        return
    pictures = [el for el in os.listdir("input")
                if os.path.splitext(el)[1] in supported_types]
    num_of_pictures = len(pictures)
    if num_of_pictures:
        click.echo(f'В папке input найдено {num_of_pictures} фотографий:' +
                   str(pictures))
        cli_cut(cut_type, pictures, angle, start, end, no_cut)
    else:
        click.echo('В папке input нет фотографий.')
    out_pictures = [str(pathlib.Path('output', el))
                    for el in os.listdir('output')
                    if os.path.splitext(el)[1] in supported_types]
    num_of_pictures = len(out_pictures)
    if num_of_pictures:
        click.echo(f'В папке output найдено {num_of_pictures} фотографий:' +
                   str(out_pictures))
        if convert_to_pdf:
            path = pcut.convert_to_pdf(out_pictures, output_name)
            click.secho('Сохраняется в ' + str(path), fg='green')
    else:
        click.echo('В папке output нет фотографий.')
    if delete != 'no':
        delete_photo(delete)


def generate_coinfirmation_text(cutType, angle, name, pdf, delete, skip):
    text = ''
    if skip:
        text += 'Скопировать фотографии из input в output. '
    else:
        if cutType:
            text += 'Разрезать фотографии пополам'
        else:
            text += 'Разрезать фотографии, оставив только правую часть'
    if not skip:
        if angle == 'right':
            text += ', повернув их вправо. '
        elif angle == 'left':
            text += ', повернув их влево. '
        else:
            text += '. '
    if pdf:
        text += f'Создать pdf файл в папке output с именем {name}. '
    if delete == 'all':
        text += 'Удалить файлы из input и output.'
    elif delete == 'input':
        text += 'Удалить файлы из input.'
    elif delete == 'output':
        text += 'Удалить файлы из output.'
    return text


def cli_cut(cut_type, pictures, angle, start, end, skip):

    num_of_pictures = len(pictures)
    if skip:
        for pic in pictures:
            path = pcut.copy_photo(pic)
            click.secho(f'{pic} копируется в output', fg='yellow')
        return
    degrees = 0
    if angle == 'right':
        degrees = 270
    elif angle == 'left':
        degrees = 90
    start_of = 0
    end_of = num_of_pictures
    if cut_type:
        if start:
            start_of = 1
            path = pcut.cut_and_rotate(pictures[0], degrees)
            click.secho('Сохраняется в ' + str(path), fg='green')
        if end:
            end_of = -1
            path = pcut.cut_and_rotate(pictures[-1], degrees)
            click.secho('Сохраняется в ' + str(path), fg='green')
        for pic in pictures[start_of:end_of]:
            path1, path2 = pcut.cut_in_half_and_rotate(pic, degrees)
            click.secho('Сохраняется в ' + str(path1), fg='green')
            click.secho('Сохраняется в ' + str(path2), fg='green')
    else:
        for pic in pictures[start_of:end_of]:
            path = pcut.cut_and_rotate(pic, degrees)
            click.secho('Сохраняется в ' + str(path), fg='green')


def delete_photo(delete):
    if delete == 'output':
        delete_output()
    elif delete == 'input':
        delete_input()
    elif delete == 'all':
        delete_input()
        delete_output()


def delete_output():
    for x in os.listdir('output'):
        if os.path.splitext(x)[1] in supported_types:
            click.secho('Удаляется ' + str(pathlib.Path('output', x)),
                        fg='red')
            os.remove(pathlib.Path('output', x))


def delete_input():
    for x in os.listdir('input'):
        if os.path.splitext(x)[1] in supported_types:
            click.secho('Удаляется ' + str(pathlib.Path('input', x)),
                        fg='red')
            os.remove(pathlib.Path('input', x))


if __name__ == "__main__":
    pcut_cli()
