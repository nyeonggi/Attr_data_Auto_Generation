import os
import json

# 약어 매핑 테이블
def parse_filename(filename):
    parts = filename.split('.')[0].split('_')
    
    short_map = {
    "male": "ma", "female": "fe",
    "kid": "ki", "adult": "ad", "elder": "el",
    "long": "lh", "short": "sh",
    "long sleeve": "lt", "short sleeve": "st",
    "pants": "pa", "long skirt": "ls", "short pants": "sp", "short skirt": "ss"
    }
    sex_map = {
    "ma": "남", 
    "fe": "여"
    }
    age_map = {
    "ki": "어린이", 
    "ad": "성인", 
    "el": "노인"
    }
    hair_map = {
    "lh": "긴 머리", 
    "sh": "짧은 머리"
    }
    top_map = {
    "lt": "긴 소매", 
    "st": "짧은 소매"
    }
    bottom_map = {
    "pa": "긴 바지", 
    "ls": "긴 치마", 
    "sp": "짧은 바지", 
    "ss": "짧은 치마"
    }
    color_map = {
    "re": "빨강색", "or": "주황색", "ye": "노랑색", "gr": "초록색", 
    "bl": "파랑색", "pu": "보라색", "pi": "핑크색", "br": "갈색", 
    "wh": "흰색", "gy": "회색", "bk": "검정색"
    }
    shoe_map = {
    "sn": "운동화", 
    "dr": "부츠/구두/하이힐",
    "sl": "샌들/슬리퍼", 
    }
    belongings_map = {
    "gl": ["안경"], 
    "ba": ["백팩"], 
    "gb": ["안경", "백팩"],
    "no": ["없음"]
    }

    # 대소문자 구분 없이 처리
    sex = sex_map.get(parts[0].lower(), "기타")
    age = age_map.get(parts[1].lower(), "기타")
    hair_type = hair_map.get(parts[2].lower(), "기타")
    top_type = top_map.get(parts[3].lower(), "기타")
    bottom_type = bottom_map.get(parts[4].lower(), "기타")
    top_color = color_map.get(parts[5].lower(), "기타")
    bottom_color = color_map.get(parts[6].lower(), "기타")
    shoe_color = color_map.get(parts[7].lower(), "기타")
    shoe_type = shoe_map.get(parts[8].lower(), "기타")
    belonging = belongings_map.get(parts[9].lower(), ["기타"])  # 리스트로 반환

    return {
        "성별": [sex],
        "연령": [age],
        "헤어 스타일": [hair_type],
        "상의 종류": [top_type],
        "하의 종류": [bottom_type],
        "상의 색상": [top_color],
        "하의 색상": [bottom_color],
        "신발 색상": [shoe_color],
        "신발 종류": [shoe_type],
        "소지품": belonging  # 리스트 그대로 반환
    }

# 기본값 추가 함수
def get_default_labels():
    return {
        "신체 보임": ["머리 등장", "상체 등장", "하체 등장"]
    }

# JSON 데이터 생성 함수
def create_task_json(image_path, filename, task_id):
    labels = parse_filename(filename)
    default_labels = get_default_labels()  # 기본값 가져오기
    
    # 기본값과 파일에서 파싱한 값을 병합
    combined_labels = {**default_labels, **labels}
    
    return {
        "id": task_id,
        "data": {
            "image": f"/data/local-files/?d=76f419d7-be2c-4cd4-bcfb-98e60eec92b5/mother_datasets/auto_attribute_gen/images/{filename}"
        },
        "predictions": [
            {
                "result": [
                    {
                        "from_name": key,
                        "to_name": "image",
                        "type": "choices",
                        "value": {
                            "choices": value  # 리스트로 값 출력
                        }
                    } for key, value in combined_labels.items()
                ]
            }
        ]
    }

# 디렉토리 내 모든 이미지 파일 처리 함수
def process_images(input_dir, output_json_file):
    task_id = 100000  # Task ID 초기값
    tasks = []
    
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            task = create_task_json(input_dir, filename, task_id)
            tasks.append(task)
            task_id += 1

    # JSON 파일로 저장
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)

    print(f"JSON 파일 생성 완료: {output_json_file}")

# 실행 예시
input_dir = "dataset"  # 이미지 파일이 저장된 디렉토리
output_json_file = "autolabelled.json"  # 생성할 JSON 파일 경로
process_images(input_dir, output_json_file)
