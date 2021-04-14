from glitch_effect import ImageGlitcher
from PIL import Image

def test_image_to_gif():
    """
     Example of getting a glitched GIF and saving it
     We use glitch_level = 2 in this example
     Please note you can use any number in between 1 and 10
     Including floats, floats with one or two decimal precision
     will work the best
     We also are making infinitely looping GIFs
     i.e loop = 0
     You may change these to whatever you'd like
    """

    DURATION = 200      # Set this to however many centiseconds each frame should be visible for
    LOOP = 0            # Set this to how many times the gif should loop
    # LOOP = 0 means infinite loop

    # All default params (i.e step = 1, glitch_change = 0, cycle = False, Frames = 23, color_offset = False, scan_lines = False)
    glitch_imgs = glitcher.glitch_image(src_image, 2, gif=True)
    glitch_imgs[0].save('glitch_result/glitched_test_default.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with scan_lines set to true
    glitch_imgs = glitcher.glitch_image(src_image, 2, scan_lines=True, gif=True)
    glitch_imgs[0].save('glitch_result/glitched_test_scan.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with color_offset set to true
    glitch_imgs = glitcher.glitch_image(src_image, 2, color_offset=True, gif=True)
    glitch_imgs[0].save('glitch_result/glitched_test_color.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with 10 frames
    glitch_imgs = glitcher.glitch_image(src_image, 2, gif=True, frames=10)
    glitch_imgs[0].save('glitch_result/glitched_test_frames.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to False
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll just stay at glitch_max for the remaining duration since cycle = False
    glitch_imgs = glitcher.glitch_image(src_image, 2, glitch_change=1, gif=True)
    glitch_imgs[0].save('glitch_result/glitched_test_increment.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by 1 every time, with cycle set to True
    # glitch_amount will reach glitch_max after (glitch_max - glitch_amount)/glitch_change glitches
    # in this case that's 8
    # It'll cycle back to glitch_min after that and keep incrementing by glitch_change again
    glitch_imgs = glitcher.glitch_image(src_image, 2, glitch_change=1, gif=True, cycle=True)
    glitch_imgs[0].save('glitch_result/glitched_test_increment_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with increasing the glitch_amount by -1 every time, with cycle set to True
    # glitch_amount will reach glitch_min after (glitch_min - glitch_amount)/glitch_change glitches
    # in this case that's 1
    # It'll cycle back to glitch_max after that and keep incrementing (actually decrementing, in this case)
    # by glitch_change again
    glitch_imgs = glitcher.glitch_image(src_image, 2, glitch_change=-1, gif=True, cycle=True)
    glitch_imgs[0].save('glitch_result/glitched_test_decrement_cycle.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # Now try with glitching only every 2nd frame
    # There will still be the specified number of frames (23 in this case)
    # But only every 2nd of the frames will be glitched
    glitch_imgs = glitcher.glitch_image(src_image, 2, gif=True, step=2)
    glitch_imgs[0].save('glitch_result/glitched_test_step.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # How about all of the above?
    glitch_imgs = glitcher.glitch_image(src_image, 2, glitch_change=-1, color_offset=True, scan_lines=True, gif=True,
                                        cycle=True, frames=10, step=2)
    glitch_imgs[0].save('glitch_result/glitched_test_all.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)

    # You can also pass an Image object inplace of the path
    # Applicable in all of the examples above
    img = Image.open(src_image)
    glitch_imgs = glitcher.glitch_image(img, 2, glitch_change=-1, color_offset=True, scan_lines=True, gif=True,
                                        cycle=True, frames=10, step=2)
    glitch_imgs[0].save('glitch_result/glitched_test_all_obj.gif',
                        format='GIF',
                        append_images=glitch_imgs[1:],
                        save_all=True,
                        duration=DURATION,
                        loop=LOOP)


def test_image_to_image():
    """
     Example of getting a glitched Image and saving it
     We use glitch_level = 2 in this example
     You may change this to whatever you'd like
    """
    # All default params(i.e color_offset = False, scan_lines = False)
    glitch_img = glitcher.glitch_image(src_image, 2)
    glitch_img.save('glitch_result/glitched_test_default.png')

    # Now try with scan_lines set to true
    glitch_img = glitcher.glitch_image(src_image, 2, scan_lines=True)
    glitch_img.save('glitch_result/glitched_test_scan.png')

    # Now try with color_offset set to true
    glitch_img = glitcher.glitch_image(src_image, 2, color_offset=True)
    glitch_img.save('glitch_result/glitched_test_color.png')

    # Now try glitching with a seed
    # This will base the RNG used within the glitching on given seed
    glitch_img = glitcher.glitch_image(src_image, 2, seed=42)
    glitch_img.save('glitch_result/glitched_test_seed.png')

    # How about all of them?
    glitch_img = glitcher.glitch_image(src_image, 2, seed=42, color_offset=True, scan_lines=True)
    glitch_img.save('glitch_result/glitched_test_all.png')

    # You can also pass an Image object inplace of the path
    # Applicable in all of the examples above
    img = Image.open(src_image)
    glitch_img = glitcher.glitch_image(img, 2, seed=42, color_offset=True, scan_lines=True)
    glitch_img.save('glitch_result/glitched_test_all_obj.png')

if __name__ == '__main__':

    glitcher = ImageGlitcher()
    src_image = 'source.png'
    glitch_level = 1.0


    glitch_img = glitcher.glitch_image(src_image, glitch_level, gif=True, effect=1)
    #glitch_img.show()
    glitch_img[0].save('glitch_result/source_glitch.gif',
                       format='GIF',
                       append_images=glitch_img[1:],
                       save_all=True,
                       duration=200,
                       loop=0,
                       compress_level=3)

    #test_image_to_image()
    #test_image_to_gif()

