#!/usr/bin/env python
"""
Written by Kang.Chen
Download from youtube.
"""
import os
import datetime

download_url = ["https://www.youtube.com/watch?v=sDsh0dJg0bQ&list=PL17RctH5HKX6XSLIhpRBGNVhbMiULUcWy"]


def download_youtube_video(download_youtube_url):
    for url in download_youtube_url:
        timestamp_1 = datetime.datetime.now()
        download_cmd = "youtube-dl" \
                       + " --proxy " \
                       + "socks5://127.0.0.1:10808/" \
                       + " -ciw " \
                       + " -f 137 " \
                       + "--cache-dir  C:\\Users\\KinG\\Desktop " \
                       + url
        os.system(download_cmd)
        timestamp_2 = datetime.datetime.now()
        print("Finish Download <<<", url, ">>>, Time use is", timestamp_2 - timestamp_1)


def download_youtube_audio(download_youtube_url):
    for url in download_youtube_url:
        timestamp_1 = datetime.datetime.now()
        download_cmd = "youtube-dl" + " --proxy " + "socks5://127.0.0.1:10808/" \
                       + " -ciw " \
                       + " -f 140 " \
                       + url
        os.system(download_cmd)
        timestamp_2 = datetime.datetime.now()
        print("Finish Download <<<", url, ">>>, Time use is", timestamp_2 - timestamp_1)

def main():
    """
    Let's fly
    """
    timestamp0 = datetime.datetime.now()
    # Begin Download youtube video process.
    download_youtube_video(download_url)
    download_youtube_audio(download_url)
    # Just a runtime collection.
    timestamp10 = datetime.datetime.now()
    print("Finish all Download Jobs, all time use is ", timestamp10 - timestamp0)


# start this thing
if __name__ == "__main__":
    main()
