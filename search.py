import os
import requests
import subprocess
def search_books(keyword, page=1, sensitive=False):
    url = "https://api.ylibrary.org/api/search/"
    headers = {}
    payload = {
        'keyword': keyword,
        'page': page,
        'sensitive': sensitive,
    }
    response = requests.post(url, headers=headers, json=payload)
    print('search name success')
    return response.json()

def get_book_details(book_id, source='zlibrary'):
    url = "https://api.ylibrary.org/api/detail/"
    headers = {}
    payload = {
        'id': book_id,
        'source': source,
    }
    response = requests.post(url, headers=headers, json=payload)
    print('search book success')
    return response.json()

def download_book(ipfs_cid, save_path):
    try:
        subprocess.run(['ipfs', 'get', ipfs_cid, '-o', save_path], check=True)
        print(f"Downloaded successfully to {save_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {save_path}: {e}")

# 示例流程
books = search_books('三体')
book_id = books['data'][0]['id']
book_details = get_book_details(book_id)
book_name = f"{book_details['title']}.{book_details['extension']}"
save_path = os.path.join('/books', book_name)
download_book(book_details['ipfs_cid'], save_path)
