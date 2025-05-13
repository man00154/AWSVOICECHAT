import wave
import pyaudio

def record_audio(output_file, duration=5, rate=16000, chunk=1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
    
    print("Recording...")
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        frames.append(stream.read(chunk))
    print("Recording stopped.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

def play_audio(file_path):
    audio = pyaudio.PyAudio()
    with wave.open(file_path, "rb") as wf:
        stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
        data = wf.readframes(1024)
        while data:
            stream.write(data)
            data = wf.readframes(1024)
        stream.stop_stream()
        stream.close()
    audio.terminate()
