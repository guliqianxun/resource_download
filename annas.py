import requests
import os
import json

# 读取生成的文件
with open('generate_torrents.json', 'r') as file:
    data = json.load(file)

# 按group_name分类
group_stats = {}
for item in data:
    group_name = item['group_name']
    if group_name not in group_stats:
        group_stats[group_name] = {
            'total_torrents': 0,
            'total_data_size': 0,
            'total_completed': 0
        }
    group_stats[group_name]['total_torrents'] += 1
    group_stats[group_name]['total_data_size'] += item['data_size']
    group_stats[group_name]['total_completed'] += item['completed']

# 打印结果
for group_name, stats in group_stats.items():
    print(f"Group: {group_name}")
    print(f"  Total Torrents: {stats['total_torrents']}")
    print(f"  Total Data Size: {stats['total_data_size'] / (1024 ** 4):.2f} TB")  # 转换为TB
    print(f"  Total Completed: {stats['total_completed']}")
    print()

zlib_entries = [entry for entry in data if entry['group_name'] == 'zlib']

# 下载目录
download_dir = "zlib_torrents"
os.makedirs(download_dir, exist_ok=True)

# 下载种子文件
def download_torrent(url, display_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(download_dir, display_name), 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {display_name}")
    else:
        print(f"Failed to download: {display_name}")

# 下载所有zlib组的种子文件
count  = 1
for entry in zlib_entries:
    print(f'processing {count} / {len(zlib_entries)}')
    torrent_url = entry['url']
    display_name = entry['display_name']
    download_torrent(torrent_url, display_name)
    
    count = count + 1

print("All torrents downloaded.")
