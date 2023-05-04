import cv2
import mediapipe as mp
import time
from dataclasses import dataclass
import numpy as np
import imageio

@dataclass
class Logged_Detection:
    """Class for keeping track of an item in inventory."""
    bbox_x: int
    bbox_y: int
    old_width: int
    old_height: int
    bbox:tuple
    age: int

def blur(source:str, output:str):
    
    cap = cv2.VideoCapture(source)
    fps = cap.get(cv2.CAP_PROP_FPS)
    writer = imageio.get_writer(output, fps=fps)

    mpFaceDetection = mp.solutions.face_detection
    faceDetection = mpFaceDetection.FaceDetection( min_detection_confidence=0.0,model_selection=1)


    detect_set = []

    success, img = cap.read()
    height = img.shape[0]
    width = img.shape[1]
    print(f"Blurring video {source} of size {width}x{height} and framerate {fps} fps")
    
    if success:
        while True:
            img = cv2.resize(img, (width, height))
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = faceDetection.process(imgRGB)

            if results.detections:
                for id, detection in enumerate(results.detections):
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, ic = img.shape
                    
                    bbox_x = int(bboxC.xmin * iw); bbox_y = int(bboxC.ymin * ih)
                    old_width = int(bboxC.width * iw); old_height = int(bboxC.height * ih)
                    if bbox_x<0:bbox_x = 0
                    if bbox_y<0:bbox_y = 0

                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    detect_set += [Logged_Detection(bbox_x,bbox_y,old_width,old_height,bbox,0)]


            for d in detect_set:
                    img[d.bbox_y:d.bbox_y+d.old_height,d.bbox_x:d.bbox_x+d.old_width] = cv2.medianBlur( img[d.bbox_y:d.bbox_y+d.old_height,d.bbox_x:d.bbox_x+d.old_width],75)
                    d.age += 1

            detect_set = [d for d in detect_set if d.age< 20]
            
            im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            writer.append_data(np.asarray(im_rgb))

            cv2.imshow("Blurred Video", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
            success, img = cap.read()
            if not success:
                break
        
    cap.release()
    writer.close()
    cv2.destroyAllWindows()