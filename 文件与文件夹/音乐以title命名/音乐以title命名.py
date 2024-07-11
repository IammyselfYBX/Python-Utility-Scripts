import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TIT2

def update_filename_with_title(mp3_path):
    try:
        audio = ID3(mp3_path)
        title = audio.get('TIT2')
        if title:
            title_str = title.text[0]
            new_filename = f"{title_str}.mp3"
            new_filepath = os.path.join(os.path.dirname(mp3_path), new_filename)
            os.rename(mp3_path, new_filepath)
            print(f"Renamed '{mp3_path}' to '{new_filepath}'")
        else:
            print(f"No title tag found in '{mp3_path}'")
    except Exception as e:
        print(f"Failed to process '{mp3_path}': {e}")

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            filepath = os.path.join(directory, filename)
            update_filename_with_title(filepath)

# Example usage
directory_path = r'D:\BaiduNetdiskDownload\test\demo'
process_directory(directory_path)
