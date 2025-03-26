from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os
import uuid

app = Flask(__name__)

# Configuration
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"
VIDEO_PATH = "eid-background.mp4"
OUTPUT_FOLDER = "generated_videos"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "Eid Video API is running!"

@app.route("/generate", methods=[POST])
def generate_video():
    data = request.get_json()
    name = data.get("name")
    position = data.get("position", "")

    if not name:
        return jsonify({"error": "Name is required."}), 400

    # Arabic text shaping
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    reshaped_position = arabic_reshaper.reshape(position) if position.strip() else ""
    bidi_position = get_display(reshaped_position) if reshaped_position else ""

    try:
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
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        final.write_videofile(output_path, codec='libx264')

        return send_file(output_path, as_attachment=True, download_name=output_filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
