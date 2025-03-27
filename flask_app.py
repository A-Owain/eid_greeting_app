from flask import Flask, request, send_file, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import uuid
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Eid Video API is running!"

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    name = data.get("name", "")
    position = data.get("position", "")

    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)
    bidi_position = get_display(arabic_reshaper.reshape(position)) if position.strip() else ""

    video_path = "eid-background.mp4"
    font_path = "IBMPlexSansArabic-Bold.ttf"
    output_path = f"output_{uuid.uuid4().hex[:8]}.mp4"

    clip = VideoFileClip(video_path, audio=False)

    name_clip = (
        TextClip(bidi_name, font=font_path, fontsize=90, color='red', method='label')
        .set_duration(clip.duration - 1.46)
        .set_start(1.46)
        .crossfadein(1.5)
        .set_position(("center", clip.h * 0.78))
    )

    clips = [clip, name_clip]

    if bidi_position:
        pos_clip = (
            TextClip(bidi_position, font=font_path, fontsize=60, color='red', method='label')
            .set_duration(clip.duration - 1.60)
            .set_start(1.60)
            .crossfadein(1.5)
            .set_position(("center", clip.h * 0.83))
        )
        clips.append(pos_clip)

    final = CompositeVideoClip(clips).set_duration(clip.duration)
    final.write_videofile(output_path, codec='libx264')

    return send_file(output_path, as_attachment=True, download_name=f"eid_greeting_{name}.mp4")
