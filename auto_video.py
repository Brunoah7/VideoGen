from moviepy.editor import ImageClip, concatenate_videoclips, ColorClip, CompositeVideoClip, AudioFileClip, TextClip
import requests
import sys
from bs4 import BeautifulSoup

import random
image_url = sys.argv[1]  
audio_file_path = sys.argv[2]  
quote = sys.argv[3]
video_length = float(sys.argv[4])
fade_length = float(sys.argv[5])
final_opacity = float(sys.argv[6])







audio = AudioFileClip(audio_file_path)



image_data = requests.get(image_url).content
with open("pinterest_download.jpg", "wb") as img_file:
    img_file.write(image_data)

print("Image done")

deep_image = ImageClip("pinterest_download.jpg", duration=video_length)

image_width, img_height = deep_image.size

box_height = img_height // 7
box_position = (0, 0)

white_box = ColorClip(size=(image_width, box_height), color=(255, 255, 255), duration=video_length)

whitebox = white_box.set_position(box_position)
deep_image = deep_image.fadein(fade_length).set_opacity(final_opacity)
max_font_size = 40  # You can adjust this value as needed

# Calculate the font size based on the image width
font_size = min(image_width // 10, max_font_size)  # Adjust the divisor to change the scaling factor

max_font_size = 40  # Maximum font size
min_font_size = 10  # Minimum font size

# Calculate the available height for text
available_height = box_height - 10  # Leave some padding

# Start with the maximum font size
font_size = max_font_size

# Create the text clip with initial font size
text_clip = TextClip(
    quote, fontsize=font_size, color="black", font="Arial-Bold", 
    size=(image_width - 60, None),  # Adjust width to fit within the image
    method='caption'  # Auto-wrap text
)

# Reduce font size until the text fits within the available height
while text_clip.size[1] > available_height and font_size > min_font_size:
    font_size -= 1  # Decrease font size
    text_clip = TextClip(
        quote, fontsize=font_size, color="black", font="Arial-Bold", 
        size=(image_width - 60, None),
        method='caption'
    )

audio = audio.subclip(0, video_length)

# Position the text in the center of the box
text_clip = text_clip.set_position(("center", (box_height - text_clip.size[1]) // 2)).subclip(0, video_length)

composited_video =  CompositeVideoClip([deep_image, white_box, text_clip])


composited_video = composited_video.set_audio(audio)
composited_video.write_videofile(
    "DeepVideo.mp4", 
    codec="libx264", 
    fps=24, 
    bitrate="600k",  # Maximum bitrate for better quality
    preset="medium",  # Use 'veryslow' for the best compression efficiency
    ffmpeg_params=["-crf", "18"]  # Set a lower CRF for higher quality
)
