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
download_type_opt = ["audio", "video"]


def get_format_string(resolution, download_type):
    res_num = int(resolution.replace('p', ''))
    if download_type == 'audio':
        return 'bestaudio/best'
    elif download_type == 'video':
        return f'bestvideo[height<={res_num}]+bestaudio/best[height<={res_num}]'

        

# Download logic
def download_video(url, resolution, download_type):
    if not url:
        st.write("Sorry, Thats not a url")
        return

    
    format_str = get_format_string(resolution, download_type)

    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        progress_text = "Downloading..."
        status_label = st.progress(0)
        for i, step in enumerate(range(1000)):    
            status_label.progress((i+1)/1000)
            st.success("Download Completed!")

    except Exception as e:
        st.write("Sorry, something went wrong")

st.title("YouTube Downloader(no ads)")

st.subheader("Free youtube videos for everyone")

video_url = st.text_input("Enter a Url")
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
        download_video(video_url, resolution, download_type)
       
