import json
import requests
import zipfile
import os
from pathlib import Path
import csv
from ReasoningVLMdata.data import *

class OphthalVQA:
    download_labels = 'https://figshare.com/ndownloader/files/45711882?private_link=3e8ad50db900e82d3b47'
    download_images = 'https://figshare.com/ndownloader/articles/25624917?folder_path=images&private_link=3e8ad50db900e82d3b47'

    def __init__(self, local_dir='./data'):
        self.local_dir= os.path.join(local_dir, 'OphthalVQA')
        os.makedirs(local_dir, exist_ok=True)

        zip_path = os.path.join(local_dir, 'imgs.zip')
        if not Path(zip_path).exists():
            response = requests.get(self.download_images, stream=True)
            with open(zip_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

        label_path = os.path.join(local_dir, 'label.csv')
        if not Path(label_path).exists():
            response = requests.get(self.download_labels, stream=True)
            with open(label_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

        with open(label_path, mode ='r') as file:
            self.csv_content = [i for i in csv.reader(file)]

        # Unzip the file
        if not Path(self.local_dir).exists():
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(self.local_dir)

    def convert(self, jsonfile, subset):
        dataset = []
        for i in self.csv_content[1:]:
            if i[6] is None or float(i[6]) < 2: continue
            tmp = FormatedData()
            tmp.user(i[3], os.path.join(self.local_dir, 'images', f'{i[2]}.jpg'))
            tmp.ai(i[4])
            dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    OphthalVQA('./testdata').convert(f'./{name}', 'test')
