import yt_dlp

def download_video(url, output_path="downloads"):
    ydl_opts = {
        "format": "bv*+ba/best",  # 最高画質の動画と音声を選択
        "merge_output_format": "mp4",  # mp4 形式で保存
        "outtmpl": f"{output_path}/%(title)s.%(ext)s",  # 出力ファイルの名前
        "noplaylist": True,  # プレイリストをダウンロードしない
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # mp4 に変換
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=Y-ysYMSLWDE"
    download_video(url)