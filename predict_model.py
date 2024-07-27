# load data
import pickle
from shutil import move

import librosa
import noisereduce as nr
import numpy as np
import sounddevice as sd
# load data
from scipy.io import wavfile
from scipy.io.wavfile import write


def move_files(flag):

    print("Moving Files")
    if flag == 1:

        for i in range(1,6):
            move("./Crying Baby/Baby_Cry"+str(i)+".wav",
                 "./Crying Baby/Baby_Cry"+str(i)+".wav")

    else:
        for i in range(1, 6):
            move("./Silence/Silent_" + str(i) + ".wav",
                 "./Silence/Silent_" + str(i) + ".wav")


def predict():
    file = open("AudioModel.pkl", "rb")
    Model = pickle.load(file)

    # Sampling frequency
    frequency = 44100

    # Recording duration in seconds
    duration = 6

    # to record audio from
    # sound-device into a Numpy
    recording = sd.rec(int(duration * frequency),
                       samplerate=frequency, channels=1)

    # Wait for the audio to complete
    sd.wait()

    # using scipy to save the recording in .wav format
    # This will convert the NumPy array
    # to an audio file with the given sampling frequency
    write("recording0.wav", rate=frequency, data=recording)
    rate, data = wavfile.read("recording0.wav")

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)

    wavfile.write("New.wav", rate=rate, data=reduced_noise)


    filename = "New.wav"
    audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')

    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)


    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

    predicted_label = Model.predict(mfccs_scaled_features)


    return predicted_label, filename