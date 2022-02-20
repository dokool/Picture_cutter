from PIL import Image
import os
import pathlib
import img2pdf


def cut_in_half_and_rotate(pic, angle):

    photo_path = pathlib.Path('input', pic)
    photo = Image.open(photo_path)
    width, height = photo.size

    first_photo = photo.crop((0, height / 2, width, height))
    first_photo_output = first_photo.rotate(angle, expand=True)
    first_output_photo_name = "cutted_" + pic
    first_photo_path = pathlib.Path('output', first_output_photo_name)
    first_photo_output.save(first_photo_path)

    second_photo = photo.crop((0, 0, width, height / 2))
    second_photo_output = second_photo.rotate(angle, expand=True)
    second_photo_filename, second_photo_extension = os.path.splitext(pic)
    second_output_photo_name = "cutted_" +\
        second_photo_filename + '_2' + second_photo_extension
    second_photo_path = pathlib.Path('output', second_output_photo_name)
    second_photo_output.save(second_photo_path)
    return (first_photo_path, second_photo_path)


def cut_and_rotate(pic, angle):

    photo_path = pathlib.Path('input', pic)
    photo = Image.open(photo_path)
    width, height = photo.size
    cutted_photo = photo.crop((0, 0, width, height / 2))
    output_photo = cutted_photo.rotate(angle, expand=True)
    output_photo_name = "cutted_" + pic
    first_photo_path = pathlib.Path('output', output_photo_name)
    output_photo.save(first_photo_path)
    return first_photo_path


def convert_to_pdf(pictures, output_filename="pdf_output"):

    output_filename += ".pdf"
    path = pathlib.Path('output', output_filename)
    with open(path, "wb") as f:
        f.write(img2pdf.convert(pictures))
    return path


def main():
    pass


if __name__ == "__main__":
    main()
