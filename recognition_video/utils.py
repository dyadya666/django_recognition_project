import cv2
import numpy as np
import os
import tempfile


def extract_keyframes(video_path, every_n_frames=30):
    """
    Повертає список шляхів до тимчасових зображень (jpg), витягнутих з відео.
    every_n_frames: інтервал кадрів (наприклад, 30 => ~1 кадр за секунду при 30fps)
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0
    success, frame = cap.read()
    while success:
        if idx % every_n_frames == 0:
            fd, tmp_path = tempfile.mkstemp(suffix='.jpg')
            os.close(fd)
            cv2.imwrite(tmp_path, frame)
            frames.append((idx, tmp_path))

        idx += 1
        success, frame = cap.read()
    cap.release()

    return frames

def classify_frames(frames, classifier_fn, top_n=1):
    """
    frames: список (frame_index, path)
    classifier_fn: функція, що приймає шлях до зображення і повертає рядок/структуру
    Повертає список dict з результатами.
    """
    results = []
    for idx, path in frames:
        try:
            res = classifier_fn(path)
            results.append({'frame': idx, 'path': path, 'result': res})
        except Exception as e:
            results.append({'frame': idx, 'path': path, 'result': f'Error: {e}'})
    
    return results

def cleanup_paths(frames):
    for _, path in frames:
        try:
            os.remove(path)
        except OSError:
            pass
