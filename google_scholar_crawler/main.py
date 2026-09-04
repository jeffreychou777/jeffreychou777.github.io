from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os
import time

def fetch_author(max_retries: int = 3, retry_delay_seconds: int = 30) -> dict:
    for attempt in range(1, max_retries + 1):
        try:
            author_data: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
            scholarly.fill(author_data, sections=['basics', 'indices', 'counts', 'publications'])
            return author_data
        except Exception as exc:
            if attempt == max_retries:
                raise
            print(
                f"Attempt {attempt}/{max_retries} failed to fetch Google Scholar data: {exc}. "
                f"Retrying in {retry_delay_seconds} seconds..."
            )
            time.sleep(retry_delay_seconds)

author: dict = fetch_author()
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
