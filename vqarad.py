import json
from datasets import load_dataset
import os
from data import *

class VQARAD:
    huggingface = 'flaviagiammarino/vqa-rad'

    def __init__(self, local_dir='./data'):
        self.ds = load_dataset(self.huggingface)
        self.local_dir= os.path.join(local_dir, 'vqarad')
        os.makedirs(self.local_dir, exist_ok=True)

    def convert(self, jsonfile, subset):
        dataset = []
        for i, data in enumerate(self.ds[subset]):
            fpath = os.path.join(self.local_dir, f"{i}.jpg")
            data['image'].save(fpath, format='JPEG')
            tmp = FormatedData()
            tmp.user(data['question'], fpath)
            tmp.ai(data['answer'])
            dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    VQARAD('./testdata').convert(f'./train_{name}', 'train')
    VQARAD('./testdata').convert(f'./test_{name}', 'test')