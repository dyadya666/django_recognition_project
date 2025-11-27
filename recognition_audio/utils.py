import numpy as np
import librosa
import keras


MODEL = keras.models.load_model('models/audio_classifier.keras')
CLASS_NAMES = np.load("class_names.npy").tolist()

def classify_audio(path, max_pad_len=128):
    y, sr = librosa.load(path, sr=16000)
    melspec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=max_pad_len)
    logspec = librosa.power_to_db(melspec)
    if logspec.shape[1] < max_pad_len:
        pad_width = max_pad_len - logspec.shape[1]
        logspec = np.pad(logspec, ((0, 0), (0, pad_width)), mode='constant')
    else:
        logspec = logspec[:, :max_pad_len]

    logspec = np.expand_dims(logspec, axis=-1)  # (128,128,1)
    logspec = np.expand_dims(logspec, axis=0)   # (1,128,128,1)

    preds = MODEL.predict(logspec)[0]
    idx = np.argmax(preds)
    return {
        'label': CLASS_NAMES[idx],
        'confidence': float(preds[idx])
    }
