import librosa
def calculate_sleep_noise(aac_file):
    # Load the audio file
    audio, _ = librosa.load(aac_file)
    
    # Convert stereo to mono if necessary
    if audio.ndim > 1:
        audio = librosa.to_mono(audio)
    
    # Calculate the root mean square (RMS) energy of the audio
    rms = librosa.feature.rms(y=audio)
    
    # Compute the average RMS energy
    avg_rms = [rms.mean()]
    
    # Convert the average RMS energy to decibels (dB)
    avg_rms_db = librosa.amplitude_to_db(avg_rms)
    
    return avg_rms_db

aac_file = "/Users/v-ramadhana.w/Documents/tidur-lelap-cc/audio/sample3.aac"
print(calculate_sleep_noise(aac_file))