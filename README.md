# Attr_Data__Auto_Generation
## Person Attribute Image Auto-Generation, Auto-Preprocessing, Auto-Labelling

3단계에 걸쳐 진행
1. 사람 속성 이미지 생성 (Auto-Generation)
2. 이미지 전처리 (Auto-Preprocessing)
3. 속성 특징 json파일로 저장 (Auto-Labelling)

1단계는 윈도우 환경  
2단계는 도커 환경  
3단계는 둘 다 가능 

## Installation
Local<br>
<details><summary> <b>Expand</b> </summary>

``` shell
pip install selenium
pip install python_dotenv
```

</details>

<br><br>
Docker enviroment (recommended)  
<details><summary> <b>Expand</b> </summary>

``` shell
# Base image with CUDA support
FROM nvidia/cuda:12.2.0-base-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    git \
    zip htop screen libgl1-mesa-glx \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgtk2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    

    # Set Python alias
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy YOLOv7 files into the container

WORKDIR /yolov7
COPY . /yolov7
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose a default command (you can modify this later)
CMD ["bash"]
```

</details>


## Auto-Generation

"""  
Full-body shot of a korean {sex} {age} with {hair} hair wearing  
a {t_color} {top} and {b_color} {bottom}  
and {s_color} {shoes} with {belong}  
shown from a distance with one's entire body visible,  
one's face should be in view  
"""  
  
  
blinkshot_crawling.py을 이용하여 blinkshot.io를 crawling하여 이미지 생성 및 저장  
1. https://www.blinkshot.io/ 이동하여 회원가입/로그인 후 API키 발급<br><br>
2. .env파일 생성후 API키 입력 -> TOGETHER_API_KEY=<api key><br><br>
3. blingshot_crawling.py 실행 시, 1차적으로 **성별, 연령, 헤어 스타일, 상의 종류, 하의 종류, 소지품**를 입력해야 함  
*해당 속성은 일반적인 입력을 요구 (남자+짧은치마X)*<br><br>
4. 입력한 값을 바탕으로 **상의 색상, 하의 색상, 신발 색상, 신발 종류**을 각 각의 속성들이 1대1 매핑되게 for문을 이용하여 사진 생성  
*기본적으로 색상은 11가지 전부 들어가있고 필요할 경우 코드 내부의 {top_colors}, {bottom_colors}, {shoes_colors}를 수정*<br><br>
5. 생성된 파일명은 성별_연령_헤어스타일_상의종류_하의종류_상의색상_하의색상_신발색상_신발종류_소지품_num.jpg 형식으로 저장됨  
*->이 후에 파일명을 parsing하여 json파일로 저장함, auto_labelling하기위한 작업*<br><br>
  
## Preprocessing
1. 도커환경이 구축된 상태에서 git clone한 폴더를 root_dir로 설정하여 컨테이너 생성<br>
*예시: docker run --gpus all -it --name yolov7-container -v <git_clone_dir>:/<root_dir> yolov7-image*<br><br>
2. main.py 실행<br><br>
3. attr_learning폴더 자동 생성 후, source_image폴더에 detect->crop->resize된 이미지 저장<br><br>
  
## Auto-labelling
1. imgtojsn.py 실행<br><br>
2. dataset의 이미지들이 label-studio에 import되어있다면,<br>
생성된 json파일을 project에 import했을 때 predict로 auto-labelling됨

