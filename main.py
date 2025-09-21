import streamlit  as st
from yt_dlp import YoutubeDL
import os
import PIL
import time

st.set_page_config(layout="wide")

fixed_thumbnail_name = "thumbnail"
# Format builder
download_folder = os.path.expanduser("~/Downloads")
resolution_options = ["360p", "480p", "720p", "1080p"]
download_type_opt = ["Audio", "Video"]


col1, col2 = st.columns(2)



def get_format_string(resolution, download_type):
    res_num = int(resolution.replace('p', ''))
    if download_type == 'Audio':
        return 'bestaudio/best'
    elif download_type == 'Video':
        return f'bestvideo[height<={res_num}]+bestaudio/best[height<={res_num}]'



def progress_hook(d):
    if d['status'] == 'downloading':
        if d.get("total_bytes") and d.get("downloaded_bytes"):
            progress = d["downloaded_bytes"] / d["total_bytes"]
           
            progress_bar.progress(progress)      
        percent = d.get('_percent_str', "0%")
        speed = d.get('_speed_str', "0 KiB/s")
        eta = d.get('_eta_str', "N/A")

        status_text.text(f"Downloading... {percent} at {speed}, ETA {eta}")

    elif d['status'] == 'finished':
        status_text.text("Download finished, now post-processing...")




# Download logic
def download_video(url, resolution, download_type):
    if not url:
        st.write("Sorry, Thats not a url")
        return

    
    format_str = get_format_string(resolution, download_type)

    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True,
        'progress_hooks': [progress_hook] 
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            d = ydl.extract_info(url, download=False)
            if d.get("_type") == 'playlist':
                st.warning("⚠️This is a playlist, playlist aren't supported")
            else:
                ydl.download([url])
    except Exception as e:
        st.error(f"Download failed: {e}")






st.title("YouTube Downloader(no ads)")

st.subheader("Free youtube videos for everyone")


video_url = st.text_input("Enter a Url", placeholder="Enter a YouTube link...")
if video_url:
    ydl_opts = {
        'quiet': True,  # Suppress console output
        'no_warnings': True, # Suppress warnings
        'extract_flat': True, # Only extract basic info, no full downloads
        'outtmpl': os.path.join(download_folder, fixed_thumbnail_name),
        
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get('title', None)
            
        except Exception as e:
            print(f"Error retrieving video title: {e}")
    command = f"yt-dlp --write-thumbnail --skip-download -o '{download_folder}/{fixed_thumbnail_name}' {video_url}"
    os.system(command)

    st.subheader(video_title)
    
    st.image(f"{download_folder}/{fixed_thumbnail_name}.webp")
    resolution = st.selectbox(options=resolution_options, label="Choose Resolution")
    download_type = st.selectbox(options=download_type_opt, label="Choose Download Type")

    download = st.button("Download")
    if download:
        progress_bar = st.progress(0)
        status_text = st.empty()
        download_video(video_url, resolution, download_type)
        
