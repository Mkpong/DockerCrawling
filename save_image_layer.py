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

    