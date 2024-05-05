# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

from PIL import Image
import os


def compress_image(infile, mb=2):
    """
    压缩图片为 jpg 格式，压缩质量为 50%，使图片大小小于指定大小
    :param infile: 压缩源文件路径
    :param mb: 压缩目标大小（MB）
    :return: 压缩后的文件大小
    """
    png_size = os.path.getsize(infile)

    if png_size < (mb - 0.1) * 1024 * 1024:
        print("图片小于指定大小，无需压缩", png_size)
        return infile
    else:
        print("图片过大，进入压缩流程", png_size)
        try:
            outfile = os.path.splitext(infile)[0] + ".jpg"
            quality = 50

            while True:
                im = Image.open(infile)
                im = im.convert("RGB")
                im.save(outfile, format="JPEG", quality=quality)

                if os.path.getsize(outfile) < (mb - 0.1) * 1024 * 1024:
                    break
                quality -= 10  # Reduce quality by 10 each time
                if quality < 0:  # Ensure quality doesn't go below 0
                    print("Unable to compress the image to the desired size.")
                    break

                infile = outfile

            return outfile

        except Exception as e:
            print(e)
            return outfile


if __name__ == '__main__':
    # 使用示例
    compress_image('2_富国 screenshot.png', mb=2)
