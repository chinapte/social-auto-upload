import asyncio
from pathlib import Path

from social_upload.conf import BASE_DIR
from social_upload.uploader.ks_uploader.main import ks_setup, KSVideo
from social_upload.utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags


import argparse
def publish(video_dir):
    filepath = video_dir
    filepath = Path(BASE_DIR) / "videos"
    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    cookie_setup = asyncio.run(ks_setup(account_file, handle=False))
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        app = KSVideo(title, file, tags, publish_datetimes[index], account_file)
        asyncio.run(app.main(), debug=False)


def publish_video(video_path):
    filepath = Path(video_path)  # 修改为单文件路径
    account_file = Path(BASE_DIR / "cookies" / "ks_uploader" / "account.json")

    if not filepath.exists() or filepath.suffix != ".mp4":
        raise ValueError("提供的路径不是有效的 MP4 文件")

    publish_datetime = generate_schedule_time_next_day(1, 1, daily_times=[16])[0]  # 只生成一个发布时间
    cookie_setup = asyncio.run(ks_setup(account_file, handle=False))

    title, tags = get_title_and_hashtags(str(filepath))

    print(f"视频文件名：{filepath}")
    print(f"标题：{title}")
    print(f"Hashtag：{tags}")

    app = KSVideo(title, filepath, tags, publish_datetime, account_file)

    asyncio.run(app.main(), debug=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publish videos to Douyin.")
    parser.add_argument("video_path", type=str, help="video file.")

    args = parser.parse_args()
    publish_video(args.video_path)