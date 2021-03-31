import ffmpeg
import os

file_dir = "C:\\Users\\KinG\\Desktop\\WOW"
file_list = os.scandir(file_dir)

if __name__ == '__main__':
    for file in file_list:
        input_video = file.path
        input_audio_name = file.path[0:-4] + '.webm'
        input_audio = ffmpeg.input(input_audio_name)
        output_file_name = file.path[0:-4] + '.' + 'mkv'
        ffmpeg_cmd = ".\\ffmpeg.exe" + " -i" + 'input_video' + " -i" + 'input_audio' + " -c copy " + 'output_file_name'
        os.system(ffmpeg_cmd)