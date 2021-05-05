import random


def get_new_logo_size(_, img_size, scale):
    return int(img_size[0] * 0.1 * scale + random.randint(-5, 5) / 100)


default = {
    'color': 'white',
    'lang': 'eng',
    'size': 2
}

modes = {
    'right_bottom':
        {
            'x': lambda logo_size, img_size, scale:
            int(img_size[0] - get_new_logo_size(logo_size, img_size, scale) - img_size[0] * 0.005),
            'y': lambda logo_size, img_size, scale:
            int(img_size[1] - int(logo_size[1] *
                                  get_new_logo_size(logo_size, img_size, scale) / logo_size[0]) -
                img_size[0] * 0.005),
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.7,
            'button_text': '⌟'
        },
    'left_bottom':
        {
            'x': lambda logo_size, img_size, scale: img_size[0] * 0.005,
            'y': lambda logo_size, img_size, scale:
            int(img_size[1] - int(logo_size[1] *
                                  get_new_logo_size(logo_size, img_size, scale) / logo_size[0]) - img_size[0] * 0.005),
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.7,
            'button_text': '⌞'
        },
    'left_top':
        {
            'x': lambda logo_size, img_size, scale: img_size[0] * 0.005,
            'y': lambda logo_size, img_size, scale: img_size[0] * 0.005,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.7,
            'button_text': '⌜'
        },
    'right_top':
        {
            'x': lambda logo_size, img_size, scale:
            int(img_size[0] - get_new_logo_size(logo_size, img_size, scale) - img_size[0] * 0.005),
            'y': lambda logo_size, img_size, scale: img_size[0] * 0.005,
            'scale': get_new_logo_size,
            'opacity': lambda _, __, ___: 0.7,
            'button_text': '⌝'
        },
    'center':
        {
            'x': lambda logo_size, img_size, scale:
            int((img_size[0] / 2) - ((img_size[0] * (0.2 + 0.1 * scale)) / 2)) + random.randint(-5, 5),
            'y': lambda logo_size, img_size, scale:
            int((img_size[1] / 2) - (logo_size[1] * ((img_size[0] * (0.2 + 0.1 * scale)) / logo_size[0]) / 2)),
            'scale': lambda logo_size, img_size, scale:
            img_size[0] * (0.2 + 0.1 * scale + random.randint(-10, 10) / 500),
            'opacity': lambda _, __, ___: 0.35 + random.randint(-50, 50) / 1000,
            'button_text': '•'
        },
}
