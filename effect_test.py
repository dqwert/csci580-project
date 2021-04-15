import os
import random
import shutil
from decimal import getcontext, Decimal
from typing import List, Optional, Tuple, Union
import numpy

import numpy as np
from PIL import Image, ImageSequence, ImageDraw

image = Image.open('pics/source.png')
assert isinstance(image, Image.Image)
mean = 0
stddev = 0.1


image.save('test_result/test_output.png')
