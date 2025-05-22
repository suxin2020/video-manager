# Video Manager

Video Manager是一个轻量级的本地视频浏览和管理工具，类似于抖音、tikitok，支持上传作品、查看用户作品、查看所有作品。

## 安装

```shell
conda activate video-manager
pip install -r requirements.txt
python app.py &
```

浏览器打开 [http://127.0.0.1:5002](http://127.0.0.1:5002)

## 浏览视频

[首页](http://127.0.0.1:5002)

- 包括上传作品、查看用户作品、查看所有作品子页面

[查看用户作品](http://127.0.0.1:5002/video)

- 显示用户ID列表和所选用户的视频作品

- 支持随机播放、顺序播放和循环播放

- 支持上下键切换视频播放

[查看所有作品](http://127.0.0.1:5002/videos_all)

- 显示所有用户的视频作品

- 支持随机播放、顺序播放和循环播放

- 支持上下键切换视频播放

## 上传视频

[上传作品](http://127.0.0.1/upload)

- 填写用户ID、本地视频文件或文件夹、封面图片进行上传

批量上传视频：

```shell
python ./batch_upload.py -i {user_id} -d {video_directory}
```

## 文件路径

- data/video.db - 数据库文件

- uploads/ - 上传文件夹
