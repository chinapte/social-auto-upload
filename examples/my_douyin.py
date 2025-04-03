import asyncio
from pathlib import Path
import argparse
#from social_upload.conf import BASE_DIR
from social_upload.examples.publish_util import call_cli
from social_upload.uploader.douyin_uploader.main import douyin_setup, DouYinVideo
from social_upload.utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags

from social_upload.conf import BASE_DIR


def publish(video_dir, title, tags):
    filepath = video_dir
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])
    cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))
    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        thumbnail_path = file.with_suffix('.png')
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        # 暂时没有时间修复封面上传，故先隐藏掉该功能
        # if thumbnail_path.exists():
        # app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file, thumbnail_path=thumbnail_path)
        # else:
        app = DouYinVideo(title, file, tags, publish_datetimes[index], account_file)
        asyncio.run(app.main(), debug=False)


def publish_video(video_path):
    filepath = Path(video_path)  # 修改为单文件路径
    account_file = Path(BASE_DIR / "cookies" / "douyin_uploader" / "account.json")

    if not filepath.exists() or filepath.suffix != ".mp4":
        raise ValueError(f"提供的路径不是有效的 MP4 文件{filepath}")

    publish_datetime = generate_schedule_time_next_day(1, 1, daily_times=[16])[0]  # 只生成一个发布时间
    cookie_setup = asyncio.run(douyin_setup(account_file, handle=False))

    title, tags = get_title_and_hashtags(str(filepath))
    thumbnail_path = filepath.with_suffix('.png')

    print(f"视频文件名：{filepath}")
    print(f"标题：{title}")
    print(f"Hashtag：{tags}")

    # 暂时没有时间修复封面上传，故先隐藏掉该功能
    # if thumbnail_path.exists():
    #     app = DouYinVideo(title, filepath, tags, publish_datetime, account_file, thumbnail_path=thumbnail_path)
    # else:
    app = DouYinVideo(title, filepath, tags, publish_datetime, account_file)

    asyncio.run(app.main(), debug=False)


if __name__ == '__main__':
    # import sys
    # sys.path.append("D:\social-auto-upload")
    #
    # parser = argparse.ArgumentParser(description="Publish videos to Douyin.")
    # parser.add_argument("video_path", type=str, help="video file.")
    #
    # args = parser.parse_args()
    # publish_video(args.video_path)
    publish_video("E:\\short\\commentary\\@movierecapsofficial\\Y7JJmcA5e_E\\Y7JJmcA5e_E_final.mp4")

