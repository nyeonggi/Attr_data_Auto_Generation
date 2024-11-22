import os
import argparse
from detect import detect
from crop import crop_logo
from resize import resize_image_with_random_area
from utils.general import increment_path

def main():
    parser = argparse.ArgumentParser(description="YOLO Detection and Preprocessing Pipeline")
    parser.add_argument("--input_dir", type=str, default="/yolov7/dataset", help="Path to input image directory")
    parser.add_argument("--output_dir", type=str, default="/yolov7/attr_learning", help="Path to save preprocessed images")
    parser.add_argument("--weights", type=str, default="/yolov7/yolov7.pt", help="Path to YOLO weights")
    parser.add_argument("--conf_thres", type=float, default=0.25, help="YOLO confidence threshold")
    parser.add_argument("--iou_thres", type=float, default=0.45, help="YOLO IOU threshold")
    parser.add_argument("--img_size", type=int, default=640, help="YOLO image size")
    args = parser.parse_args()

    # YOLO detect.py 실행
    os.system(f"python detect.py --source {args.input_dir} --weights {args.weights} --conf-thres {args.conf_thres} "
              f"--iou-thres {args.iou_thres} --img-size {args.img_size} --save-txt --project {args.output_dir} "
              f"--name detect_results --exist-ok")

    # Crop 단계
    cropped_images = crop_logo(
        images_path=args.input_dir,
        save=os.path.join(args.output_dir, "cropped"),
        labels=os.path.join(args.output_dir, "detect_results", "labels")
    )
    
    print("Cropping complete. Resizing images...")

    # Resize 단계: 고유한 resized 폴더 생성
    resized_output_dir = increment_path(os.path.join(args.output_dir, "source_image"), exist_ok=False)
    os.makedirs(resized_output_dir, exist_ok=True)
    
    for image_name, cropped_img in cropped_images.items():
        output_path = os.path.join(resized_output_dir, f"{image_name}.jpg")
        resize_image_with_random_area(cropped_img, output_path)

    print(f"Preprocessing complete. Final images saved to {resized_output_dir}")

if __name__ == "__main__":
    main()
