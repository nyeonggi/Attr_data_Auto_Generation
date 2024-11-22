# 도커환경 접속 전 로컬에서

from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import os
import urllib


load_dotenv()
key= os.getenv('TOGETHER_API_KEY')

# 크롬드라이버 실행
driver = webdriver.Chrome() 

#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://www.blinkshot.io/')
driver.maximize_window()


# 줄임말 맵핑
short_map = {
    "male": "ma", "female": "fe",
    "kid": "ki", "adult": "ad", "elder": "el",
    "long": "lh", "short": "sh",
    "long sleeve": "lt", "short sleeve": "st",
    "pants": "pa", "long skirt": "ls", "short pants": "sp", "short skirt": "ss",
    "glasses": "gl", "backpack": "ba", "glasses and backpack": "gb", "": "no"
}

# 한글-영어 매핑 리스트
choices_map = {
    "성별": ["남성", "여성"],
    "성별_영어": ["male", "female"],
    "연령": ["어린이", "성인", "노인"],
    "연령_영어": ["kid", "adult", "elder"],
    "헤어 스타일": ["긴 머리", "짧은 머리"],
    "헤어 스타일_영어": ["long", "short"],
    "상의 종류": ["긴 소매", "짧은 소매"],
    "상의 종류_영어": ["long sleeve", "short sleeve"],
    "하의 종류": ["긴 바지", "긴 치마", "짧은 바지", "짧은 치마"],
    "하의 종류_영어": ["pants", "long skirt", "short pants", "short skirt"],
    "소지품": ["안경", "백팩", "안경, 백팩", "없음"],
    "소지품_영어": ["glasses", "backpack", "glasses and backpack", ""]
}


# 사용자 선택 함수
def get_user_choice(options, name):
    print(f"{name} 선택:")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    choice = int(input(f"선택 번호(1-{len(options)}): ")) - 1
    return choice  # 인덱스 반환

# 사용자 선택
sex_index = get_user_choice(choices_map["성별"], "성별")
age_index = get_user_choice(choices_map["연령"], "연령")
hair_index = get_user_choice(choices_map["헤어 스타일"], "헤어 스타일")
top_index = get_user_choice(choices_map["상의 종류"], "상의 종류")
bottom_index = get_user_choice(choices_map["하의 종류"], "하의 종류")
belong_index = get_user_choice(choices_map["소지품"], "소지품")

# 영어 선택값 가져오기
sex = choices_map["성별_영어"][sex_index]
age = choices_map["연령_영어"][age_index]
hair = choices_map["헤어 스타일_영어"][hair_index]
top = choices_map["상의 종류_영어"][top_index]
bottom = choices_map["하의 종류_영어"][bottom_index]
belong = choices_map["소지품_영어"][belong_index]

# sex= ["female", "male"]
# age= ["kid", "adult", "elder"]
# hair= ["long", "short"]
# top= ["long sleeve", "short sleeve"]
# bottom= ["pants", "long skirt", "short pants", "short skirt"]
# belong= ["glasses", "backpack", "glasses and backpack", ""]
# 색상       ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "gray", "black"]


top_colors= ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "gray", "black"]
bottom_colors= ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "gray", "black"]
shoes_colors= ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "white", "gray", "black"]
shoes_list= ["sneakers", "dress shoes", "slides"]
num= 1

def get_color_short(color):
    if color == "gray":
        return "gy"  # gray는 gy로 변환
    elif color == "black":
        return "gk"  # black은 bk로 변환
    else:
        return color[:2]  # 나머지는 앞 두 글자 반환

for t_color in top_colors:
    for b_color in bottom_colors:
        for s_color in shoes_colors:
            for shoes in shoes_list:
                    prompt = f"""
                    Full-body shot of a korean {sex} {age} with {hair} hair wearing 
                    a {t_color} {top} and {b_color} {bottom}
                    and {s_color} {shoes} with {belong}
                    shown from a distance with one's entire body visible,
                    one's face should be in view
                    """
                    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[2]/input').send_keys(key)
                    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/fieldset/div[1]/textarea').send_keys(prompt)

                    # 줄임말 변환
                    t_color_short = get_color_short(t_color)
                    b_color_short = get_color_short(b_color)
                    s_color_short = get_color_short(s_color)
                    
                    for i in range(num):
                        time.sleep(5)
                        image_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/img')
                        image_url = image_element.get_attribute("src")
                        
                        # 파일명 생성
                        filename = f"{short_map[sex]}_{short_map[age]}_{short_map[hair]}_{short_map[top]}_{short_map[bottom]}_" \
                                   f"{t_color_short}_{b_color_short}_{s_color_short}_{shoes[:2]}_{short_map[belong]}_{i+1}.jpg"

                        urllib.request.urlretrieve(image_url, os.path.join('dataset', filename))

                        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/fieldset/div[1]/textarea').send_keys(" ")
                        print("Saved:", filename)
                    
                    driver.refresh()
