import json
from .data import *
import json
import os

class CLEFMed:
    '''Remember to download dataset from drive (link is in the github page), unzip it and parse name of unzip folder to this class, test set of this data does not contain labels'''

    def __init__(self, local_dir='ImageCLEFmed-MEDVQA-GI-2023-Development-Dataset'):
        self.local_dir = local_dir

    def convert(self, jsonfile, subset):
        dataset = []
        with open(os.join(self.local_dir, 'gt.json')) as wf:
            contents = json.load(wf)

        for item in contents:
            for label in item['Labels']:    
                tmp = FormatedData()
                tmp.user(label['Question'], os.path.join(self.local_dir, 'images', f"{item['ImageID']}.jpg"))
                tmp.ai(','.join(label['Answer']))
                dataset.append(tmp.data)
        
        with open(jsonfile, "w") as f:
            json.dump(dataset, f, indent=4)

if __name__ == '__main__':
    name = os.path.basename(__file__) + '.json'
    CLEFMed('ImageCLEFmed-MEDVQA-GI-2023-Development-Dataset').convert(f'./{name}', 'test')