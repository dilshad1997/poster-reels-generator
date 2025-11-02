from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip
import os, time

app = Flask(__name__)
os.makedirs('static/generated', exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    img = request.files['image']
    text = request.form['text']
    filename = f"{int(time.time())}_{img.filename}"
    path = f"static/uploads/{filename}"
    img.save(path)

    # Image processing
    image = Image.open(path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 80)
    draw.text((100,100), text, fill=(255,255,255), font=font)
    styled = f"static/generated/{filename.split('.')[0]}_styled.png"
    image.save(styled)

    # 20-second video
    clip = ImageClip(styled, duration=20)
    clip.write_videofile(styled.replace('.png', '.mp4'), fps=24)
    return send_file(styled.replace('.png', '.mp4'), as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
