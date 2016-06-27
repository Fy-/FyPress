# -*- coding: UTF-8 -*-
from PIL import Image
from resizeimage import resizeimage
import os


class FyImage(object):
    sizes = {
        'thumbnail': [150, 150, 'thumbnail'],
        'thumbnail-s': [150, 150, 'tcrop'],
        'thumbnail-lg': [270, 175, 'crop'],
        'medium': [400, 0, 'width'],
        'large': [800, 0, 'width'],
        'featured': [1180, 305, 'contain']
    }

    def __init__(self, src):
        self.src = src
        self.cdir = os.path.dirname(os.path.realpath(self.src))
        self.name = os.path.splitext(os.path.basename(self.src))[0]
        self.ext = os.path.splitext(os.path.basename(self.src))[1]

    @staticmethod
    def allowed_sizes():
        sizes = []
        for size in FyImage.sizes:
            sizes.append(size)

        return sizes

    def generate(self):
        output = []
        for key, size in FyImage.sizes.items():
            output.append(self.resize(size[0], size[1], key, size[2]))

        return output

    def resize(self, width, height, name='', type='width'):
        output = os.path.join(self.cdir, self.name + '-' + str(width) + 'x' + str(height) + '-' + name + self.ext)

        with open(self.src, 'r+b') as f:
            with Image.open(f) as image:
                if type == 'contain':
                    try:
                        result = resizeimage.resize_cover(image, [width, height])
                    except:
                        tmp = resizeimage.resize_contain(image, [width, height])
                        result = resizeimage.resize_cover(tmp, [width, height])

                elif type == 'height':
                    result = resizeimage.resize_height(image, height, validate=False)
                elif type == 'crop':
                    tmp = resizeimage.resize_contain(image, [width + 150, height + 150])
                    result = resizeimage.resize_crop(tmp, [width, height])
                elif type == 'tcrop':
                    tmp = resizeimage.resize_contain(image, [width, height])
                    result = resizeimage.resize_crop(tmp, [width, height])
                elif type == 'thumbnail':
                    result = resizeimage.resize_thumbnail(image, [width, height])
                else:
                    result = resizeimage.resize_width(image, width, validate=False)

                result.save(output, optimize=True)
                return [output, '[{}x{}] {}'.format(width, height, name), self.name + '-' + str(width) + 'x' + str(height) + '-' + name + self.ext, name]


'''
test = FyImage('/home/fy/Dev16/FyPress/fypress/static/uploads/image.jpg')
test.generate()
'''
