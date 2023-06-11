from datetime import datetime
import app
import librosa, os

def calculate_sleep_time(from_time, to_time):

    datetime1 = datetime.fromisoformat(from_time)
    datetime2 = datetime.fromisoformat(to_time)

    return (datetime2 - datetime1).total_seconds()

def calculate_sleep_noise(aac_file):
    # Load the audio file
    audio, _ = librosa.load(aac_file)
    
    # Convert stereo to mono if necessary
    if audio.ndim > 1:
        audio = librosa.to_mono(audio)
    
    # Calculate the root mean square (RMS) energy of the audio
    rms = librosa.feature.rms(y=audio)
    
    # Compute the average RMS energy
    avg_rms = rms.mean()
    
    # Convert the average RMS energy to decibels (dB)
    avg_rms_db = librosa.amplitude_to_db(avg_rms)
    
    return avg_rms_db

def save_audio_file(audio_recording):
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
