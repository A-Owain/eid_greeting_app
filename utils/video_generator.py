from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os

def generate_greeting_video(name: str, background_path: str, output_path: str, font_path: str):
    # Reshape and reorder Arabic name
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_text = get_display(reshaped_name)

    # Load background video
    clip = VideoFileClip(background_path)

    # Create text clip
    txt_clip = TextClip(
        bidi_text,
        font=font_path,  # Full path to .ttf font file
        fontsize=90,
        color='red'
    ).set_position('center').set_start(1.5).set_duration(clip.duration - 1.5)

    # Composite text on video
    video = CompositeVideoClip([clip, txt_clip])

    # Write final video with original audio
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
