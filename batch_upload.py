
import argparse
import os
import requests

parser = argparse.ArgumentParser(description='批量上传')
parser.add_argument('-i', type=str, help='用户ID')
parser.add_argument('-d', type=str, help='视频文件夹')
args = parser.parse_args()

# 服务器端处理上传的 URL，需根据实际情况修改
upload_url = 'http://127.0.0.1:5002/upload'

# 固定的用户 ID，需根据实际情况修改
user_id = args.i

# 要上传的文件夹路径，需根据实际情况修改
folder_path = args.d

# 遍历文件夹中的所有文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.mp4'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as video_file:
                    # 构建表单数据
                    data = {
                        'user_id': user_id
                    }
                    files = {
                        'video': video_file
                    }
                    # 发送 POST 请求进行文件上传
                    response = requests.post(upload_url, data=data, files=files)
                    if response.status_code == 200:
                        print(f'{file} 上传成功')
                    else:
                        print(f'{file} 上传失败，状态码: {response.status_code}')
            except Exception as e:
                print(f'{file} 上传时出现错误: {e}')
    