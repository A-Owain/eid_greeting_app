from flask import Flask, request, send_file, jsonify
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os
import uuid

app = Flask(__name__)

FONT_PATH = "IBMPlexSansArabic-Bold.ttf"
VIDEO_PATH = "eid-background.mp4"

@app.route("/")
def home():
    return "Eid Video API is running!"

@app.route("/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    name = data.get("name", "")
    position = data.get("position", "")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    # Prepare text
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    bidi_position = ""
    if position.strip():
        reshaped_pos = arabic_reshaper.reshape(position)
        bidi_position = get_display(reshaped_pos)

    # Create video
    try:
        clip = VideoFileClip(VIDEO_PATH, audio=False)

        name_clip = (
            TextClip(bidi_name, font=FONT_PATH, fontsize=90, color="red", method="label")
            .set_duration(clip.duration - 1.46)
            .set_start(1.46)
            .crossfadein(1.5)
            .set_position(("center", clip.h * 0.78))
        )

        clips = [clip, name_clip]

        if bidi_position:
            pos_clip = (
                TextClip(bidi_position, font=FONT_PATH, fontsize=60, color="red", method="label")
                .set_duration(clip.duration - 1.60)
                .set_start(1.60)
                .crossfadein(1.5)
                .set_position(("center", clip.h * 0.83))
            )
            clips.append(pos_clip)

        final = CompositeVideoClip(clips).set_duration(clip.duration)

        filename = f"eid_greeting_{uuid.uuid4().hex[:6]}.mp4"
        final.write_videofile(filename, codec="libx264")

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        try:
            if os.path.exists(filename):
                os.remove(filename)
        except:
            pass

if __name__ == "__main__":
    app.run(debug=True)
