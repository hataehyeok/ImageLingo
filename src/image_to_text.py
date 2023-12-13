import pytesseract
from pytesseract import Output
import cv2
import numpy as np
from collections import namedtuple
import re

Rectangle = namedtuple('Rectangle', ['xmin', 'ymin', 'xmax', 'ymax'])



class Levels:
    PAGE = 1
    BLOCK = 2
    PARAGRAPH = 3
    LINE = 4
    WORD = 5


def intersect_area(a, b):
    dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
    dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)

    return float(dx*dy) if (dx >= 0) and (dy >= 0) else 0.


def normalize_images(images):
    return [cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            if image.ndim == 2 else image for image in images]


def threshold_image(img_src):
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img_thresh, img_gray


def mask_image(img_src, lower, upper):
    img_hsv = cv2.cvtColor(img_src, cv2.COLOR_BGR2HSV)
    hsv_lower = np.array(lower, np.uint8)
    hsv_upper = np.array(upper, np.uint8)

    img_mask = cv2.inRange(img_hsv, hsv_lower, hsv_upper)

    return img_mask, img_hsv

def apply_mask(img_src, img_mask):

    img_result = cv2.bitwise_and(img_src, img_src, mask=img_mask)

    return img_result


def denoise_image(img_src):

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    img_denoise = cv2.morphologyEx(
        img_src, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return img_denoise 

def draw_word_boundings(img_src, data_ocr, highlighted_words=False):

    img_result = cv2.cvtColor(img_src, cv2.COLOR_GRAY2BGR) if img_src.ndim == 2 else img_src.copy()

    for i in range(len(data_ocr['text'])):
        if data_ocr['level'][i] != Levels.WORD:
            continue
        if highlighted_words and not data_ocr['highlighted'][i]:
            continue
        (x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
                        [i], data_ocr['width'][i], data_ocr['height'][i])
        cv2.rectangle(img_result, (x, y), (x + w, y + h), (0, 0, 255), 2)

    return img_result


def draw_contour_boundings(img_src, img_mask, threshold_area=400):
    contours, hierarchy, = cv2.findContours(
        img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    img_contour = img_src.copy()
    img_box = img_src.copy()

    for idx, c in enumerate(contours):
        if  cv2.contourArea(c) < threshold_area:
            continue

        cv2.drawContours(img_contour, contours, idx, (0, 0, 255), 2, cv2.LINE_4, hierarchy)

        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(img_box, (x, y), (x + w, y + h), (255, 0, 0), 2, cv2.LINE_AA, 0)

    return img_contour, img_box

def draw_contour_rectangles(img_contour, img_result, rect_width=10, rect_height=10, threshold_percentage=25):

    threshold = (rect_width * rect_height * threshold_percentage) / 100

    contours, hierarchy, = cv2.findContours(
        img_contour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for idx, c in enumerate(contours):

        xmin, ymin, w, h = cv2.boundingRect(c)
        xmax = xmin + w
        ymax = ymin + h

        for x in range(xmin, xmax, rect_width):
            for y in range(ymin, ymax, rect_height):
                rect_roi = Rectangle(x, y, x+rect_width, y+rect_height)
                img_roi = img_contour[y:y+rect_height, x:x+rect_width]

                count = cv2.countNonZero(img_roi)

                if count > threshold:
                    cv2.rectangle(img_result, (rect_roi.xmin, rect_roi.ymin),
                                  (rect_roi.xmax, rect_roi.ymax),
                                  (255, 0, 0), 1, cv2.LINE_AA, 0)

    return img_result



def find_highlighted_words(img_mask, data_ocr, threshold_percentage=25):

    data_ocr['highlighted'] = [False] * len(data_ocr['text'])

    for i in range(len(data_ocr['text'])):
        (x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
                        [i], data_ocr['width'][i], data_ocr['height'][i])
        rect_threshold = (w * h * threshold_percentage) / 100
        img_roi = img_mask[y:y+h, x:x+w]
        count = cv2.countNonZero(img_roi)
        if count > rect_threshold:
            data_ocr['highlighted'][i] = True

    return data_ocr


def mark_highlighted_words(img_result, data_ocr):
    for i in range(len(data_ocr['text'])):
        if data_ocr['level'][i] != Levels.WORD:
            continue
        if not data_ocr['highlighted'][i]:
            continue

        (x, y, w, h) = (data_ocr['left'][i], data_ocr['top']
                        [i], data_ocr['width'][i], data_ocr['height'][i])
        rect_roi = Rectangle(x, y, x+w, y+h)

        cv2.rectangle(img_result, (rect_roi.xmin, rect_roi.ymin),
                      (rect_roi.xmax, rect_roi.ymax), (0, 255, 0), 2)

    return img_result


def draw_text(
    img,
    *,
    text,
    uv_top_left,
    color=(255, 255, 255),
    fontScale=0.5,
    thickness=1,
    fontFace=cv2.FONT_HERSHEY_COMPLEX,
    outline_color=(0, 0, 0),
    line_spacing=1.5,
):

    assert isinstance(text, str)

    uv_top_left = np.array(uv_top_left, dtype=float)
    assert uv_top_left.shape == (2,)

    for line in text.splitlines():
        (w, h), _ = cv2.getTextSize(
            text=line,
            fontFace=fontFace,
            fontScale=fontScale,
            thickness=thickness,
        )
        uv_bottom_left_i = uv_top_left + [0, h]
        org = tuple(uv_bottom_left_i.astype(int))

        if outline_color is not None:
            cv2.putText(
                img,
                text=line,
                org=org,
                fontFace=fontFace,
                fontScale=fontScale,
                color=outline_color,
                thickness=thickness * 3,
                lineType=cv2.LINE_AA,
            )
        cv2.putText(
            img,
            text=line,
            org=org,
            fontFace=fontFace,
            fontScale=fontScale,
            color=color,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )

        uv_top_left += [0, h * line_spacing]

def draw_separation_lines(img_src, images=1):
    height, width = img_src.shape[:2]
    img_result = img_src.copy()

    for i in range(1, images):
        x = int((width / images) * i)
        img_result = cv2.line(img_result, (x, 0), (x, height), (255, 255, 255), thickness=2)

    return img_result

def words_to_string(data_ocr):
    word_list = []
    line_breaks = (Levels.PAGE, Levels.BLOCK, Levels.PARAGRAPH, Levels.LINE)

    for i in range(len(data_ocr['text'])):


        if data_ocr['level'][i] in line_breaks:
            word_list.append("\n")
            continue

        text = data_ocr['text'][i].strip()

        if text and data_ocr['highlighted'][i]:
            word_list.append(text + " ")

    word_string = "".join(word_list)
    word_string = re.sub(r'\n+', '\n', word_string).strip()

    return word_string


def image_to_data(img_src):
    return pytesseract.image_to_data(
        img_src, lang='eng', config='--psm 6', output_type=Output.DICT)


def image_to_string(img_src):
    return pytesseract.image_to_string(
        img_src, lang='eng', config='--psm 6')

def _extract_voca_list(args):
    img_input = str(args.img_input)

    img_orig = cv2.imread(img_input)
    img_thresh, img_gray = threshold_image(img_orig)
    data_ocr = image_to_data(img_thresh)
    hsv_lower = [22, 30, 30]
    hsv_upper = [45, 255, 255]
    img_mask, img_hsv = mask_image(
        img_orig, hsv_lower, hsv_upper)

    img_mask_denoised = denoise_image(
        img_mask)

    data_ocr = find_highlighted_words(
        img_mask_denoised, data_ocr, threshold_percentage=25)

    string_ocr = pytesseract.image_to_string(
        img_thresh, lang='eng', config='--psm 6')
        
    print("\n\n")
    print(string_ocr)
    print("\n\n")

    str_highlight = words_to_string(data_ocr)
    return str_highlight

def extract_voca_list(image_path):
    class Args:
            def __init__(self, img_input):
                self.img_input = img_input
    from pathlib import Path
    img_input_path = image_path
    img_input = Path(img_input_path)
    args = Args(img_input)
    return _extract_voca_list(args)
