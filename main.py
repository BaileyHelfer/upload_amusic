import logging
import subprocess
from flask import Flask, render_template, request
import os
import stat
from sclib import SoundcloudAPI, Track, Playlist
from pytube import YouTube
from yaml import safe_load

app = Flask(__name__)

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create a file handler which logs even debug messages
fh = logging.FileHandler('app.log')
fh.setLevel(logging.INFO)
# Create a formatter and set the formatter for the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(fh)

def run_apple_script(song_path,artist_name,album_name,song_name,artwork):
    ''''
    This function runs the apple script to add the song to Apple Music Library
    '''
    with open('config.yaml', 'r') as file:
        config = safe_load(file)

    apple_script = config['apple_script']
    song_path = os.path.abspath(song_path)
    artwork = os.path.abspath(artwork)
    apple_script = config['apple_script_path']
    
    subprocess.run(["osascript",
                    apple_script,
                    song_path,
                    artist_name,
                    album_name,
                    song_name,
                    artwork])

@app.route("/")
def index():
    '''
    Load the index page with the list of artists
    '''
    with open('config.yaml', 'r') as file:
        config = safe_load(file)
    
    # Extract the artist names from the config
    artists = list(config.get('artist', {}).keys())
    
    return render_template('index.html', artists=artists)

@app.route("/download", methods=["POST"])
def download():
    """
    This function handles the POST request to download a song from the server. 
    
    It takes in the URL of the song, the name of the song, the artist of the song, and the name of the album to which the song belongs. It then downloads the song using the YouTube and SoundCloud APIs and adds it to the Apple Music Library using an AppleScript.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    render_template('success.html', song_name=song_name, artist_name=artist_name, album_name=album_name)
        A rendered HTML template that displays the name of the song, the artist of the song, and the name of the album.
    """
    with open('config.yaml', 'r') as file:
        config = safe_load(file)

    url = request.form["url"]
    song_name = request.form["song_name"]
    artist_name = request.form["artist"]
    album_name = config['artist'][artist_name]['album']
    artwork = config['artist'][artist_name]['artwork']

    songs_dir = './songs'
    if not os.path.exists(songs_dir):
        os.makedirs(songs_dir)

    if "youtube.com" in url or "youtu.be" in url:
        # Download the song from YouTube
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        # Download the file to the 'songs' directory
        filename = audio_stream.download(output_path=songs_dir)
        # Log the filename
        logger.info(f"Downloaded {filename} from YouTube")
    elif "soundcloud.com" in url:
        api = SoundcloudAPI()  
        track = api.resolve(url=url)
        assert type(track) is Track
        filename = os.path.join(songs_dir, f'{track.artist} - {track.title}.mp3')
        # Log the filename
        logger.info(f"Downloaded {filename} from SoundCloud")
    else:
        raise ValueError("Invalid file path")

    with open(filename, 'wb+') as file:
        track.write_mp3_to(file)
    os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    run_apple_script(filename,artist_name,album_name,song_name,artwork)

    return render_template('success.html', song_name=song_name, artist_name=artist_name, album_name=album_name)


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)

