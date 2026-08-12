# ANPR Smart Traffic Management System

Portfolio-ready starter project using Python, YOLOv8, OpenCV, EasyOCR and Flask.

Pipeline:
Input image -> YOLOv8 plate detection -> OpenCV preprocessing -> OCR -> traffic decision -> REST API/dashboard

## Important
This package contains the application code, but not a trained license-plate model or dataset.
Place your trained YOLOv8 plate model at `weights/plate_detector.pt`.

Do not claim an accuracy number until you measure it on a held-out test set.

## Setup

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Training
Prepare a YOLO-format dataset and edit `dataset/data.yaml`, then:
```bash
python train_plate_detector.py
```

Copy the resulting best weights to:
`weights/plate_detector.pt`

## API
POST `/api/detect` with multipart field `file`.
GET `/api/health`.

## Resume-safe workflow
Document your actual dataset, train/validation/test split, YOLOv8 configuration, detection metrics, OCR accuracy and false positives/negatives. Only report measured results.
