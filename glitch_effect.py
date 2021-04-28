# Adopted from https://github.com/TotallyNotChase/glitch-this

import math
import os
import random
# The shutil module offers a number of high-level operations on files and collections of files.
# In particular, functions are provided which support file copying and removal.
import shutil
# Decimal fixed point and floating point arithmetic
# The decimal module provides support for fast correctly-rounded decimal floating point arithmetic.
# It offers several advantages over the float datatype:
from decimal import getcontext
# Support for type hints (Most fundamental: Any, Union, Tuple, Callable, TypeVar, and Generic).
from typing import List, Optional, Union

import numpy
import numpy as np
# Pillow is the friendly fork of PIL (the Python Imaging Library).
from PIL import Image, ImageSequence, ImageDraw


class ImageGlitcher:

    def __init__(self):
        # Setting up global variables needed for glitching
        self.pixel_tuple_len = 0
        self.img_width, self.img_height = 0, 0
        self.img_mode = 'Unknown'
        self.seed = None

        # Creating 3D arrays for pixel data
        self.inputarr = None
        self.outputarr = None

        # Getting path of temp folders
        self.lib_path = os.path.split(os.path.abspath(__file__))[0]  # get parent dir
        self.gif_dirpath = os.path.join(self.lib_path, 'Glitched GIF')

        # Setting glitch_amount max and min
        self.GLITCH_MAX = 10.0
        self.GLITCH_MIN = 0.1

        self.effects = (
            self.__analog_noise,
            self.__rgb_split,
            self.__tile_jitter,
            self.__screen_jump_effect,
            self.__screen_shake_effect,
            self.__wave_jitter_effect,
            self.__image_block,
            self.__image_block_hsv,
            self.__scan_line,
            self.__line_block,
            self.__color_block,
        )

        self.__scan_line_current_step = 0

        # Return glitched GIF
        # Set up directory for storing glitched images
        # code moved to init for optimization
        if os.path.isdir(self.gif_dirpath):
            shutil.rmtree(self.gif_dirpath)
        os.mkdir(self.gif_dirpath)

    # Returns true if input image is a GIF and/or animated
    @staticmethod
    def __is_gif(img: Union[str, Image.Image]) -> bool:
        # if img is a path str, open it as an Image
        if isinstance(img, str):
            if not os.path.isfile(img):
                return False
            img = Image.open(img)
        index = 0
        # More than one frames means image is animated
        for _ in ImageSequence.Iterator(img):
            index += 1
            if index >= 2:
                return True
        return False

    @staticmethod
    def __open_image(img_path: str) -> Image.Image:
        # Will throw exception if img_path doesn't point to Image
        if img_path.endswith('.gif'):
            # Do not convert GIF file
            return Image.open(img_path)
        elif img_path.endswith('.png'):
            # Convert the Image to RGBA if it's png
            return Image.open(img_path).convert('RGBA')
        else:
            # Otherwise convert it to RGB
            return Image.open(img_path).convert('RGB')

    def __fetch_image(self,
                      src_img: Union[str, Image.Image],
                      gif_allowed: bool
                      ) -> Image.Image:
        """
         The following code resolves whether input was a path or an Image
         Then returns an Image object
         Raises an exception if `img` param is not an Image
        """
        if isinstance(src_img, str) and (gif_allowed or not src_img.endswith('.gif')):
            """
             An str object was passed
             If GIF is not allowed and the Image path is a GIF
             the function will raise an Exception
             If GIF is allowed, any Image path is good to go
            """
            # Sanity Check if the path exists
            if not os.path.isfile(src_img):
                raise FileNotFoundError('Path not found')
            try:
                # Open the image at given path
                img = self.__open_image(src_img)
            except:
                # File is not an Image
                raise Exception('Wrong format')
        elif isinstance(src_img, Image.Image) and (gif_allowed or not self.__is_gif(src_img)):
            """
             An Image object was passed
             If GIF is not allowed and the Image object is a GIF
             the function will raise an Exception
             If GIF is allowed, any Image object is good to go
            """
            if src_img.format == 'GIF':
                # Do not convert GIF file
                return src_img
            elif src_img.format == 'PNG':
                # Convert the Image to RGBA if it's png
                img = src_img.convert('RGBA')
            else:
                # Otherwise convert it to RGB
                img = src_img.convert('RGB')
        else:
            # File is not an Image
            # OR it's a GIF but GIF is not allowed

            # Raise the GENERIC exception here
            raise Exception('Wrong format')
        return img

    def glitch_image(self,
                     src_img: Union[str, Image.Image],
                     seed: Optional[Union[int, float]] = None,
                     glitch_change: Union[int, float] = 0.0,
                     gif: bool = False,
                     cycle: bool = False,
                     frames: int = 23,
                     step: int = 1,
                     effect_type_seq=()
                     ) -> Union[Image.Image, List[Image.Image]]:
        """
         Sets up values needed for glitching the image
         Returns created Image object if gif=False
         Returns list of Image objects if gif=True
         PARAMETERS:-
         src_img: Either the path to input Image or an Image object itself
         glitch_amount: Level of glitch intensity, [0.1, 10.0] (inclusive)
         glitch_change: Increment/Decrement in glitch_amount after every glitch
         cycle: Whether or not to cycle glitch_amount back to glitch_min or glitch_max
                if it over/underflows
         color_offset: Specify True if color_offset effect should be applied
         scan_lines: Specify True if scan_lines effect should be applied
         gif: True if output should be ready to be saved as GIF
         frames: How many glitched frames should be generated for GIF
         step: Glitch every step'th frame, defaults to 1 (i.e all frames)
         seed: Set a random seed for generating similar images across runs,
               defaults to None (random seed).
        """

        # Sanity checking the inputs
        if not ((isinstance(glitch_change, float)
                 or isinstance(glitch_change, int))
                and -self.GLITCH_MAX <= glitch_change <= self.GLITCH_MAX):
            raise ValueError(
                f'glitch_change parameter must be a number between {-self.GLITCH_MAX} and {self.GLITCH_MAX}, inclusive')
        if seed and not (isinstance(seed, float) or isinstance(seed, int)):
            raise ValueError(
                f'seed parameter must be a number')
        if not (frames > 0 and isinstance(frames, int)):
            raise ValueError(
                'frames param must be a positive integer value greater than 0')
        if not step > 0 or not isinstance(step, int):
            raise ValueError(
                'step parameter must be a positive integer value greater than 0')
        if not isinstance(cycle, bool):
            raise ValueError('cycle param must be a boolean')
        if not isinstance(gif, bool):
            raise ValueError('gif param must be a boolean')

        self.seed = seed
        if self.seed:
            # Set the seed if it was given
            self.__reset_seed()

        try:
            # Get Image, whether input was an str path or Image object
            # GIF input is NOT allowed in this method
            img = self.__fetch_image(src_img, gif_allowed=False)
        except FileNotFoundError:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise FileNotFoundError(f'No image found at given path: {src_img}')
        except:
            # Throw DETAILED exception here (Traceback will be present from previous exceptions)
            raise Exception(
                'File format not supported - must be a non-animated image file')

        # Fetching image attributes
        self.pixel_tuple_len = len(img.getbands())
        self.img_width, self.img_height = img.size
        self.img_mode = img.mode

        # Assigning the 3D arrays with pixel data
        self.inputarr = np.asarray(img)
        self.outputarr = np.array(img)

        # Glitching begins here
        if not gif:
            # Return glitched image
            return self.__apply_glitch(effect_type_seq)

        # Return glitched GIF
        # Set up directory for storing glitched images
        # code moved to init for optimization

        # Set up decimal precision for glitch_change
        original_prec = getcontext().prec
        getcontext().prec = 4

        glitched_imgs = []
        for i in range(frames):
            """
             * Glitch the image for n times
             * Where n is 0,1,2...frames
             * Save the image the in temp directory
             * Open the image and append a copy of it to the list
            """
            if not i % step == 0:
                # Only every step'th frame should be glitched
                # Other frames will be appended as they are
                glitched_imgs.append(img.copy())
                continue
            glitched_img = self.__apply_glitch(effect_type_seq)
            file_path = os.path.join(self.gif_dirpath, 'glitched_frame.png')
            # glitched_img.save(file_path, compress_level=3)
            glitched_imgs.append(glitched_img.copy())

        # Set decimal precision back to original value
        getcontext().prec = original_prec
        # Cleanup
        shutil.rmtree(self.gif_dirpath)
        return glitched_imgs

    def __apply_glitch(self, effect_type_seq=()) -> Image.Image:

        if self.seed:
            # Get the same channels on the next call, we have to reset the rng seed
            # as the previous loop isn't fixed in size of iterations and depends on glitch amount
            self.__reset_seed()

        image = Image.fromarray(self.outputarr, self.img_mode)
        outputarr = self.outputarr

        if len(effect_type_seq) > 0:
            for i in effect_type_seq:
                image = self.effects[i](image)
                self.outputarr = np.array(image)

        self.outputarr = outputarr


        # Creating glitched image from output array
        # return Image.fromarray(self.outputarr, self.img_mode)
        return image

    def __reset_seed(self, offset: int = 0):
        """
        Calls random.seed() with self.seed variable
        offset is for looping and getting new positions for each iteration that contains the
        previous one, otherwise we would get the same position on every loop and different
        results afterwards on non fixed size loops
        """
        random.seed(self.seed + offset)

    def clamp_int(self, x, max_, min_=0):
        if x < min_:
            return int(min_)
        elif x > max_:
            return int(max_)
        else:
            return int(x)

    def __analog_noise(self, image: Image.Image, mean=0, stddev=50) -> Image.Image:
        noise = np.random.randn(*self.outputarr.shape) * stddev
        np.clip(noise, 0, 255, out=noise).astype('uint16')

        np.add(self.outputarr.astype('uint16'), noise, out=noise)
        return Image.fromarray(np.clip(noise, 0, 255).astype('uint8'), self.img_mode)

    def __rgb_split(self, image: Image.Image, mean=0, stddev=0.01) -> Image.Image:
        width = self.img_width
        height = self.img_height

        x_offset = random.normalvariate(mean, stddev) * width
        y_offset = random.normalvariate(mean, stddev) * height

        frame = self.outputarr.copy()

        for y in range(self.img_height):
            for x in range(self.img_width):
                frame[y][x][0] = self.outputarr[self.clamp_int(y + y_offset, height - 1)][self.clamp_int(x + x_offset, width - 1)][0]
                frame[y][x][2] = self.outputarr[self.clamp_int(y - y_offset, height - 1)][self.clamp_int(x - x_offset, width - 1)][2]

        return Image.fromarray(frame, self.img_mode)

    def __tile_jitter(self, image: Image.Image, strip_height=50, mean=0, stddev=0.1) -> Image.Image:
        x_offset = random.normalvariate(mean, stddev) * image.width
        original = image.copy()

        width = image.width
        height = image.height
        prev_strip = -1

        for y in range(height):
            current_strip = y // strip_height
            is_jittered = current_strip % 2 == 0
            if prev_strip != current_strip:
                x_offset = int(random.normalvariate(mean, stddev) * image.width)
            prev_strip = current_strip
            for x in range(width):
                if is_jittered:
                    image.putpixel((x, y), original.getpixel(((x + x_offset) % width, y)))
        return image

    def __screen_jump_effect(self, image: Image.Image, vertical=True):
        if not vertical:
            start_y = 0
            stop_y = self.img_height

            # For copy
            start_x = int(0.15 * self.img_width)
            # For paste
            stop_x = self.img_width - start_x

            left_chunk = self.outputarr[start_y:stop_y, start_x:]
            wrap_chunk = self.outputarr[start_y:stop_y, :start_x]
            self.outputarr[start_y:stop_y, :stop_x] = left_chunk
            self.outputarr[start_y:stop_y, stop_x:] = wrap_chunk
        else:
            start_x = 0
            stop_x = self.img_width

            # For copy
            start_y = int(0.15 * self.img_height)
            # For paste
            stop_y = self.img_height - start_y

            up_chunk = self.outputarr[start_y:, start_x:stop_x]
            wrap_chunk = self.outputarr[:start_y, start_x:stop_x]
            self.outputarr[:stop_y, start_x:stop_x] = up_chunk
            self.outputarr[stop_y:, start_x:stop_x] = wrap_chunk

        return Image.fromarray(self.outputarr, self.img_mode)

    def __screen_shake_effect(self, image: Image.Image, amplitude=5):
        start_y = 0
        stop_y = self.img_height

        # For copy
        offset = random.random()
        if offset < 0.5:
            offset = offset / amplitude
        else:
            offset = 1 - offset / amplitude

        start_x = int(offset * self.img_width)
        # For paste
        stop_x = self.img_width - start_x
        shake_array = self.outputarr.copy()

        left_chunk = self.outputarr[start_y:stop_y, start_x:]
        wrap_chunk = self.outputarr[start_y:stop_y, :start_x]
        shake_array[start_y:stop_y, :stop_x] = left_chunk
        shake_array[start_y:stop_y, stop_x:] = wrap_chunk

        return Image.fromarray(shake_array, self.img_mode)

    def __wave_jitter_effect(self, image: Image.Image, wave=10, amplitude=10):
        height = self.img_height
        vertical_range = height / wave
        offset = random.randint(0, self.img_height)
        shake_array = self.outputarr.copy()
        for i in range(height):
            omega = ((i + offset) % vertical_range) / vertical_range * 2 * math.pi
            shift = int(amplitude * math.sin(omega))

            start_y = i
            stop_y = i + 1

            if shift > 0:
                start_x = shift
                stop_x = self.img_width - shift
            elif shift < 0:
                shift *= -1
                start_x = self.img_width - shift
                stop_x = shift
            else:
                continue

            left_chunk = self.outputarr[start_y:stop_y, start_x:]
            wrap_chunk = self.outputarr[start_y:stop_y, :start_x]
            shake_array[start_y:stop_y, :stop_x] = left_chunk
            shake_array[start_y:stop_y, stop_x:] = wrap_chunk
        return Image.fromarray(shake_array, self.img_mode)

    def __image_block(self, image: Image.Image, color_effect=False,
                      num_mean=10, num_stddev=10,
                      size_mean=0.09, size_stddev=0.03,
                      offset_mean=0, offset_stddev=0.05) -> Image.Image:
        original = image.copy()
        block_num = int(random.normalvariate(num_mean, num_stddev))
        height = image.height
        width = image.width

        colors = ["#b4b2b5", "#dfd73f", "#6ed2dc", "#66cf5d", "#c542cb", "#d0535e", "#3733c9"]

        for _ in range(block_num):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)

            len_x = int(random.normalvariate(size_mean, size_stddev) * width * 3)
            len_y = int(random.normalvariate(size_mean, size_stddev) * height)

            offset_x = int(random.normalvariate(offset_mean, offset_stddev) * width)
            offset_y = int(random.normalvariate(offset_mean, offset_stddev) * height)

            color = np.random.randint(3, size=4)

            if color_effect:
                for j in range(y, y + len_y):
                    for i in range(x, x + len_x):
                        image.putpixel((self.clamp_int(i, width - 1, 0), self.clamp_int(j, height - 1, 0)),
                                       tuple(min(m * n, 255) for (m, n) in zip(color,
                                                                               original.getpixel(
                                                                                   ((i + offset_x) % width,
                                                                                    (j + offset_y) % height)))))
            else:
                for j in range(y, y + len_y):
                    for i in range(x, x + len_x):
                        image.putpixel((self.clamp_int(i, width - 1, 0), self.clamp_int(j, height - 1, 0)),
                                       original.getpixel(((i + offset_x) % width, (j + offset_y) % height)))
        return image

    def __image_block_hsv(self, image: Image.Image,
                      num_mean=8, num_stddev=3,
                      size_mean=0.09, size_stddev=0.03,
                      offset_mean=0, offset_stddev=0.05) -> Image.Image:
        arr = np.array(image.convert(mode="HSV"))
        ori = image.copy()
        block_num = int(random.normalvariate(num_mean, num_stddev))

        for _ in range(block_num):
            x = random.randint(0, self.img_width - 1)
            y = random.randint(0, self.img_height - 1)

            len_x = int(random.normalvariate(size_mean, size_stddev) * self.img_width * 5)
            len_y = int(random.normalvariate(size_mean, size_stddev) * self.img_height)

            offset_x = int(random.normalvariate(offset_mean, offset_stddev) * self.img_width)
            offset_y = int(random.normalvariate(offset_mean, offset_stddev) * self.img_height)

            color = (np.random.randn(4) + 1).astype('uint16')

            for j in range(y, y + len_y):
                for i in range(x, x + len_x):
                    image.putpixel((self.clamp_int(i, self.img_width - 1, 0), self.clamp_int(j, self.img_height - 1, 0)),
                                   tuple(min(m * n, 255) for (m, n) in zip(color,
                                                                           ori.getpixel(
                                                                               ((i + offset_x) % self.img_width,
                                                                                (j + offset_y) % self.img_height)))))
        return image

    def __scan_line(self, image: Image.Image, offset_ratio=0.1, total_step=30):
        self.__scan_line_current_step = (self.__scan_line_current_step + 1) % total_step

        amplitude = math.sin(self.__scan_line_current_step / total_step * 2 * math.pi)

        width = self.img_width
        height = self.img_height
        shake_array = self.outputarr.copy()
        for i in range(height):
            shift = int(
                amplitude * self.clamp_int(int(random.normalvariate(0, int(width * offset_ratio))), width, -width))
            start_y = i
            stop_y = i + 1

            if shift > 0:
                start_x = shift
                stop_x = self.img_width - shift
            elif shift < 0:
                shift *= -1
                start_x = self.img_width - shift
                stop_x = shift
            else:
                continue

            left_chunk = self.outputarr[start_y:stop_y, start_x:]
            wrap_chunk = self.outputarr[start_y:stop_y, :start_x]
            shake_array[start_y:stop_y, :stop_x] = left_chunk
            shake_array[start_y:stop_y, stop_x:] = wrap_chunk
        return Image.fromarray(shake_array, self.img_mode)

    def __line_block(self, image: Image.Image, glitch_in=0.1, glitch_out=0.2, mean=0, stddev=0.1):
        width = image.width
        height = image.height
        original = image.copy()

        glitch = False
        offset = int(random.normalvariate(mean, stddev) * image.width)
        for y in range(height):
            if not glitch and random.random() < glitch_in:
                offset = int(random.normalvariate(mean, stddev) * image.width)
                glitch = not glitch
            elif glitch and random.random() < glitch_out:
                glitch = not glitch

            for x in range(width):
                if glitch:
                    image.putpixel((x, y), original.getpixel((self.clamp_int(x + offset, width - 1), y)))
        return image

    def __color_block(self, image):
        colors = [(185, 65, 210, 128), (96, 178, 78, 128), (236, 68, 68, 128), (37, 128, 190, 128), (220, 43, 255, 128), (128, 128, 255, 128), (128, 212, 64, 128)]
        canvas_height = self.img_height
        canvas_width = self.img_width
        bnw_layer = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bnw_layer)
        for i in range(1000):
            x0 = int(random.random() * canvas_width)
            y0 = int(random.random() * canvas_height)
            dx = int(random.random() * 25)
            dy = int(random.random() * 25)
            alpha_w = int(255 * 0.5 * random.random())
            alpha_b = int(255 * 0.5 * random.random())
            draw.rectangle([x0, y0, x0 + dx, y0 + dy], fill=(0, 0, 0, alpha_b))
            draw.rectangle([x0, y0, x0 + dx, y0 + dy], fill=(255, 255, 255, alpha_w))

        color_index = random.randint(0, 6)
        y = int(random.random() * canvas_height)
        x = int(random.random() * canvas_width)
        draw.rectangle([x, y, min(x + x, canvas_width), min(y + y, canvas_height)], fill=colors[color_index])

        res = Image.alpha_composite(image.convert('RGBA'), bnw_layer)
        background = Image.new("RGB", res.size, (255, 255, 255))
        background.paste(res, mask=res.split()[3])  # 3 is the alpha channel

        return res
