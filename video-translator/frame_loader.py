import glob
import os
import frame_utils as fu
from PIL import Image

class FrameLoader():
    def __init__(self, path, batch=60, ext='jpg'):
        files = glob.glob(os.path.join(path, f'*.{ext}'))
        files.sort(key=fu.compKey)
        self.files = files
        self.pointer = 0
        self.numFrames = len(files)
        self.batch = batch
    
    def total(self):
        return self.numFrames

    def hasNext(self):
        return self.pointer < self.numFrames

    # Returns next batch of PIL images. None if comsumed
    def next(self):
        if self.pointer >= self.numFrames:
            return None
        else:
            to = min(self.pointer + self.batch, self.numFrames)
            files_to_return = self.files[self.pointer:to]
            self.pointer = to
            frames = []
            for file in files_to_return:
                img = Image.open(file).convert('RGB')
                frames.append(img)
            return frames