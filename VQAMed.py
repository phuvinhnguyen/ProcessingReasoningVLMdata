import json
from data import *
import requests
import zipfile
import os
from pathlib import Path

class VQAMed:
    download_links = ['https://zenodo.org/records/10499039/files/ImageClef-2019-VQA-Med-Training.zip?download=1',
                      'https://zenodo.org/records/10499039/files/ImageClef-2019-VQA-Med-Validation.zip?download=1',
                      'https://zenodo.org/records/10499039/files/VQAMed2019Test.zip?download=1']

    def __init__(self, local_dir='./data'):
        self.local_dir = os.path.join(local_dir, 'VQAMed')
        os.makedirs(self.local_dir, exist_ok=True)

        for i, name in zip(self.download_links, ['train', 'val', 'test']):
            zip_path = os.path.join(self.local_dir, f'{name}.zip')
            extract_folder = os.path.join(self.local_dir, f'{name}')
            if not Path(zip_path).exists():
                response = requests.get(i, stream=True)
                with open(zip_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        file.write(chunk)

            # Unzip the file
            if not Path(extract_folder).exists():
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_folder)

            if name == 'test':
                zip_path = os.path.join(self.local_dir, 'test/VQAMed2019Test/VQAMed2019_Test_Images.zip')
                extract_folder = os.path.join(self.local_dir, 'test/VQAMed2019Test/VQAMed2019_Test_Images')
                
                if not Path(extract_folder).exists():
                    with zipfile.ZipFile(zip_path, "r") as zip_ref:
                        zip_ref.extractall(extract_folder)

    def convert(self, jsonfile, subset):
        dataset = []
        files = {
            'test': (os.path.join(self.local_dir, 'test/VQAMed2019Test/VQAMed2019_Test_Questions_w_Ref_Answers.txt'),
                     os.path.join(self.local_dir, 'test/VQAMed2019Test/VQAMed2019_Test_Images/VQAMed2019_Test_Images')),
            'val': (os.path.join(self.local_dir, 'val/ImageClef-2019-VQA-Med-Validation/All_QA_Pairs_val.txt'),
                    os.path.join(self.local_dir, 'val/ImageClef-2019-VQA-Med-Validation/Val_images')),
            'train': (os.path.join(self.local_dir, 'testdata/VQAMed/train/ImageClef-2019-VQA-Med-Training/All_QA_Pairs_train.txt'),
                    os.path.join(self.local_dir, 'train/ImageClef-2019-VQA-Med-Training/Train_images'))
        }

        with open(files[subset][0]) as wf:
            contents = wf.readlines()

        for line in contents:
            data = line.strip().split('|')
            tmp = FormatedData()
            tmp.user(data[1], os.path.join(files[subset][1], f"{data[0]}.jpg"))
            tmp.ai(data[2])
            dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    VQAMed('./testdata').convert(f'./train_{name}', 'train')
    VQAMed('./testdata').convert(f'./test_{name}', 'test')
    VQAMed('./testdata').convert(f'./val_{name}', 'val')