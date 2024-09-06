import docker
import os
import tarfile
import requests
from tqdm import tqdm
import sys

# Pull Image & Save Layer
# Image pull에 실패했을 때 최종 인덱스를 반환해서 다음 작업을 해당 인덱스부터 수행할 수 있게 만들어야 함
def download_and_save_image_layer(image_name, output_dir, platform="arm64"):
    client = docker.from_env()
    
    # docker.errors.APIError이 Limit가 발생했을 때 발생하는가?
    try:
        image = client.images.pull(image_name, platform=platform)
    except docker.errors.APIError as e:
        print(f"{platform} 플랫폼에 대한 {image_name} 이미지를 가져오는 중 오류 발생\n{e}")
        return -1
    
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
                
def docker_crawling(image_name, start_index):
    image_name_tag = []
    image_name_path = os.path.join("../data/images", image_name+"_name.txt")
    
    with open(image_name_path, 'r') as file:
        all_lines = file.readlines()
        if(start_index > len(all_lines)):
            return 1
        image_name_tag = all_lines[start_index : start_index+200]
        
    image_name_tag = [name.strip() for name in image_name_tag] # 파일에서 읽어올 때 발생한 개행문자 제거
    
    print(f"Get image and save layers - {image_name}({start_index})")
    for image in tqdm(image_name_tag):
        tag = image.split(":")[1].replace('.','_').replace('-','_')
        output_dir = "../image/" + image_name + "/" + tag
        
        os.makedirs(output_dir, exist_ok=True)

        return_code = download_and_save_image_layer(image, output_dir)
        if return_code == -1:
            os.rmdir(output_dir)

    return 0
        

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Input image_name and start_index")
        sys.exit(-1)
        
    image_name = sys.argv[1]
    start_index = int(sys.argv[2])

    sys.exit(docker_crawling(image_name, start_index))