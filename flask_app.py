from flask import Flask, request, send_file, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os
import uuid

app = Flask(__name__)

VIDEO_PATH = "eid-background.mp4"
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"

@app.route("/")
def home():
    return "✅ Eid Video API is running!"

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    name = data.get("name", "").strip()
    position = data.get("position", "").strip()

    if not name:
        return jsonify({"error": "Name is required"}), 400

    # Debugging
    print("🔍 Current directory:", os.getcwd())
    print("📂 Directory contents:", os.listdir("."))
    print(f"🎥 Looking for video: {VIDEO_PATH}")

    if not os.path.isfile(VIDEO_PATH):
        return jsonify({"error": f"Video file not found: {VIDEO_PATH}"}), 500

    try:
        reshaped_name = arabic_reshaper.reshape(name)
        bidi_name = get_display(reshaped_name)

        reshaped_position = arabic_reshaper.reshape(position) if position else ""
        bidi_position = get_display(reshaped_position) if position else ""

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
        final.write_videofile(output_filename, codec="libx264")

        return send_file(output_filename, mimetype="video/mp4", as_attachment=True)

    except Exception as e:
        print("💥 Exception occurred:", e)
        return jsonify({"error": "Video generation failed", "details": str(e)}), 500
