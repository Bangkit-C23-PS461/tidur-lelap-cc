import tensorflow as tf
import subprocess, shortuuid, os
from keras.models import load_model
import os

# Model Path
MODEL_PATH = "{base_path}/ml/Snoring-Detection-Model-44100.hdf5".format(base_path=os.getcwd())
AUDIO_PATH = "{base_path}/audio/fat_guy _snoring.aac".format(base_path=os.getcwd())
AUDIO_PATH_WAV = "audio.wav"


# Load audio
def load_audio_data(audio_path=AUDIO_PATH, audio_dest=AUDIO_PATH_WAV, duration=1):
    # Convert aac to wav and load audio
    # NOTE: PLEASE INSTALL FFMPEG, MORE INFO AT https://ffmpeg.org/
    # subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-acodec", "pcm_s16le", "-ar", "44100", audio_dest])
    audio = tf.io.read_file(audio_dest)
    audio, sample_rate = tf.audio.decode_wav(audio, desired_channels=-1)

    # Divide for each second
    chunk_size = int(duration * sample_rate)
    audio_chunks = []
    for i in range(0, audio.shape[0], chunk_size):
        chunk = audio[i:i+chunk_size]

        # Add zero padding if chunk size is different
        if chunk.shape[0] != chunk_size:
            zero_padding = tf.zeros([chunk_size - chunk.shape[0], 1], dtype=tf.float32)
            chunk = tf.concat([zero_padding, chunk],0)
        
        audio_chunks.append(chunk)

    audio_chunks = tf.data.Dataset.from_tensor_slices(audio_chunks)
    audio_chunks = audio_chunks.map(lambda x: tf.squeeze(x, axis=-1))
    return audio_chunks


# Change shape with fourier transform
def preprocess_audio(wav):
    wav = wav[:44100]
    spectrogram = tf.signal.stft(wav, frame_length=256, frame_step=128)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    return spectrogram


# Model predict function
def predict_snore(model_path=MODEL_PATH, audio_path=AUDIO_PATH, threshold=0.5):
    # Load variables
    model = load_model(model_path, compile=False)
    audio_data = load_audio_data(audio_path,audio_path)
    audio_data = audio_data.map(preprocess_audio)

    # Batch audio data for each second
    audio_data_batch = audio_data.batch(1)

    # Predict audio data
    result = model.predict(audio_data_batch)

    # Count snore base on confidence threshold
    count = 0
    for el in result:
        if el >= threshold:
            count += 1

    # return ({
    #     "result": result,
    #     "count": count
    # })

    return count

# print(predict_snore())