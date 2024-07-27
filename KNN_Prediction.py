import pickle

import librosa
import noisereduce as nr
import numpy as np
import sounddevice as sd
# load data
from scipy.io import wavfile
from scipy.io.wavfile import write

file = open("AudioModel.pkl","rb")
Model = pickle.load(file)

# Sampling frequency
frequency = 22050

# Recording duration in seconds
duration = 5

# to record audio from
# sound-device into a Numpy
recording = sd.rec(int(duration * frequency),
                   samplerate=frequency, channels=1)

# Wait for the audio to complete
sd.wait()

# using scipy to save the recording in .wav format
# This will convert the NumPy array
# to an audio file with the given sampling frequency
write("recording0.wav", rate=frequency,data=recording)

# using wavio to save the recording in .wav format
# This will convert the NumPy array to an audio
# file with the given sampling frequency
#wv.write("recording1.wav",rate=frequency, data=recording, sampwidth=2)

rate, data = wavfile.read("recording0.wav")
print("rate: ",rate)
# perform noise reduction
reduced_noise = nr.reduce_noise(y=data, sr=rate)

wavfile.write("New.wav", rate = rate, data = reduced_noise)
print("redduced noise: ",reduced_noise)

filename="New.wav"
audio, sample_rate = librosa.load(filename, res_type='kaiser_fast')
print("sample_rate: ",sample_rate)
mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)

print("mfccs_scaled_features: ",mfccs_scaled_features)
mfccs_scaled_features=mfccs_scaled_features.reshape(1,-1)
print("mfccs_scaled_features: ",mfccs_scaled_features)
print("mfccs_scaled_features: ",mfccs_scaled_features.shape)
predicted_label=Model.predict(mfccs_scaled_features)
print("predicted_label: ",predicted_label)

if predicted_label == 1:
    print("Baby is Crying")
else:
    print("Baby is Silent")