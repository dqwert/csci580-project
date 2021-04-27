import os

from PIL import Image

from glitch_effect import ImageGlitcher

if __name__ == '__main__':
    picture_path = "pics"
    output_path = "result"

    src_images = [f for f in os.listdir(picture_path)
                  if os.path.isfile(os.path.join(picture_path, f)) and not f.startswith('.')]

    for src_image in src_images:
        for single_effect in range(10):
            # src_image = "source.png"
            print('processing: ', os.path.join(picture_path, src_image))
            glitcher = ImageGlitcher()

            glitch_level = 1.0

            glitch_img = glitcher.glitch_image(os.path.join(picture_path, src_image), gif=True,
                                               effect_type_seq=(single_effect,))
            # glitch_img.show()
            glitch_img[0].save(os.path.join(output_path, src_image + '_' + str(single_effect) + '.gif'),
                               format='GIF',
                               append_images=glitch_img[1:],
                               save_all=True,
                               duration=200,
                               loop=0,
                               compress_level=3)