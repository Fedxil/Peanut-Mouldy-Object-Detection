import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO
from flask import Flask, request, render_template
import io
import base64
import os


app = Flask(__name__, template_folder='template')

# --- 1. LOAD MODEL ---
model_path = 'Peanut_Model_v1/weights/best.pt'
try:
    model = YOLO(model_path)
except Exception as e:
    print(f"Gagal memuat model YOLO: {e}")
    model = None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if model is None:
            return render_template('home.html', error="Model YOLO tidak tersedia atau gagal dimuat.")
        
        if 'file' not in request.files:
            return render_template('home.html', error="Tidak ada file yang diunggah.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('home.html', error="File tidak valid.")

        try:
            # Baca gambar dalam memori dan konversi ke Array
            image = Image.open(file.stream).convert("RGB")
            img_array = np.array(image)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            
            # --- 3. JALANKAN PREDIKSI & GAMBAR BOUNDING BOX ---
            results = model.predict(source=img_bgr, conf=0.80, augment=True, save=False)
            res = results[0]
            count_moldy, count_healthy = 0, 0

            for box in res.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf, cls = float(box.conf[0]), int(box.cls[0])
                label_name = res.names[cls]
                
                color = (0, 0, 255) if label_name == 'Moldy' else (0, 255, 0)
                count_moldy += 1 if label_name == 'Moldy' else 0
                count_healthy += 1 if label_name != 'Moldy' else 0
                label_text = f"Moldy {conf:.2f}" if label_name == 'Moldy' else "Sehat"
                
                cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 6)
                cv2.putText(img_bgr, label_text, (x1, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            # Konversi kembali ke RGB dan Encode ke Base64
            img_result_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            result_image = Image.fromarray(img_result_rgb)
            buffered = io.BytesIO()
            result_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            return render_template('home.html', image_data=img_str, count_moldy=count_moldy, count_healthy=count_healthy)
            
        except Exception as e:
            return render_template('home.html', error=f"Terjadi kesalahan saat memproses gambar: {e}")

    return render_template('home.html')

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1']
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)