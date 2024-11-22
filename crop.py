import os 
import argparse
import numpy as np
import cv2
import torch
#1
def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images", default="", type=str, help="Path to images directory to crop images from.")
    parser.add_argument("--save", default="", type=str, help="Path to save cropped images.")
    parser.add_argument("--labels", default="", type=str, help="Path to the label files directory.")
    opt = parser.parse_args()
    return opt

def xywhn2xyxy(x, w=640, h=640, padw=0, padh=0):
    """Convert normalized boxes to xyxy format"""
    y = x.clone() if isinstance(x, torch.Tensor) else np.copy(x)
    y[..., 0] = w * (x[..., 0] - x[..., 2] / 2) + padw  # top left x
    y[..., 1] = h * (x[..., 1] - x[..., 3] / 2) + padh  # top left y
    y[..., 2] = w * (x[..., 0] + x[..., 2] / 2) + padw  # bottom right x
    y[..., 3] = h * (x[..., 1] + x[..., 3] / 2) + padh  # bottom right y
    return y

def save_img(img, name, save_path):
    """Save the cropped images to the given directory"""
    save_file = os.path.join(save_path, name)
    cv2.imwrite(save_file, img)

def find_image_path(images_path, image_name):
    """Attempt to find an image with various possible extensions"""
    extensions = [".jpg", ".jpeg", ".png"]
    for ext in extensions:
        image_path = os.path.join(images_path, image_name + ext)
        if os.path.exists(image_path):
            return image_path
    return None

def crop_logo(images_path, save, labels):
    """Crop images based on YOLO labels and save to the specified directory."""
    cropped_images = {}  # 크롭된 이미지를 저장할 딕셔너리
    annotations = os.listdir(labels)
    
    for annot in annotations:
        image_name = annot.rsplit('.', 1)[0].strip()
        image_path = find_image_path(images_path, image_name)
        annot_path = os.path.join(labels, annot)

        if image_path is not None:
            img = cv2.imread(image_path)
            height, width = img.shape[:2]
            with open(annot_path) as f:
                annotation = []
                line = f.readline() 
                annot = [float(num) for num in line.split(" ")]
                annotation.append(annot[1:])
            annotation = np.array(annotation)
            boxes = xywhn2xyxy(annotation, w=width, h=height)
            for box in boxes:
                x_top, y_top, x_bottom, y_bottom = int(box[0]) + 3, int(box[1]) + 3, int(box[2]) - 3, int(box[3]) - 3
                cropped_img = img[y_top: y_bottom, x_top: x_bottom]
                
                # 메모리에 저장
                cropped_images[image_name] = cropped_img
                save_img(cropped_img, image_name + ".jpg", save)
        else:
            print(f"Image for {image_name} not found in {images_path}!")
    
    return cropped_images  # 크롭된 이미지를 반환



def main():
    args = read_args()
    crop_logo(args.images, args.save, args.labels)
    print("done!")

if __name__ == "__main__":
    main()
