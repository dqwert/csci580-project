import os
import random
import shutil
from decimal import getcontext, Decimal
from typing import List, Optional, Tuple, Union
import numpy

import numpy as np
from PIL import Image, ImageSequence, ImageDraw


def clamp(x, max, min=0):
    if x < min:
        return min
    elif x > max:
        return max
    else:
        return x


image = Image.open('pics/source.png')
assert isinstance(image, Image.Image)




image.save('test_result/test_output.png')
