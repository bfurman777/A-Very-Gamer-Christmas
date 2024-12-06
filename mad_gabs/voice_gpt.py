import pyaudio
import wave
import os
import whisper
from datetime import datetime

# Function to record audio
def record_audio(filename, duration=10, rate=44100, channels=2, chunk_size=1024):
    # Set up the audio stream
    p = pyaudio.PyAudio()

    # Open a stream to record audio from the microphone
    stream = p.open(format=pyaudio.paInt16, 
                    channels=channels, 
                    rate=rate, 
                    input=True, 
                    frames_per_buffer=chunk_size)

    print("Recording...")

    # Initialize an empty list to store frames of audio
    frames = []

    # Record audio for the specified duration
    for i in range(0, int(rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    # Stop the stream
    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio as a .wav file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {filename}")
    
    return filename

# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    # Load the Whisper model (this will automatically download it if not present)
    model = whisper.load_model("base")  # You can use "small", "medium", "large" based on your need

    # Transcribe the audio file
    result = model.transcribe(filename)
    
    # Print the transcription text
    print("\nTranscription:\n")
    print(result["text"])

# Main function to execute recording and transcription
if __name__ == "__main__":
    # Define the file path for saving the recording
    
    file_name = f"recorded_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    
    # Check if the file already exists and prompt for a new name if needed
    if os.path.exists(file_name):
        print(f"File '{file_name}' already exists. Please specify a new file name.")
        transcribe_audio(file_name)

    else:
        # Start recording (e.g., record for 10 seconds)
        recorded_file = record_audio(file_name, duration=10)
        
        # Transcribe the recorded audio using Whisper
        transcribe_audio(recorded_file)
