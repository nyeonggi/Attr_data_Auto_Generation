import json
from collections import Counter

def count_labels(file_path):
    # 결과를 저장할 Counter 객체 생성
    top_colors = Counter()
    bottom_colors = Counter()
    shoes_colors = Counter()
    shoes_types = Counter()
    belongings = Counter()

    # JSON 파일 읽기
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for task in data:
        predictions = task.get("predictions", [])
        for prediction in predictions:
            results = prediction.get("result", [])
            for result in results:
                from_name = result["from_name"]
                choices = result["value"]["choices"]
                
                if from_name == "상의 색상":
                    top_colors.update(choices)
                elif from_name == "하의 색상":
                    bottom_colors.update(choices)
                elif from_name == "신발 색상":
                    shoes_colors.update(choices)
                elif from_name == "신발 종류":
                    shoes_types.update(choices)
                elif from_name == "소지품":
                    if isinstance(choices, list):
                        belongings.update(item for sublist in choices for item in (sublist if isinstance(sublist, list) else [sublist]))
                    else:
                        belongings.update(choices)
    
    # 결과 출력 함수
    def print_sorted_counts(title, counter):
        sorted_counts = counter.most_common()  # 빈도순으로 정렬
        print(f"\n{title} (총 {sum(counter.values())}개)")
        for label, count in sorted_counts:
            print(f"{label}: {count}개")

    # 각 항목별로 출력
    print_sorted_counts("상의 색상 카운트", top_colors)
    print_sorted_counts("하의 색상 카운트", bottom_colors)
    print_sorted_counts("신발 색상 카운트", shoes_colors)
    print_sorted_counts("신발 종류 카운트", shoes_types)
    print_sorted_counts("소지품 카운트", belongings)

# JSON 파일 경로
file_path = "autolabelled.json"  # JSON 파일 경로를 여기에 입력하세요.
count_labels(file_path)
