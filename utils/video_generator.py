from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
import os


def generate_greeting_video(name: str, output_path: str, font_path: str, video_path: str):
    # Reshape Arabic text for proper display
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    # Create image with text using PIL
    img = Image.new("RGBA", (2160, 2824), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 90)

    text_width, text_height = draw.textsize(bidi_name, font=font)
    position = ((2160 - text_width) // 2, 400)

    draw.text(position, bidi_name, font=font, fill="red")

    # Save temporary PNG
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        img.save(tmp_img.name, "PNG")
        tmp_img_path = tmp_img.name

    # Load base video
    video = VideoFileClip(video_path)

    # Create ImageClip from the PIL image
    text_overlay = (
        ImageClip(tmp_img_path)
        .set_duration(video.duration)
        .set_start(1.5)
        .set_position("center")
    )

    # Composite
    final = CompositeVideoClip([video, text_overlay])
    final.write_videofile(output_path, codec="libx264", audio=True)

    # Clean up temp file
    os.remove(tmp_img_path)
