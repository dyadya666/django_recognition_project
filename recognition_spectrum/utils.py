import librosa
import librosa.display
import matplotlib
matplotlib.use("Agg")  # без GUI
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid


def analyze_spectrum(path):
    y, sr = librosa.load(path, sr=16000)
    # FFT
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1/sr)

    # Знаходимо піки
    # топ-5 частот
    peaks = freqs[np.argsort(spectrum)[-5:]]
    peaks = sorted(peaks)

    return {
        "dominant_frequencies": [float(f) for f in peaks],
        "max_amplitude": float(np.max(spectrum)),
        "mean_amplitude": float(np.mean(spectrum))
    }

def save_spectrogram(file_path, out_dir="media/spectrograms"):
    """
    Побудова та збереження спектрограми сигналу у PNG.
    Кожен файл отримує унікальне ім'я, щоб уникнути перезапису.
    """
    # Завантажуємо сигнал
    y, sr = librosa.load(file_path, sr=16000)
    melspec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    logspec = librosa.power_to_db(melspec)

    # Готуємо директорію
    os.makedirs(out_dir, exist_ok=True)

    # Формуємо унікальне ім'я файлу
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    unique_id = uuid.uuid4().hex[:8]
    file_name = f'{base_name}_{unique_id}.png'
    out_path = os.path.join(out_dir, file_name)

    # Малюємо спектрограму
    plt.figure(figsize=(6, 4))
    librosa.display.specshow(logspec, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Mel Spectrogram")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

    # Повертаємо шлях відносно MEDIA_URL
    return os.path.join("spectrograms", file_name)
