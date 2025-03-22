class FormatedData:
    def __init__(self):
        self.data = {
            'messages': [],
            'images': []
        }
    def user(self, content, image_path):
        self.data['messages'].append({
                "role": "user",
                "content": f"<image> {content}"
            })
        self.data['images'].append(image_path)
    def ai(self, content):
        self.data['messages'].append({
            "role": "assistant",
            "content": content
        })
        