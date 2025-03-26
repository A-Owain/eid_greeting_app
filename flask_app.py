from flask import Flask, request, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import uuid
import os

app = Flask(__name__)

VIDEO_PATH = "eid-background.mp4"
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"
STATIC_DIR = "static/videos"
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    name = data.get("name", "").strip()
    position = data.get("position", "").strip()

    if not name:
        return jsonify({"error": "Name is required."}), 400

    # Arabic text reshaping
    bidi_name = get_display(arabic_reshaper.reshape(name))
    bidi_position = get_display(arabic_reshaper.reshape(position)) if position else ""

    # Create video
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

    video_id = uuid.uuid4().hex[:10]
    output_filename = f"eid_greeting_{video_id}.mp4"
    output_path = os.path.join(STATIC_DIR, output_filename)
    final.write_videofile(output_path, codec="libx264")

    public_url = f"{request.host_url}static/videos/{output_filename}"
    return jsonify({"url": public_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
