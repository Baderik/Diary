def open_image_from_db(binary, name='image.png'):
    if type(binary) is tuple and type(binary[0]) is bytes:
        with open(f'../frontend/image/{name}', 'wb') as img:
            img.write(binary[0])
        return name

    else:
        return 'standard.png'
