import json
import pandas as pd

with open('compiled_data.json', 'r') as file:
    data = json.load(file)

scraped_urls = {entry["URL_ID"] for entry in data}
all_urls = set([f"blackassign{str(i).zfill(4)}" for i in range(1, 101)])
missing_urls = all_urls - scraped_urls

print("Missing URLs:")
for url in sorted(missing_urls):
    print("\t" + url)