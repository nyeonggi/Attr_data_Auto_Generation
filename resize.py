import cv2
import os
import random
import math
import argparse

# 랜덤 넓이 범위 설정
min_area = 3000
max_area = 20000

def resize_image_with_random_area(image, output_path):
    # 이미지를 직접 처리 (배열을 입력으로 받음)
    if image is None:
        print("잘못된 이미지 입력입니다.")
        return

    # 이미지 크기와 비율 계산
    h, w = image.shape[:2]
    aspect_ratio = w / h

    # 랜덤 넓이 선택
    target_area = random.randint(min_area, max_area)

    # 새 가로세로 크기 계산
    new_width = int(math.sqrt(target_area * aspect_ratio))
    new_height = int(new_width / aspect_ratio)

    # 이미지 리사이즈
    resized_image = cv2.resize(image, (new_width, new_height))

    # 리사이즈된 이미지 저장
    cv2.imwrite(output_path, resized_image)
    print(f"리사이즈된 이미지를 저장했습니다: {output_path}")

# 메인 함수
def main():
    # 인자 파서 설정
    parser = argparse.ArgumentParser(description="이미지 리사이즈 스크립트")
    parser.add_argument("input_dir", type=str, help="원본 이미지가 저장된 디렉토리 경로")
    parser.add_argument("output_dir", type=str, help="리사이즈된 이미지를 저장할 디렉토리 경로")
    args = parser.parse_args()

    # 출력 디렉토리 생성
    os.makedirs(args.output_dir, exist_ok=True)

    # 디렉토리 내 모든 이미지 파일에 대해 리사이즈 작업 수행
    for filename in os.listdir(args.input_dir):
        file_path = os.path.join(args.input_dir, filename)
        image = cv2.imread(file_path)  # 이미지 경로에서 배열로 읽어오기
        if image is not None:
            output_path = os.path.join(args.output_dir, filename)
            resize_image_with_random_area(image, output_path)
        else:
            print(f"이미지를 불러오지 못했습니다: {file_path}")

if __name__ == "__main__":
    main()
