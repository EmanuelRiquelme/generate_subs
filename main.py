from faster_whisper import WhisperModel
from audio_pross import stream_stamps
import soundfile as sf
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from generate_sub import generate_json,add_subtitle,create_subtitle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name_video', type=str, help='The name of the video')

model_size = "large-v2"

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = 'cuda'
try:
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
except:
    model = WhisperModel(model_size, device="cuda", compute_type="int8")
def test_stream(video_name,num_secs = 5,model = model):
    create_subtitle(video_name)
    audio_vector,chunk_stamps,sample_rate = stream_stamps(video_name,num_secs)
    for idx in range(len(chunk_stamps)):
        left_range,right_range = chunk_stamps[idx]
        chunk = audio_vector[left_range:right_range]
        sf.write('temp.wav',chunk, sample_rate)
        segments, _ = model.transcribe('temp.wav', word_timestamps=True,language = 'en')
        for segment in segments:
            if segment.text != ' Thanks for watching!' and segment.text != ' You':
                text,start,end = segment.text,segment.start+idx*num_secs,segment.end+idx*num_secs
                json_file = generate_json(start,end,text)
                add_subtitle(video_name,json_file)

if __name__ == '__main__':
    args = parser.parse_args()
    video_name = args.name_video
    test_stream(video_name,num_secs = 10)
