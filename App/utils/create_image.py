# -*- coding:utf-8 -*-
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


def get_image(width=128, height=38, char_length=4, font_file='application01/static/font/font.ttf', font_size=30):
    code = []
    # 创建画布
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        return chr(random.randint(65, 90))

    def rndColor():
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        # 加粗显示
        for j in range(4):
            draw.text([i * width / char_length + j, h], char, font=font, fill=rndColor())

    # 干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 干扰圆
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, width)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 干扰线
    for i in range(10):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # print(''.join(code))
    # img.show()
    return img, ''.join(code)


if __name__ == '__main__':
    get_image()
