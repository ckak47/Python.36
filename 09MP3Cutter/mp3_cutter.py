from pydub import AudioSegment
import ffmpeg

files_path = "D:\\"
file_name = "YsMl4m6bsBp49W8kuaBtApRFSAgZntNbqv3Hlmdv"

startMin = 0
startSec = 0

endMin = 1
endSec = 59

# Time to miliseconds
startTime = startMin*60*1000+startSec*1000
endTime = endMin*60*1000+endSec*1000

# Opening file and extracting segment
song = AudioSegment.from_mp3("D:\\YsMl4m6bsBp49W8kuaBtApRFSAgZntNbqv3Hlmdv.mp3")
extract = song[startTime:endTime]

# Saving
extract.export("D:\\YsMl4m6bsBp49W8kuaBtApRFSAgZntNbqv3Hlmdv_converted.mp3", format="mp3")