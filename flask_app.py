from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Eid Video API is running!"

@app.route('/generate-video', methods=['POST'])
def generate_video():
    # Dummy response for now
    data = request.get_json()
    return jsonify({"url": "https://your-storage-url.com/fake.mp4"})
