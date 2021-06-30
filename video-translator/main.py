import argparse
from frame_loader import FrameLoader
import json
import os
import time
import frame_utils as fu
import shutil
import translator

def __clamp__(n, l=0, h=1):
    if n < l:
        return l
    if n > h:
        return h
    return n

def __fetchFilters__():
    filterMap = dict()
    with open('./filters.json') as filterInfo:
        filters = json.load(filterInfo)
        for filter in filters:
            filterMap[filter['modelCode']] = filter['model']
    return filterMap

def __initPath__():
    if not os.path.exists('./translation'):
        os.mkdir('./translation')

def __createSession__():
    session = str(time.time()).replace('.','-')
    if not os.path.exists(f'./translation/{session}'):
        os.mkdir(f'./translation/{session}')
        os.mkdir(f'./translation/{session}/in_frames')
        os.mkdir(f'./translation/{session}/out_frames')
    else:
        raise "Session name must be unique"
    return f'./translation/{session}'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Video translator")
    parser.add_argument('src', help="Path to the video")
    parser.add_argument('--filter', help="Comma separated values of filter codes to apply", required=False, default=0)
    parser.add_argument('--batch', help='Number of elements in a conversion batch', required=False, default=5)
    args = parser.parse_args()

    filterMap = __fetchFilters__()
    
    __initPath__()
    sessionPath = __createSession__()

    try:
        width, height, fps, duration = fu.breakFrames(args.src, sessionPath)
        frameLoader = FrameLoader(os.path.join(sessionPath, 'in_frames'), batch=int(args.batch))
        print(width, height, fps, duration)

        translator.set_model(filterMap[int(args.filter)])

        count = 1
        while frameLoader.hasNext():
            frames = frameLoader.next()

            # Frame is a PIL image of size 256 x 256
            # Do your machine learning stuff here with frames as a batch
            # update frames with a PIL image after done
            frames = translator.translate(frames)

            for frame in frames:
                image = frame.resize((width, height)) # Restore original size
                image.save(os.path.join(sessionPath, 'out_frames', f'{count}.jpg'))
                count += 1
            progress = __clamp__(count / frameLoader.total(), 0, 1)
            print('P1 %d' % (int(__clamp__(progress) * 100.0)))
        print('Frames converted!')

        fu.joinFrames(sessionPath, os.path.join(sessionPath, 'out.mp4'), fps=fps, frameSize=(width, height))
    finally:
        print('Cleaning up...')
        shutil.rmtree(os.path.join(sessionPath, 'in_frames'))
        shutil.rmtree(os.path.join(sessionPath, 'out_frames'))