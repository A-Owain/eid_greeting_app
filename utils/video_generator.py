from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
import os


def generate_greeting_video(name: str, background_path: str, font_path: str) -> str:
    # Prepare Arabic name
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    # Load background video
    clip = VideoFileClip(background_path)

    # Create transparent image with text
    img = Image.new("RGBA", clip.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, 90)
    text_width, text_height = draw.textsize(bidi_name, font=font)
    position = ((clip.size[0] - text_width) // 2, clip.size[1] - text_height - 100)

    draw.text(position, bidi_name, font=font, fill="red")

    # Save temporary image
    temp_img_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    img.save(temp_img_path)

    # Make overlay clip
    txt_clip = ImageClip(temp_img_path).set_duration(clip.duration).set_start(1.5)
    final = CompositeVideoClip([clip, txt_clip])

    # Save output
    output_path = os.path.join(tempfile.gettempdir(), f"eid_greeting_{name}.mp4")
    final.write_videofile(output_path, codec="libx264", audio=True)

    return output_path
