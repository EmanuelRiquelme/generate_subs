from moviepy.editor import VideoFileClip
import numpy as np
import soundfile as sf

def extract_wav_vector(video_name):
    video = VideoFileClip(video_name)
    sample_rate = video.audio.fps
    audio = video.audio
    audio_vector = np.array(audio.to_soundarray())
    return audio_vector,sample_rate

def stream_stamps(video_name,num_seconds = 5):
    audio_vector,sample_rate = extract_wav_vector(video_name)
    chunk = sample_rate*num_seconds
    num_chunks = int(audio_vector.shape[0]//chunk)
    chunk_range = []
    for idx_chunk in range(num_chunks):
        chunk_range.append(chunk*idx_chunk)
    chunk_stamps = []
    for idx_chunk in range(len(chunk_range)-1):
        chunk_stamps.append([chunk_range[idx_chunk],chunk_range[idx_chunk+1]])
    chunk_stamps.append([chunk_range[-1],audio_vector.shape[0]])
    return audio_vector,chunk_stamps,sample_rate

def test_stream(video_name):
    audio_vector,chunk_stamps,sample_rate = stream_stamps(video_name)
    for idx in range(len(chunk_stamps)):
        left_range,right_range = chunk_stamps[idx]
        audio = audio_vector[left_range:right_range]
        sf.write('tone.wav',audio, sample_rate)
