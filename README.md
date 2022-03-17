# bilispider 1.0

爬取bilibili的小脚本

- 工具可以指定下载的媒体的种类，可以指定下载音频和视频

# 用法

```python
pip install -r requirements.txt
Usage: python bilispider.py -u <Target URL> -f <file_type>
Options:
  -h, --help    show this help message and exit
  -u URL        target url for download
  -f FILE_TYPE  MV or AU or ALL
```



### 注意：本工具需要借用ffmpeg进行视频的合成，请再使用之前安装好ffmpeg并配置好环境变量。

![image-20220317193955501](https://gitee.com/snikers/picgos/raw/master/202203171939809.png)
