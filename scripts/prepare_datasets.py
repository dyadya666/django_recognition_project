import os
import numpy as np
import librosa

DATASET_PATH = "dataset"
CLASS_NAMES = sorted([p for p in os.listdir(DATASET_PATH) if not p.startswith('.')])

X, y = [], []

def extract_features(file_path, max_pad_len=128):
    audio, sr = librosa.load(file_path, sr=16000)
    melspec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
    logspec = librosa.power_to_db(melspec)
    if logspec.shape[1] < max_pad_len:
        pad_width = max_pad_len - logspec.shape[1]
        logspec = np.pad(logspec, pad_width=((0,0),(0,pad_width)), mode='constant')
    else:
        logspec = logspec[:, :max_pad_len]
    return logspec

for idx, label in enumerate(CLASS_NAMES):
    folder = os.path.join(DATASET_PATH, label)
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            path = os.path.join(folder, file)
            features = extract_features(path)
            X.append(features)
            y.append(idx)

X = np.array(X)[..., np.newaxis]  # (N,128,128,1)
y = np.array(y)

np.save("X.npy", X)
np.save("y.npy", y)
np.save("class_names.npy", CLASS_NAMES)

print("Dataset prepared:", X.shape, y.shape, CLASS_NAMES)
