from moviepy.editor import AudioFileClip


def extract_audio(file_path, export_path):
    try:
        with AudioFileClip(file_path) as file:
            file.write_audiofile(export_path)
        return True
    except Exception as err:
        print("err: ", err)
    return False

