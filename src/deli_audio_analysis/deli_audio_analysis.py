import librosa
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf  # 導入 TensorFlow
from rich import traceback

traceback.install()

def load_audio(audio_file):
    """載入音訊檔案。"""
    try:
        audio, sr = librosa.load(audio_file)
        return audio, sr
    except Exception as e:
        print(f"載入音訊檔案時發生錯誤: {e}")
        return None, None

def calculate_fft(audio, sr):
    """計算音訊的快速傅立葉轉換 (FFT)。"""
    if audio is None:
        return None, None
    n_fft = 2048  # FFT 視窗大小
    hop_length = 512  # 相鄰 FFT 視窗之間的步幅
    fft_result = np.abs(librosa.stft(audio, n_fft=n_fft, hop_length=hop_length))
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    return fft_result, frequencies

def plot_spectrogram(fft_result, frequencies, sr):
    """繪製頻譜圖。"""
    if fft_result is None or frequencies is None:
        return None
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.amplitude_to_db(fft_result, ref=np.max),
                             sr=sr, x_axis='time', y_axis='log',
                             x_coords=librosa.frames_to_time(np.arange(fft_result.shape[1]),
                                                            sr=sr, hop_length=512),
                             y_coords=frequencies)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    return plt

def analyze_fft_spectrum(audio, sr):
    """對整個音訊進行傅立葉轉換分析。"""
    if audio is None:
        return None, None
    n_fft = len(audio)
    frequencies = np.fft.fftfreq(n_fft, d=1/sr)
    fft_magnitude = np.abs(np.fft.fft(audio))
    # 只取正頻率部分
    positive_frequency_indices = np.where(frequencies > 0)
    frequencies = frequencies[positive_frequency_indices]
    fft_magnitude = fft_magnitude[positive_frequency_indices]
    return fft_magnitude, frequencies

def plot_fft_spectrum(fft_magnitude, frequencies):
    """繪製傅立葉轉換後的頻譜。"""
    if fft_magnitude is None or frequencies is None:
        return None
    plt.figure(figsize=(10, 4))
    plt.plot(frequencies, fft_magnitude)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("FFT Transform")
    plt.grid(True)
    plt.tight_layout()
    return plt

# 可選: 使用 TensorFlow 建立一個簡單的神經網路模型 (範例)
# def create_neural_network_model(input_shape):
#     model = tf.keras.models.Sequential([
#         tf.keras.layers.Dense(128, activation='relu', input_shape=input_shape),
#         tf.keras.layers.Dense(10, activation='softmax') # 假設有 10 個類別
#     ])
#     model.compile(optimizer='adam',
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])
#     return model

# 可選: 使用模型進行預測 (範例)
# def predict_audio_class(model, features):
#     # 將特徵塑造成模型期望的形狀
#     features = np.expand_dims(features, axis=0)
#     predictions = model.predict(features)
#     return np.argmax(predictions)