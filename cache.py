import requests, json, sys, os

new_files = []
def CreateDirIfNotExists(dirpath):
    if os.path.exists(dirpath) == False:
        os.mkdir(dirpath)

def FastDownloadFile(url, save_path):
    response = requests.get(url, allow_redirects=True, stream=True)
    size = response.headers.get("content-length")

    file = open(save_path, "wb")
    count = 1
    for i in response.iter_content(chunk_size=1024):
        file.write(i)
        print(f"下载中..{round(count * 1024 / float(size) * 100, 2)}%", end="\r")
        count += 1
    print(f"下载完成", end="\r")
    new_files.append(save_path)

def FetchDDNet():
    try:
        url = "https://update.ddnet.org/update.json"
        update = requests.get(url, allow_redirects=True)
        update_json = json.loads(update.content) #获取版本号
        
        Version = str(update_json[0]["version"])
        FileCheckName = f"cache/DDNet/DDNet-{Version}.apk"
        if os.path.exists(FileCheckName) == False:
            print(f"正在拉取DDNet-Android-{Version}")
            CreateDirIfNotExists("cache/DDNet")
            FastDownloadFile(f"https://ddnet.org/downloads/DDNet-{Version}.apk", FileCheckName)

        print("DDNet已更新到最新!")
    except:
        print("拉取DDNet部分失败!")

def FetchTaterClient():
    try:
        url = "https://api.github.com/repos/sjrc6/TaterClient-ddnet/releases/latest"
        update = requests.get(url, allow_redirects=True)
        update_json = json.loads(update.content) #获取版本号
        
        TagName = str(update_json["tag_name"]);
        Version = str(update_json["name"])
        FileCheckName = f"cache/TaterClient/TaterClient-{Version}.zip"
        if os.path.exists(FileCheckName) == False:
            print(f"正在拉取TaterClient-{Version}")
            CreateDirIfNotExists("cache/TaterClient")
            FastDownloadFile(f"https://github.com/sjrc6/TaterClient-ddnet/releases/download/{TagName}/TClient-windows.zip", f"cache/TaterClient/TaterClient-{Version}.zip")

        print("TaterClient已更新到最新!")
    except:
        print("拉取TaterClient部分失败!")

def main():
    CreateDirIfNotExists("cache")
    FetchDDNet()
    FetchTaterClient()

if __name__ == "__main__":
    sys.exit(main())