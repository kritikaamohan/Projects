import os
import wave
import time
import threading
import tkinter as tk
import pyaudio

class VoiceRecorder:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Recorder")
        self.root.resizable(False, False)
        self.button = tk.Button(self.root, text="🎤", font=("Arial", 120, "bold"), fg="black", bg="red", command=self.click_handler)
        self.button.pack(pady=20)
        self.label = tk.Label(self.root, text="00:00:00", fg="white", bg="black", font=("Arial", 24))
        self.label.pack(pady=10)
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(bg="red")
        else:
            self.recording = True
            self.button.config(bg="green")
            threading.Thread(target=self.record).start()
            threading.Thread(target=self.update_timer).start()

    def update_timer(self):
        start_time = time.time()
        while self.recording:
            elapsed = int(time.time() - start_time)
            hours = elapsed // 3600
            mins = (elapsed % 3600) // 60
            secs = elapsed % 60
            self.label.config(text=f"{hours:02d}:{mins:02d}:{secs:02d}")
            time.sleep(1)

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
        frames = []
        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        folder = os.path.join(os.getcwd(), "Recordings")
        os.makedirs(folder, exist_ok=True)
        i = 1
        while os.path.exists(os.path.join(folder, f"recording{i}.wav")):
            i += 1
        file_name = os.path.join(folder, f"recording{i}.wav")
        with wave.open(file_name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b"".join(frames))
        print(f"Recording saved as {file_name}")

VoiceRecorder()
