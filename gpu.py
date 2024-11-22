import torch

# 사용 가능한 GPU 확인
print(torch.cuda.current_device())  # 현재 사용 중인 GPU 번호
print(torch.cuda.get_device_name(torch.cuda.current_device()))  # GPU 이름 출력
