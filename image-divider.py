from PIL import Image, ImageOps
import sys

def main():

    BORDER_PERCENTAGE = 1

    if len(sys.argv) < 2:
        print("Error: Debe proporcionar el nombre del archivo de imagen como argumento.")
        print("Uso: python script.py <nombre_de_archivo> [<numero_de_partes> [<color_del_borde>]]")
        sys.exit(1)

    FILENAME = sys.argv[1]

    if len(sys.argv) > 2:
        try:
            N = int(sys.argv[2])
            if N <= 0:
                raise ValueError
        except ValueError:
            print("Error: El número de partes debe ser un entero positivo.")
            sys.exit(1)
    else:
        N = 3

    if len(sys.argv) > 3:
        BORDER_COLOR = sys.argv[3]
    else:
        BORDER_COLOR = 'black'
    
    try:
        with Image.open(FILENAME) as img:
            img.load()
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo '{FILENAME}'.")
        sys.exit(1)

    width, height = img.size
    BORDER = round(width * BORDER_PERCENTAGE / 100)

    # left, top, right, bottom
    borders = [(BORDER, BORDER, 0, BORDER), (0, BORDER, 0, BORDER), (0, BORDER, BORDER, BORDER)]


    for i in range(N):
        left = i*width//N + BORDER if i == 0 else i*width//N
        right = (i+1)*width//N - BORDER if i == N-1 else (i+1)*width//N

        if i == 0: 
            border_config = borders[0]
        elif i == N-1:
            border_config = borders[2]
        else:
            border_config = borders[1]

        img_part = img.crop((left, BORDER, right, height - BORDER))

        try:
            new_img = ImageOps.expand(img_part, border=border_config, fill=BORDER_COLOR)
        except ValueError:
            print('El color especificado no es correcto.')
            sys.exit(1)

        #new_img.show()

        new_img.save(f'image_{i+1}.jpg')


if __name__ == '__main__':
    main()
