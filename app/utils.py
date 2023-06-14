from datetime import datetime
import os, math
from pydub import AudioSegment
import shortuuid, bcrypt, sqlalchemy
from . import config

AUDIO_PATH = "{base_path}/audio/".format(base_path=os.getcwd())

def calculate_sleep_time(from_time, to_time):

    datetime1 = datetime.fromisoformat(from_time)
    datetime2 = datetime.fromisoformat(to_time)

    return (datetime2 - datetime1).total_seconds()

def get_aac_audio_length(file_path):
    audio = AudioSegment.from_file(file_path, format="aac")
    duration_in_minutes = len(audio) / 60000  # Convert milliseconds to seconds
    return duration_in_minutes

def aac_to_wav(aac_file):
    audio = AudioSegment.from_file(aac_file, format="aac")
    wav_file = AUDIO_PATH+ shortuuid.uuid()+"converted.wav"
    audio.export(wav_file, format="wav")

    return wav_file


def calculate_sleep_noise(wav_file):

    # Load the WAV file
    audio = AudioSegment.from_file(wav_file)

    # Calculate the root mean square (RMS)
    rms = audio.rms

    # Convert RMS to decibels (dB)
    sleep_noise = 20 * math.log10(rms)

    #  Remove the temporary WAV file
    # os.remove(wav_file)

    return sleep_noise

def save_file(audio_recording):
    audio_file = audio_recording
    
    if audio_file:
        folder_path = os.getcwd() + "/audio" # Get the current working directory
        if not os.path.exists(folder_path):
            # Create the folder
            os.makedirs(folder_path)
        audioname = shortuuid.uuid()+audio_file.filename
        file_path = os.path.join(folder_path, audioname)  # Join root folder path with the filename
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

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a TCP connection pool for a Cloud SQL instance of MySQL."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    db_host = config["DATABASE"][
        "INSTANCE_HOST"
    ]  # e.g. '127.0.0.1' ('172.17.0.1' if deployed to GAE Flex)
    db_user = config["DATABASE"]["DB_USER"]  # e.g. 'my-db-user'
    db_pass = config["DATABASE"]["DB_PASS"]  # e.g. 'my-db-password'
    db_name = config["DATABASE"]["DB_NAME"]  # e.g. 'my-database'
    db_port = config["DATABASE"]["DB_PORT"]  # e.g. 3306

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        # ...
    )
    return pool