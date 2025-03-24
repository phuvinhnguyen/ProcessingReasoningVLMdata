import json
from data import *
from datasets import load_dataset
import requests
import zipfile
import os
from pathlib import Path

class SLAKE:
    download_link = 'https://huggingface.co/datasets/BoKelvin/SLAKE/resolve/main/imgs.zip'
    huggingface = 'BoKelvin/SLAKE'

    def __init__(self, local_dir='./data'):
        self.ds = load_dataset(self.huggingface)
        self.local_dir= local_dir
        os.makedirs(local_dir, exist_ok=True)

        zip_path = os.path.join(local_dir, 'imgs.zip')
        extract_folder = os.path.join(local_dir, 'imgs')
        if not Path(zip_path).exists():
            print("Downloading the file...")
            response = requests.get(self.download_link, stream=True)
            with open(zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print("Download complete.")

        # Unzip the file
        if not Path(extract_folder).exists():
            print("Extracting files...")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_folder)
            print("Extraction complete.")

    def convert(self, jsonfile, subset):
        dataset = []
        for data in self.ds[subset]:
            tmp = FormatedData()
            tmp.user(data['question'], os.path.join(self.local_dir, 'imgs/imgs', data['img_name']))
            tmp.ai(data['answer'])
            dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    SLAKE('./testdata').convert(f'./train_{name}', 'train')
    SLAKE('./testdata').convert(f'./test_{name}', 'test')
    SLAKE('./testdata').convert(f'./val_{name}', 'validation')