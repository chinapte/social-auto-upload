import time
from pathlib import Path

from social_upload.uploader.bilibili_uploader.main import read_cookie_json_file, extract_keys_from_json, random_emoji, \
    BilibiliUploader
from social_upload.conf import BASE_DIR
from social_upload.utils.constant import VideoZoneTypes
from social_upload.utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags
import argparse


def publish(video_dir):
    filepath = video_dir
    # how to get cookie, see the file of get_bilibili_cookie.py.
    account_file = Path(BASE_DIR / "cookies" / "bilibili_uploader" / "account.json")
    if not account_file.exists():
        print(f"{account_file.name} 配置文件不存在")
        exit()
    cookie_data = read_cookie_json_file(account_file)
    cookie_data = extract_keys_from_json(cookie_data)

    tid = VideoZoneTypes.KNOWLEDGE_CAMPUS.value  # 设置分区id

    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)
    timestamps = generate_schedule_time_next_day(file_num, 1, daily_times=[16], timestamps=True)

    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # just avoid error, bilibili don't allow same title of video.
        title += random_emoji()
        tags_str = ','.join([tag for tag in tags])
        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")
        # I set desc same as title, do what u like.
        desc = title
        bili_uploader = BilibiliUploader(cookie_data, file, title, desc, tid, tags, timestamps[index])
        bili_uploader.upload()

        # life is beautiful don't so rush. be kind be patience
        time.sleep(30)


def publish_video(video_file):
    filepath = Path(video_file)
    if not filepath.exists() or not filepath.suffix == ".mp4":
        print(f"{filepath.name} 不是有效的 MP4 文件")
        exit()

    # 获取 cookie
    account_file = Path(BASE_DIR / "cookies" / "bilibili_uploader" / "account.json")
    if not account_file.exists():
        # print(f"{account_file.name} 配置文件不存在")
        account_file = Path(BASE_DIR / "uploader" / "bilibili_uploader" / "account.json")
        if not account_file.exists():
            print(f"{account_file.name} 配置文件不存在")
            exit()

    cookie_data = read_cookie_json_file(account_file)
    cookie_data = extract_keys_from_json(cookie_data)

    tid = VideoZoneTypes.SPORTS_FOOTBALL.value  # 设置分区id

    # 生成标题和标签
    title, tags = get_title_and_hashtags(str(filepath))
    title += random_emoji()  # 避免 B 站标题重复报错
    tags_str = ','.join(tags)

    print(f"视频文件名：{filepath}")
    print(f"标题：{title}")
    print(f"Hashtag：{tags}")

    desc = title  # 描述直接用标题

    # 上传
    bili_uploader = BilibiliUploader(cookie_data, filepath, title, desc, tid, tags, None)
    bili_uploader.upload()

    time.sleep(30)  # 防止频繁上传，适当间隔


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publish videos to Douyin.")
    parser.add_argument("video_path", type=str, help="video file.")

    args = parser.parse_args()
    publish_video(args.video_path)
