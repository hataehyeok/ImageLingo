import cv2
import pytesseract
from PIL import Image
import numpy as np

def extract_highlighted_text(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([20, 80, 80])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    highlighted = cv2.bitwise_and(image, image, mask=mask)
    pil_image = Image.fromarray(cv2.cvtColor(highlighted, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_image)
    
    return text
