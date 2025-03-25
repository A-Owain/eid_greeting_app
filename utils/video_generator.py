from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display

def generate_greeting_video(name, position, background_path, output_path, font_path):
    reshaped_name = get_display(arabic_reshaper.reshape(name))
    reshaped_position = get_display(arabic_reshaper.reshape(position))

    clip = VideoFileClip(background_path)

    # Name clip
    name_clip = (
        TextClip(reshaped_name, fontsize=90, color="red", font=font_path)
        .set_start(1.5)
        .set_duration(clip.duration - 1.5)
        .fadein(1.5)
        .set_position(("center", clip.h * 0.78))
    )

    # Position clip
    pos_clip = (
        TextClip(reshaped_position, fontsize=60, color="red", font=font_path)
        .set_start(2.0)
        .set_duration(clip.duration - 2.0)
        .fadein(1.0)
        .set_position(("center", clip.h * 0.83))
    )

    final = CompositeVideoClip([clip, name_clip, pos_clip])
    final = final.set_audio(clip.audio)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
