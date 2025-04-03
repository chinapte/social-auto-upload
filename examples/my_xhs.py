import configparser
from pathlib import Path
from time import sleep

from xhs import XhsClient

from social_upload.conf import BASE_DIR
from social_upload.utils.files_times import generate_schedule_time_next_day, get_title_and_hashtags
from social_upload.uploader.xhs_uploader.main import sign_local, beauty_print

# 读取 .ini 文件内容
file_path = Path(BASE_DIR / "uploader" / "xhs_uploader" / "accounts.ini")

# 打开文件并读取内容
with open(file_path, 'r', encoding='utf-8') as file:
    cookies = file.read()

import argparse


def publish(video_dir):
    filepath = Path(BASE_DIR) / "videos"
    # 获取视频目录
    folder_path = Path(filepath)
    # 获取文件夹中的所有文件
    files = list(folder_path.glob("*.mp4"))
    file_num = len(files)

    xhs_client = XhsClient(cookies, sign=sign_local, timeout=60)
    # auth cookie
    # 注意：该校验cookie方式可能并没那么准确
    try:
        xhs_client.get_video_first_frame_image_id("3214")
    except:
        print("cookie 失效")
        exit()

    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])

    for index, file in enumerate(files):
        title, tags = get_title_and_hashtags(str(file))
        # 加入到标题 补充标题（xhs 可以填1000字不写白不写）
        tags_str = ' '.join(['#' + tag for tag in tags])
        hash_tags_str = ''
        hash_tags = []

        # 打印视频文件名、标题和 hashtag
        print(f"视频文件名：{file}")
        print(f"标题：{title}")
        print(f"Hashtag：{tags}")

        topics = []
        # 获取hashtag
        for i in tags[:3]:
            topic_official = xhs_client.get_suggest_topic(i)
            if topic_official:
                topic_official[0]['type'] = 'topic'
                topic_one = topic_official[0]
                hash_tag_name = topic_one['name']
                hash_tags.append(hash_tag_name)
                topics.append(topic_one)

        hash_tags_str = ' ' + ' '.join(['#' + tag + '[话题]#' for tag in hash_tags])

        note = xhs_client.create_video_note(title=title[:20], video_path=str(file),
                                            desc=title + tags_str + hash_tags_str,
                                            topics=topics,
                                            is_private=False,
                                            post_time=publish_datetimes[index].strftime("%Y-%m-%d %H:%M:%S"))

        beauty_print(note)
        # 强制休眠30s，避免风控（必要）
        sleep(30)


import os
from pathlib import Path
from time import sleep


def publish_video(video_file_path):
    filepath = Path(BASE_DIR) / "videos"
    # Get the folder path (you may not need this if only one file is used)
    folder_path = Path(filepath)

    # Validate if the video file exists
    file = Path(video_file_path)
    if not file.exists() or file.suffix != '.mp4':
        print(f"Invalid video file path: {video_file_path}. Please provide a valid .mp4 file.")
        return

    # Get the number of files (it will always be 1 in this case)
    file_num = 1

    # Assuming the cookies and other setup configurations are correct
    xhs_client = XhsClient(cookies, sign=sign_local, timeout=60)

    # Validate cookies (check if valid by trying to get a video)
    try:
        note = xhs_client.get_note_by_id("67cc4bdd000000002602cdf1", 'ABgeZhT4MoDfZq6ybkZPNpyEnJEs0kUsr7BDQrjGau7fQ=')
        print(note)
    except Exception as e:
        print(e.args)
        print("Cookie expired or invalid.")
        exit()

    # Generate the publish datetime for this single file
    publish_datetimes = generate_schedule_time_next_day(file_num, 1, daily_times=[16])

    title, tags = get_title_and_hashtags(str(file))
    # Create the tag string for the description
    tags_str = ' '.join(['#' + tag for tag in tags])
    hash_tags_str = ''
    hash_tags = []

    # Print video information
    print(f"视频文件名：{file}")
    print(f"标题：{title}")
    print(f"Hashtag：{tags}")

    topics = []
    # Get the suggested hashtags (only use the first 3 tags)
    for i in tags[:3]:
        topic_official = xhs_client.get_suggest_topic(i)
        if topic_official:
            topic_official[0]['type'] = 'topic'
            topic_one = topic_official[0]
            hash_tag_name = topic_one['name']
            hash_tags.append(hash_tag_name)
            topics.append(topic_one)

    # Create the full description with hashtags
    hash_tags_str = ' ' + ' '.join(['#' + tag + '[话题]#' for tag in hash_tags])

    # Create the video note
    note = xhs_client.create_large_video_note(
        title=title[:20],
        video_path=str(file),
        cover_path=str(file).replace('.mp4', '.jpg'),
        desc=title + tags_str + hash_tags_str,
        topics=topics,
        is_private=False,
        post_time=publish_datetimes[0].strftime("%Y-%m-%d %H:%M:%S")
    )

    # Print the note details
    beauty_print(note)

    # Sleep for 30 seconds to avoid risk controls
    sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Publish videos to Douyin.")
    parser.add_argument("video_path", type=str, help="video file.")

    args = parser.parse_args()
    publish_video(args.video_path)
