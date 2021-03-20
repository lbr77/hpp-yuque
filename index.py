from requests import *
from os import environ, walk, path, listdir
from hashlib import md5
from yaml import load, warnings
warnings({'YAMLLoadWarning': False})
yuquetoken = environ.get("YUQUE_TOKEN");
if yuquetoken == None:
    print("未定义yuque_token")
    exit(1)
# load Configurations
config = {};
with open("_config.yml", "r") as f:
    config = load(f.read())
    f.close();
print("配置读取成功")

def loadfiledir(root):
    fileq = []
    for root, dirs, files in walk(root):
        for file in files: 
            fileq.append(path.join(root,file))
    return fileq

def loadfiles():
    articles = [];
    n = 0
    for file in loadfiledir(config['postPath']):
        with open(file,"r",encoding = 'UTF-8',errors='ignore') as f:
            fileqwq=f.read()
            articles.append({
                "title": file.split('\\')[-1].split('.')[0],
                "data": fileqwq,
                "slug": md5(fileqwq.encode('utf8')).hexdigest()[0:5],
                "id": str(n)
            });
            f.close();
        n = n+1
    return articles

def uploadfiles(filename,file,slug):
    return post(config["baseurl"]+"/repos/"+config["login"]+"/"+config["repo"]+"/docs",data={
        "title": filename,
        "slug": slug,
        "public": 1,
        "format": "markdown",
        "body": file
    },headers = {
        "X-Auth-Token": yuquetoken,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4435.0 Safari/537.36 Edg/91.0.825.0"
    })

print("开始读取文件")

for i in loadfiles():
    # print()
    res = uploadfiles(i["title"],i["data"],i["slug"])
    if res.status_code == 200:
        print("上传文件"+i["title"]+"成功")
    else:
        print("错误:"+ str(res.json()))