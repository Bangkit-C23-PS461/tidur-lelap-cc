from datetime import datetime
import os, math
from pydub import AudioSegment

def calculate_sleep_time(from_time, to_time):

    datetime1 = datetime.fromisoformat(from_time)
    datetime2 = datetime.fromisoformat(to_time)

    return (datetime2 - datetime1).total_seconds()

def get_aac_audio_length(file_path):
    audio = AudioSegment.from_file(file_path, format="aac")
    duration_in_minutes = len(audio) / 60000  # Convert milliseconds to seconds
    return duration_in_minutes

def calculate_sleep_noise(aac_file):
    # Convert AAC to WAV
    audio = AudioSegment.from_file(aac_file, format="aac")
    wav_file = "converted.wav"
    audio.export(wav_file, format="wav")

    # Load the WAV file
    audio = AudioSegment.from_file(wav_file)

    # Calculate the root mean square (RMS)
    rms = audio.rms

    # Convert RMS to decibels (dB)
    sleep_noise = 20 * math.log10(rms)

    # Remove the temporary WAV file
    os.remove(wav_file)

    return sleep_noise

def save_file(audio_recording):
    audio_file = audio_recording
    
    if audio_file:
        folder_path = os.getcwd() + "/audio" # Get the current working directory
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
        file_path = os.path.join(folder_path, audio_file.filename)  # Join root folder path with the filename
        audio_file.save(file_path)
        return file_path
    
    return ""

def remove_file(file_path: str):
    try:
        os.remove(file_path)
        print("File removed successfully.")
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied - unable to remove the file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")