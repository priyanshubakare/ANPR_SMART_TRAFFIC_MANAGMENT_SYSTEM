import re
from functools import lru_cache
import easyocr

@lru_cache(maxsize=1)
def reader():
    return easyocr.Reader(["en"], gpu=False)

def clean(text):
    return re.sub(r"[^A-Z0-9]", "", text.upper())

def read_plate(image):
    results = reader().readtext(image, detail=1, paragraph=False)
    candidates = []
    for _, text, conf in results:
        text = clean(text)
        if text:
            candidates.append({"text": text, "confidence": round(float(conf), 4)})
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    return candidates[0] if candidates else {"text": "", "confidence": 0.0}
