import os
import shutil
import sqlite3
import cv2
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
VIDEOS_DB = 'data/videos.db'
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'jpg', 'mp4'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/create')
def create():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    conn = sqlite3.connect('data/videos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos
                 (user_id TEXT, work_id TEXT, cover_path TEXT, video_path TEXT)''')
    conn.commit()
    conn.close()
    return 'True'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        cover = request.files.get('cover')
        video = request.files.get('video')

        if user_id and video and allowed_file(video.filename):
            import uuid
            work_id = str(uuid.uuid4())
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
            work_folder = os.path.join(user_folder, work_id)
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            if not os.path.exists(work_folder):
                os.makedirs(work_folder)

            video_path = os.path.join(work_folder, video.filename)
            video.save(video_path)

            if cover and allowed_file(cover.filename):
                cover_path = os.path.join(work_folder, cover.filename)
                cover.save(cover_path)
            else:
                # 未上传封面图片，使用cv2从视频中提取首帧作为封面
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        cover_path = os.path.join(work_folder, 'cover.jpg')
                        cv2.imwrite(cover_path, frame)
                cap.release()

            conn = sqlite3.connect('data/videos.db')
            c = conn.cursor()
            c.execute("INSERT INTO videos VALUES (?,?,?,?)", (user_id, work_id, cover_path, video_path))
            conn.commit()
            conn.close()
            return redirect(url_for('upload'))
    return render_template('upload.html')


@app.route('/videos', methods=['GET', 'POST'])
def videos():
    conn = sqlite3.connect('data/videos.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT user_id FROM videos")
    user_ids = [row[0] for row in c.fetchall()]
    user_ids.sort()

    selected_user_id = request.form.get('user_id')
    works = []
    if selected_user_id:
        c.execute("SELECT work_id, cover_path, video_path FROM videos WHERE user_id =?", (selected_user_id,))
        works = c.fetchall()

    conn.close()
    return render_template('videos.html', user_ids=user_ids, selected_user_id=selected_user_id, works=works)

@app.route('/videos_all', methods=['GET', 'POST'])
def videos_all():
    conn = sqlite3.connect('data/videos.db')
    c = conn.cursor()

    c.execute("SELECT work_id, cover_path, video_path FROM videos")
    works = c.fetchall()

    conn.close()
    return render_template('videos_all.html', user_ids='', selected_user_id='', works=works)


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete')
def delete():
    if os.path.exists(VIDEOS_DB):
        os.remove(VIDEOS_DB)
    shutil.rmtree(UPLOAD_FOLDER)
    return 'True'

if __name__ == '__main__':
    create()
    app.run(port=5002)
    