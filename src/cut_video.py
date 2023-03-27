# Import everything needed to edit video clips
from moviepy.editor import *

# loading video gfg
clip = VideoFileClip("parking.mp4")
# getting only first 54 seconds
clip = clip.subclip(0, 54)
new_clip = clip.without_audio()
new_clip.write_videofile("car_parking.mp4")
# showing clip
clip.ipython_display()