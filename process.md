main.py를 통해 전처리과정 통합 완료.
도커환경 켜기전에 blinkshot_crawling.py로 이미지부터 dataset에 생성
그 후 도커환경 실행 후 main.py로 이미지 전처리
python3 main.py
imgtojsn.py로 파일명 파싱하여 오토라벨링 정보(predict) json파일로 저장
이미지가 서버에 저장되어 있다는 가정하에 json파일을 label studio에 import
