import glob
import os
from PIL import Image
from moviepy.utils import VideoFileClip
import moviepy.editor as mpe
import numpy as np

compKey = lambda a : int(a.split('\\')[-1].split('.')[0])

# Returns (original_width, original_height, fps, duration)
def breakFrames(videoPath, sessionPath, resize=(256, 256), audio_save_progress_logger=None):
    print('I Breaking video into frames')
    clip = VideoFileClip(videoPath)
    fps = clip.fps
    width, height = clip.size
    duration = clip.duration
    if clip.audio:
        clip.audio.write_audiofile(os.path.join(sessionPath, 'temp_audio.mp3'), logger=audio_save_progress_logger)
    frames = clip.iter_frames()
    cnt = 1
    framesPath = os.path.join(sessionPath, "in_frames")
    for i, frame in enumerate(frames):
        print('I Obtained Frame', i)
        Image.fromarray(frame).resize(resize).convert('RGB').save(os.path.join(framesPath, f'{cnt}.jpg'))
        cnt += 1
    clip.close()
    return width, height, fps, duration

# Converts frames from framePath with sortable frame names to a .mp4 Video at videoPath
def joinFrames(sessionPath, videoPath, fps=30, frameSize=(256, 256), save_logger=None):
    framesPath = os.path.join(sessionPath, 'out_frames')
    filenames = glob.glob(os.path.join(framesPath, f'*.jpg'))
    filenames.sort(key=compKey)
    video = mpe.ImageSequenceClip(filenames, fps)
    video = video.fx(mpe.vfx.resize, width = frameSize[0], height = frameSize[1])
    audio = os.path.join(sessionPath, "temp_audio.mp3") if os.path.exists(os.path.join(sessionPath, "temp_audio.mp3")) else False
    video.write_videofile(videoPath, audio=audio, fps=fps, logger=save_logger)
    video.close()