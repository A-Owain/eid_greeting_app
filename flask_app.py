from flask import Flask, request, send_file, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import uuid
import os

app = Flask(__name__)

VIDEO_PATH = "eid-background.mp4"
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"

@app.route("/")
def index():
    return "Eid Video API is running!"

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    name = data.get("name", "").strip()
    position = data.get("position", "").strip()

    if not name:
        return jsonify({"error": "Name is required"}), 400

    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    bidi_position = ""
    if position:
        reshaped_position = arabic_reshaper.reshape(position)
        bidi_position = get_display(reshaped_position)

    clip = VideoFileClip(VIDEO_PATH, audio=False)

    name_clip = (
        TextClip(bidi_name, font=FONT_PATH, fontsize=90, color='red', method='label')
        .set_duration(clip.duration - 1.46)
        .set_start(1.46)
        .crossfadein(1.5)
        .set_position(("center", clip.h * 0.78))
    )

    clips = [clip, name_clip]

    if bidi_position:
        pos_clip = (
            TextClip(bidi_position, font=FONT_PATH, fontsize=60, color='red', method='label')
            .set_duration(clip.duration - 1.60)
            .set_start(1.60)
            .crossfadein(1.5)
            .set_position(("center", clip.h * 0.83))
        )
        clips.append(pos_clip)

    final = CompositeVideoClip(clips).set_duration(clip.duration)
    output_filename = f"eid_greeting_{uuid.uuid4().hex[:8]}.mp4"
    final.write_videofile(output_filename, codec='libx264', audio=False)

    return send_file(output_filename, as_attachment=True, download_name=output_filename)
