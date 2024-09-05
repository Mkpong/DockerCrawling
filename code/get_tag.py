import docker
import os
import tarfile
import requests
from tqdm import tqdm
import sys

# Image name을 통해 모든 tag를 받고 리스트 형태로 저장
def get_tag(image):
    tags = []
    page_size = 100
    
    image_name = "library/"+image
    
    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags"
    response = requests.get(url)
    count = response.json()['count']
    total_page = count//100 + 1
    print(f"Get tag - {image_name} (Total={count})")
    
    for page in tqdm(range(1, total_page+1 , 1), desc=f"Get tag({image_name})"):
        url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/?page_size={page_size}&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Page{page} : 태그 정보를 가져오지 못했습니다: {response.status_code} - {response.text}")
        tags_info = response.json()['results']
        for tag in tags_info:
            tags.append(tag['name'])

    save_data(image, tags)
    return tags
    
    

def save_data(image_name, tags):
    tag_file_path = os.path.join("../data/tags", image_name+"_tags"+".txt")
    image_file_path = os.path.join("../data/images", image_name+"_name"+".txt")
    
    os.makedirs("../data/tags", exist_ok=True) # tags 폴더가 존재하지 않으면 생성
    os.makedirs("../data/images", exist_ok=True) # iamges 폴더가 존재하지 않으면 생성
    
    with open(tag_file_path, 'w') as file:
        for tag in tags:
            file.write(tag+'\n')
            
    with open(image_file_path, 'w') as file:
        for tag in tags:
            image = "library/"+image_name+":"+tag
            file.write(image+'\n')
            
    
if __name__=="__main__":
    images = sys.argv[1:]
    
    if not images:
        print("적어도 하나 이상의 이미지 이름을 입력하세요.")
        exit(1)
    
    for image in images:
        get_tag(image)