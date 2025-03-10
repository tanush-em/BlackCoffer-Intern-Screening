import json

with open('compiled_data.json', 'r') as json_file:
    data = json.load(json_file)

for entry in data:
    URL_ID = entry['URL_ID']
    article_content = entry['article_content']
    
    with open(f"data/{URL_ID}.txt", 'w') as text_file:  
        text_file.write(article_content)  