import docker
import os
import tarfile
import requests
from tqdm import tqdm

# Pull Image & Save Layer
def download_and_save_image_layer(image_name, output_dir):
    client = docker.from_env()
    
    image = client.images.pull(image_name)
    
    image_tar_path = os.path.join(output_dir, f"{image_name.replace(':', '_')}.tar")
    
    os.makedirs(os.path.dirname(image_tar_path), exist_ok=True)
    
    with open(image_tar_path, 'wb') as image_tar:
        for chunk in image.save(named=True):
            image_tar.write(chunk)
    
    with tarfile.open(image_tar_path, 'r') as tar:
        tar.extractall(path=output_dir)
        
    for member in os.listdir(output_dir):
        if member.endswith('.tar'):
            layer_tar_path = os.path.join(output_dir, member)
            layer_output_dir = os.path.join(output_dir, member.replace('.tar' , ''))
            os.makedirs(layer_output_dir, exist_ok=True)
            
            with tarfile.open(layer_tar_path, 'r') as layer_tar:
                layer_tar.extractall(path=layer_output_dir)

# 태그 불러오기
def fetch_image_tags(image_name):
    tags = []
    page_size = 100

    # Get Total Image Count
    url = f"https://hub.docker.com/v2/repositories/{image_name}/tags"
    response = requests.get(url)
    count = response.json()['count']
    total_page = count//100 + 1

    # Get Tag (All image)
    # Try Catch로 예외처리 추가하기 -> API 호출 리미트 측정
    print(f"Get tag - {image_name} / Total={count}")
    for page in tqdm(range(1, total_page+1 , 1), desc=f"Get tag({image_name})"):
        url = f"https://hub.docker.com/v2/repositories/{image_name}/tags/?page_size={page_size}&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Page{page} : 태그 정보를 가져오지 못했습니다: {response.status_code} - {response.text}")
        tags_info = response.json()['results']
        for tag in tags_info:
            tags.append(tag['name'])

    print()
    return tags

def docker_crawling(image_name):
    for name in image_name:
        image_name_tag = []
        image_path = "library/" + name

        tags=fetch_image_tags(image_path)

        for tag in tags:
            image_name_tag.append(image_path+":"+tag)

        print(f"Get image and save layers - {name}")
        for image in tqdm(image_name_tag):
            tag = image.split(":")[1]
            tag = tag.replace('.', '_').replace('-', '_')
            output_dir = "./" + name + "/" + tag
            
            os.makedirs(output_dir, exist_ok=True)

            download_and_save_image_layer(image, output_dir)
        print()
            
        
            
if __name__=='__main__':
    docker_crawling(["nginx" , "node"])

    