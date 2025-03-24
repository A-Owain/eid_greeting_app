from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display

def generate_greeting_video(name, position, background_path, font_path, output_path):
    clip = VideoFileClip(background_path)

    # Prepare Arabic text
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    reshaped_pos = arabic_reshaper.reshape(position)
    bidi_pos = get_display(reshaped_pos)

    # Create text clips
    name_text = TextClip(bidi_name, fontsize=90, font=font_path, color='red').set_start(1.5).set_duration(clip.duration - 1.5).set_position('center')
    pos_text = TextClip(bidi_pos, fontsize=60, font=font_path, color='white').set_start(2.5).set_duration(clip.duration - 2.5).set_position(("center", "bottom"))

    # Combine clips
    final = CompositeVideoClip([clip, name_text, pos_text])
    final.write_videofile(output_path, codec='libx264', audio=True, preset='ultrafast')
