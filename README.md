- [v] https://huggingface.co/datasets/flaviagiammarino/path-vqa
- [v] https://github.com/simula/ImageCLEFmed-MEDVQA-GI-2023 - about 400MD after zip
- [v] https://figshare.com/s/3e8ad50db900e82d3b47
- [v] https://github.com/xiaoman-zhang/PMC-VQA?tab=readme-ov-file - 20GB after zip
- [v] https://zenodo.org/records/10499039
- [v] flaviagiammarino/vqa-rad
- [v] BoKelvin/SLAKE


## GET DATA
```bash
cd ReasoningVLMdata
chmod +x run.sh
./run_all.sh ./
```

## OUTPUT FORMAT

```json
[
    {
        "messages": [
            {
                "role": "user",
                "content": "<image> Answer in natural language. What diseases are included in the picture?"
            },
            {
                "role": "assistant",
                "content": "Lung Cancer"
            }
        ],
        "images": [
            "Abnormal_Ours/test/imgs_test_abnormal/xmlab102.jpg"
        ]
    },
    {
        "messages": [
            {
                "role": "user",
                "content": "<image> Answer in natural language. Is the lung healthy?"
            },
            {
                "role": "assistant",
                "content": "No"
            }
        ],
        "images": [
            "Abnormal_Ours/test/imgs_test_abnormal/xmlab102_1.jpg"
        ]
    },
    {
```