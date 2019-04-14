def open_image_from_db(binary, name='image.png'):
    if type(binary) is bytes:
        with open(f'/frontend/image/{name}', 'wb') as img:
            img.write(binary)
        return name

    else:
        return 'standard.png'
