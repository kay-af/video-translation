import sys
from PIL import Image
import translator
import numpy as np

if __name__ == '__main__':
    filepath = sys.argv[1].strip()
    dstpath = sys.argv[2].strip()
    print('Opening image...')
    frame = Image.open(filepath)
    width, height = frame.width, frame.height
    print('Image dimensions:', width, height)
    print('Resizing...')
    frame = frame.resize((256, 256))
    print('Initializing translator...')
    translator.set_model('./models/h2z.pth')
    print('Translating...')
    converted = translator.translate([frame], include_logs=False)
    print('Restoring dimensions...')
    converted = converted[0]
    converted = converted.resize((width, height))
    print('Saving as', dstpath)
    converted.save(dstpath, dstpath.split('.')[-1])