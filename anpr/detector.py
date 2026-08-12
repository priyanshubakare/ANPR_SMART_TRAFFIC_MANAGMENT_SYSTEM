from pathlib import Path
import cv2
from ultralytics import YOLO
from .preprocessing import preprocess_plate
from .ocr import read_plate
from .traffic import traffic_decision

class ANPRPipeline:
    def __init__(self):
        self.plate_path = Path("weights/plate_detector.pt")
        self.plate_model = YOLO(str(self.plate_path)) if self.plate_path.exists() else None

    def health(self):
        return {
            "status": "ok",
            "yolov8_plate_model_loaded": self.plate_model is not None,
            "message": "Add weights/plate_detector.pt for actual plate detection."
        }

    def process(self, path, output_dir):
        image = cv2.imread(path)
        if image is None:
            raise ValueError("Could not read image")
        plates = []

        if self.plate_model is not None:
            results = self.plate_model.predict(source=image, conf=0.25, verbose=False)
            for result in results:
                if result.boxes is None:
                    continue
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                    conf = float(box.conf[0].cpu().item())
                    h, w = image.shape[:2]
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    crop = image[y1:y2, x1:x2]
                    if crop.size == 0:
                        continue
                    text = read_plate(preprocess_plate(crop))
                    plates.append({
                        "bbox": [int(x1), int(y1), int(x2), int(y2)],
                        "detection_confidence": round(conf, 4),
                        "text": text["text"],
                        "ocr_confidence": text["confidence"],
                    })

        annotated = image.copy()
        for p in plates:
            x1, y1, x2, y2 = p["bbox"]
            label = p["text"] or "PLATE"
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated, label, (x1, max(25, y1-8)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        out = Path(output_dir) / (Path(path).stem + "_result.jpg")
        cv2.imwrite(str(out), annotated)

        return {
            "plates": plates,
            "traffic": traffic_decision(plates),
            "result_image": out.name,
            "plate_model_loaded": self.plate_model is not None,
        }
