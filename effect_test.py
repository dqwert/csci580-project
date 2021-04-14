import os
import random
import shutil
from decimal import getcontext, Decimal
from typing import List, Optional, Tuple, Union

import numpy as np
from PIL import Image, ImageSequence, ImageDraw

image = Image.open('pics/source.png')

channels = image.split()

image.save('test_result/test_output.png')
