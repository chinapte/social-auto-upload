import asyncio
from pathlib import Path

from social_upload.conf import BASE_DIR
# from tk_uploader.main import tiktok_setup, TiktokVideo
from social_upload.uploader.tk_uploader.main_chrome import tiktok_setup, TiktokVideo
from social_upload.utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags


import argparse
import asyncio
from pathlib import Path


def publish_video(video_file_path):
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "tk_uploader" / "account.json")
    folder_path = Path(filepath)

    # Assuming video_file_path is the path to the single video
    file = Path(video_file_path)

    # Check if the file exists and is an mp4 file
    if file.exists() and file.suffix == '.mp4':
        title, tags = get_title_and_hashtags(str(file))
        thumbnail_path = file.with_suffix('.png')

        print(f"video_file_name: {file}")
        print(f"video_title: {title}")
        print(f"video_hashtag: {tags}")

        if thumbnail_path.exists():
            print(f"thumbnail_file_name: {thumbnail_path}")
            app = TiktokVideo(title, file, tags, generate_schedule_time_next_day(1, 1, daily_times=[16])[0],
                              account_file, thumbnail_path)
        else:
            app = TiktokVideo(title, file, tags, generate_schedule_time_next_day(1, 1, daily_times=[16])[0],
                              account_file)

        asyncio.run(app.main(), debug=False)
    else:
        print(f"Invalid video file path: {video_file_path}. Please provide a valid .mp4 file.")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publish videos to Douyin.")
    parser.add_argument("video_path", type=str, help="video file.")

    args = parser.parse_args()
    publish_video(args.video_path)