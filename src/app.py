import numpy as np
import streamlit as st
import deli_audio_analysis as analyzer
import pandas as pd
import logging
from io import BytesIO
from rich.logging import RichHandler

logging.basicConfig(level=logging.NOTSET, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])

def main():
    st.title("聲音頻譜分析")

    uploaded_file = st.file_uploader("上傳一個音訊檔案", type=["wav", "mp3", "ogg"])

    if uploaded_file is not None:
        st.subheader("音訊檔案資訊")
        st.write(f"檔案名稱: {uploaded_file.name}")
        st.audio(uploaded_file, format="audio/*")

        st.subheader("頻譜分析")
        audio_bytes = uploaded_file.read()
        audio, sr = analyzer.load_audio(BytesIO(audio_bytes))

        if audio is not None and sr is not None:
            fft_result, frequencies = analyzer.calculate_fft(audio, sr)

            if fft_result is not None and frequencies is not None:
                spectrogram_plot = analyzer.plot_spectrogram(fft_result, frequencies, sr)
                if spectrogram_plot:
                    st.pyplot(spectrogram_plot)

                # 可選: 提取更多特徵以供神經網路使用 (範例)
                # mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
                # st.subheader("MFCC 特徵 (範例)")
                # st.write(mfccs)

                # 可選: 使用預訓練的神經網路模型進行預測 (範例)
                # st.subheader("神經網路分析 (範例)")
                # # 假設您已經載入了一個訓練好的模型
                # # model = tf.keras.models.load_model('your_trained_model.h5')
                # # prediction = analyzer.predict_audio_class(model, mfccs)
                # # st.write(f"預測類別: {prediction}")
            else:
                st.error("無法計算頻譜。")
            
            # 傅立葉轉換分析
            st.subheader("頻譜分析 (傅立葉轉換)")
            fft_magnitude, frequencies_fft = analyzer.analyze_fft_spectrum(audio, sr)
            if fft_magnitude is not None and frequencies_fft is not None:
                fft_spectrum_plot = analyzer.plot_fft_spectrum(fft_magnitude, frequencies_fft)
                if fft_spectrum_plot:
                    st.pyplot(fft_spectrum_plot)
                # 準備匯出傅立葉轉換數據
                    fft_data = pd.DataFrame({'頻率 (Hz)': frequencies_fft, '幅度': fft_magnitude})

                    # 匯出按鈕 (XLSX)
                    def download_fft_xlsx():
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            fft_data.to_excel(writer, sheet_name='傅立葉轉換數據', index=False)
                        processed_data = output.getvalue()
                        return processed_data

                    st.download_button(label="匯出傅立葉轉換數據為 XLSX",
                                       data=download_fft_xlsx(),
                                       file_name="fft_data.xlsx",
                                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

                    # 匯出按鈕 (CSV)
                    def download_fft_csv():
                        csv_data = fft_data.to_csv(index=False).encode('utf-8')
                        return csv_data

                    st.download_button(label="匯出傅立葉轉換數據為 CSV",
                                       data=download_fft_csv(),
                                       file_name="fft_data.csv",
                                       mime="text/csv")
            else:
                st.error("無法進行傅立葉轉換分析。")
        else:
            st.error("無法載入音訊檔案。")

if __name__ == "__main__":
    main()