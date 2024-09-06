#!/bin/bash

params=("$@")
IMAGE_COUNT=${#params[@]}
START_INDEX=0
IMAGE_INDEX=0

echo "IMAGE COUNT : $IMAGE_COUNT"

# Tag 불러오기
for param in "${params[@]}"; do
    echo "Get $param tag"
    python ../code/get_tag.py $param
done

while :
do
    REPOSITORY=${params[$IMAGE_INDEX]}
    python ../code/pull_and_save_image.py $REPOSITORY $START_INDEX
    STATUS=$?

    # DB에 저장하고 성공적으로 저장 이후 Delete 부분 추가

    if [ $STATUS -eq 0 ]; then # 성공적 다운로드
        START_INDEX=$(expr $START_INDEX + 200)
    elif [ $STATUS -eq 1 ]; then # 특정 Repository의 모든 Tag 다운로드 완료
        IMAGE_INDEX=$(expr $IMAGE_INDEX + 1)
        START_INDEX=0
        if [ $IMAGE_INDEX -eq $IMAGE_COUNT ]; then
            echo "Download All Repository and Image"
            break
        fi
    elif [ $STATUS -eq 2 ]; then # Docker Pull Limit 발생
        echo "Sleep 1 hours - Docker Pull Limit"
        sleep 3600 # 1시간 대기 후 다시 시작
        echo "Docker Pull Restart"
    else
        echo "Unexpected Error"
    fi
done