from ultralytics import YOLO
import cv2
import numpy as np
from os import chdir, path, getcwd
from time import time
from PARAMETERS import IMGSZ, CONFIDENCE
from miscellaneous import get_available_filename


def just_predict(image_path, file_name, model, imgsz, conf, save=False):
    results = model.predict(image_path, imgsz = imgsz, conf=conf)
    image = cv2.imread(image_path)
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Result', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if save:
        chdir("saved_results")
        file_name = get_available_filename(file_name)
        cv2.imwrite(file_name, image)

if __name__ == "__main__":
    file_name = "snapshot_44.jpg"
    image_path = path.join("testing_imgs",file_name)
    weights = "best.pt"

    just_predict(image_path=image_path, file_name=file_name, model=YOLO(weights), imgsz=IMGSZ, conf=CONFIDENCE, save=True)