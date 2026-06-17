Proyek ini menggunakan YOLOv8 untuk mendeteksi kacang yang berjamur (Moldy) dan yang sehat (NotMoldy), lengkap dengan antarmuka web berbasis Flask.

## Langkah-langkah Penggunaan (Steps):

1. **Persiapan Dataset**:
   - Dataset disimpan di Google Drive dalam format ZIP (`PeanutDataset.zip`).
   - Ekstrak dataset ke direktori `/content/peanut_dataset`.

2. **Pembagian Data (Data Splitting)**:
   - Data dibagi menjadi 70% Train, 15% Validation, dan 15% Test menggunakan skrip Python.

3. **Konfigurasi Model**:
   - Menggunakan file `data.yaml` untuk mendefinisikan path ke folder train, val, dan test.
   - Kelas yang dideteksi: `Moldy` dan `NotMoldy`.

4. **Pelatihan Model (Training)**:
   - Model dilatih menggunakan `yolov8n.pt` selama 50 epoch.
   - Hasil terbaik (`best.pt`) disimpan di folder `weights`.

5. **Evaluasi & Inferensi**:
   - Hasil pelatihan dapat dilihat pada grafik `results.png` dan `confusion_matrix.png`.
   - Gunakan fungsi `model.predict()` untuk melakukan deteksi pada gambar baru.

6. **Penyimpanan**:
   - Model yang sudah dilatih dikirim kembali ke Google Drive dan di-upload ke repository GitHub ini.

7. **Menjalankan Interface (Flask Web App)**:
   - **Persiapan Environment**:
     Pastikan Anda memiliki Python terinstal, lalu buat virtual environment:
     ```bash
     python -m venv env
     source env/bin/activate  # Untuk Linux/macOS
     env\\Scripts\\activate     # Untuk Windows
     ```
   - **Instalasi Library**:
     Instal dependensi yang diperlukan:
     ```bash
     pip install flask ultralytics opencv-python pillow
     ```
   - **Struktur Folder**:
     Pastikan file `app.py` berada di root, folder `templates/` berisi file HTML, dan model `best.pt` berada di path yang sesuai.
   - **Menjalankan Aplikasi**:
     ```bash
     python app.py
     ```
     Buka browser dan akses `http://127.0.0.1:5000`.
"""
