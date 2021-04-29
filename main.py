import os
from glitch_effect import ImageGlitcher


def gen_all_single_effects_of_all_image(img_path="pics", out_path="result"):
    src_images = [f for f in os.listdir(img_path)
                  if os.path.isfile(os.path.join(img_path, f)) and not f.startswith('.')]

    for src_image in src_images:
        for effect_i in range(10):
            print('processing ', os.path.join(img_path, src_image), "effect =", effect_i)
            glitcher = ImageGlitcher()
            glitch_img = glitcher.glitch_image(os.path.join(img_path, src_image), gif=True,
                                               effect_type_seq=(effect_i,))
            glitch_img[0].save(os.path.join(out_path, src_image.split('.')[0] + '_' + str(effect_i) + '.gif'),
                               format='GIF',
                               append_images=glitch_img[1:],
                               save_all=True,
                               duration=200,
                               loop=0,
                               compress_level=3)


def gen_effects_of_all_image(img_path="pics", out_path="result", effect_type_seq=(1, )):
    src_images = [f for f in os.listdir(img_path)
                  if os.path.isfile(os.path.join(img_path, f)) and not f.startswith('.')]

    for src_image in src_images:
        print('processing ', os.path.join(img_path, src_image), ", effects =",
              ','.join([str(i) for i in effect_type_seq]))
        glitcher = ImageGlitcher()
        glitch_img = glitcher.glitch_image(os.path.join(img_path, src_image), gif=True,
                                           effect_type_seq=effect_type_seq)
        glitch_img[0].save(
            os.path.join(out_path, src_image.split('.')[0] + '_' + '_'.join([str(k) for k in effect_type_seq]) + '.gif'),
            format='GIF',
            append_images=glitch_img[1:],
            save_all=True,
            duration=200,
            loop=0,
            compress_level=3)


if __name__ == '__main__':
    gen_all_single_effects_of_all_image()
