
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os

# === User Inputs ===
name = "Paul Melotto"
position = "CEO"

# === File Paths ===
VIDEO_PATH = "eid-background.mp4"
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"
OUTPUT_FILE = f"eid_greeting_{name.replace(' ', '_')}.mp4"

# === Reshape Arabic Text ===
reshaped_name = arabic_reshaper.reshape(name)
bidi_name = get_display(reshaped_name)

bidi_position = ""
if position.strip():
    reshaped_pos = arabic_reshaper.reshape(position)
    bidi_position = get_display(reshaped_pos)

# === Load Video ===
clip = VideoFileClip(VIDEO_PATH)

# === Create Name Clip with Animation ===
name_clip = (
    TextClip(bidi_name, font=FONT_PATH, fontsize=90, color='red',
             method='caption', align='center', size=(clip.w, None))
    .set_duration(clip.duration - 1.46)
    .set_start(1.46)
    .crossfadein(1.5)
    .set_position(("center", clip.h * 0.78))
)

clips = [clip, name_clip]

# === Create Position Clip with Animation ===
if bidi_position:
    pos_clip = (
        TextClip(bidi_position, font=FONT_PATH, fontsize=60, color='red',
                 method='caption', align='center', size=(clip.w, None))
        .set_duration(clip.duration - 1.60)
        .set_start(1.60)
        .crossfadein(1.5)
        .set_position(("center", clip.h * 0.83))
    )
    clips.append(pos_clip)

# === Composite Final Video ===
final = CompositeVideoClip(clips).set_duration(clip.duration)
final = final.set_audio(clip.audio)
final.write_videofile(
    OUTPUT_FILE,
    codec="libx264",
    audio=True,
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True
)
