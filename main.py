from __future__ import unicode_literals
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import shutil
import yt_dlp
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'info@4004'
UPLOAD_FOLDER = './upload'
CWD = os.path.expanduser(os.getcwd())
OUTPUT_FOLDER = './output'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/downloader', methods=['GET', 'POST'])
def youtube_downloader():
    dir_name = os.path.expanduser('~/PycharmProjects/ArcMusic')
    path = os.listdir(dir_name)
    for item in path:
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))

    if request.method == 'POST':
        link = request.form.get('link')
        if not link:
            flash('Link Inválido!')
            return redirect(url_for('youtube_downloader'))
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(ext)s',


        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(link, download=False)
                video_title = info_dict.get('title', None)
                ydl.download(link)
            except yt_dlp.DownloadError:
                flash('Link Inválido!')
                return redirect(url_for('youtube_downloader'))
            except FileNotFoundError:
                flash('Algum erro inesperado ocorreu!')
                return redirect(url_for('youtube_downloader'))
        return send_file(f'{video_title}.mp3', as_attachment=True)

    return render_template('donwloader.html')


@app.route('/list-downloader', methods=['GET', 'POST'])
def list_downloader():
    zipname = 'musics'
    output_path = os.listdir(OUTPUT_FOLDER)
    upload_path = os.listdir(UPLOAD_FOLDER)
    path = os.listdir(CWD)
    for item in upload_path:
        if item.endswith(".txt"):
            os.remove(os.path.join(UPLOAD_FOLDER, item))

    for item in output_path:
        if item.endswith(".mp3"):
            os.remove(os.path.join(OUTPUT_FOLDER, item))

    for item in path:
        if item.endswith(".zip"):
            os.remove(os.path.join(CWD, item))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            save_path = os.path.join(UPLOAD_FOLDER, secure_filename('list.txt'))
            file.save(save_path)
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './output/%(title)s.%(ext)s',

            }
            with open("./upload/list.txt") as file:
                for line in file:
                    line = line.strip()
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        try:
                            ydl.download(line)
                        except:
                            flash('Link(s) Incorreto(s)!')
                            pass

                shutil.make_archive(zipname, 'zip', './output')
            return send_file('./musics.zip')
    return render_template('list_downloader.html')


@app.route('/video-downloader', methods=['GET', 'POST'])
def video_downloader():
    # think about it later!
    pass


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
