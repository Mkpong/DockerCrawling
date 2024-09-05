import docker
import os
import tarfile
import requests
from tqdm import tqdm
import sys

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
                
def docker_crawling(image_name, start_index):
    image_name_tag = []
    image_name_path = os.path.join("../data/images", image_name+"_name.txt")
    
    with open(image_name_path, 'r') as file:
        all_lines = file.readlines()
        image_name_tag = all_lines[start_index : start_index+200]
        
    image_name_tag = [name.strip() for name in image_name_tag] # 파일에서 읽어올 때 발생한 개행문자 제거
    
    print(f"Get image and save layers - {image_name}")
    for image in tqdm(image_name_tag):
        tag = image.split(":")[1].replace('.','_').replace('-','_')
        output_dir = "../images/" + image_name + "/" + tag
        
        os.makedirs(output_dir, exist_ok=True)

        download_and_save_image_layer(image, output_dir)
        

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Input image_name and start_index")
        exit(1)
        
    image_name = sys.argv[1]
    start_index = int(sys.argv[2])

    docker_crawling(image_name, start_index)