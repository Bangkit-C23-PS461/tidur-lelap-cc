from keras.models import load_model
import os
# Model Path
MODEL_PATH = "{base_path}/ml/Stress-Level-Classification.hdf5".format(base_path=os.getcwd())
SR = 55.52  # Snoring range in dB
RR = 19.1   # Snoring rate in bpm
SD = 6.1    # Sleep duration in hour

# Model predict function
def predict_stress(model_path=MODEL_PATH, snoring_range=SR, snoring_rate=RR, sleep_duration=SD):
    # Load variables
    model = load_model(model_path, compile=False)

    # Predict stress level
    data = [[snoring_range, snoring_rate, sleep_duration]]
    result = model.predict(data)
    result = list(result[0])
    stess_level = result.index(max(result)) + 1 # Stress level range from 1 to 5

    # return ({
    #     "stress_level_array": result,
    #     "stress_level": stess_level
    # })

    return stess_level

# print(predict())