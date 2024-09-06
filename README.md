# DockerCrawling

## Prerequisites
- Ubuntu : 20.04.6 LTS
- Python : v3.9.19
- Anaconda3 : v23.7.4
- docker : v26.1.4

## How to use?
1. Run Install_Anaconda.sh
2. Run Create_Env.sh
3. Run Install_Docker.sh
    - 해당 부분 우분투 버전(20.04, 22.04, ...)에 따라 다른 조건으로 실행될 수 있는 스크립트로 수정해야 함(자동화 추가)
4. Run get_tag.py or pull_and_save_image.py
    - 해당 부분은 스크립트 파일로 대체 예정

## Code
1. get_tag.py
- 원하는 이미지의 태그를 불러와서 txt파일로 태그, 이미지 전체 이름 저장

2. pull_and_save_image.py
- 원하는 이미지와 start_index를 설정하여 200개의 이미지를 pull & save

## Etc
**To-Do List**
- Architecture x86-64만 다운로드 받도록 필터링 설정
    -> tag 받을 떄 정보 뜯어봐서 Architecture 설정 확인해서 x86만 저장하면 괜찮을 듯

- Docker Image Layer 분석
- DB에 어떤 형태로 저장할건지? DB 설계
- 쉘 스크립트로 자동화 -> Docker Image Pull limit 확인해서 특정 시간마다 요청
- DB에 저장한 후 해당 이미지에 대한 데이터를 삭제한 후 다른 이미지를 Pull
    -> Python 코드 내에서 작업 진행해도 괜찮을거 같음
- 중복되는 Layer는 어떻게 확인하고 저장을 하지 않을건지?