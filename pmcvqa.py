import json
from data import *
from datasets import load_dataset
import requests
import zipfile
import os
from pathlib import Path

class PMCVQA:
    download_link1 = 'https://huggingface.co/datasets/xmcmic/PMC-VQA/resolve/main/images.zip'
    # download_link2 = 'https://huggingface.co/datasets/xmcmic/PMC-VQA/resolve/main/images_2.zip'
    huggingface = 'xmcmic/PMC-VQA'

    def __init__(self, local_dir='./data'):
        self.ds = load_dataset(self.huggingface, revision='a44ac85fe26f9abb976dab4268d86e7f77fe7ecc')
        self.local_dir = os.path.join(local_dir, 'PMCVQA')
        os.makedirs(local_dir, exist_ok=True)

        zip_path1 = os.path.join(local_dir, 'imgs1.zip')
        zip_path2 = os.path.join(local_dir, 'imgs2.zip')
        extract_folder = os.path.join(local_dir, 'imgs')
        if not Path(zip_path1).exists():
            response = requests.get(self.download_link1, stream=True)
            with open(zip_path1, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
        if not Path(zip_path2).exists():
            response = requests.get(self.download_link1, stream=True)
            with open(zip_path2, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

        # Unzip the file
        if not Path(extract_folder).exists():
            with zipfile.ZipFile(zip_path1, "r") as zip_ref:
                zip_ref.extractall(extract_folder)
        if not Path(extract_folder).exists():
            with zipfile.ZipFile(zip_path2, "r") as zip_ref:
                zip_ref.extractall(extract_folder)

    def convert(self, jsonfile, subset):
        dataset = []
        for data in self.ds[subset]:
            tmp = FormatedData()
            tmp.user(data['Question'], os.path.join(self.local_dir, 'figures', data['Figure_path']))
            tmp.ai(data['Answer'])
            dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    PMCVQA('./testdata').convert(f'./train_{name}', 'train')
    PMCVQA('./testdata').convert(f'./test_{name}', 'test')