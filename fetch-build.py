import requests, json, sys, os

from github import Github
from github import Auth
from github import GitRelease

token = str(os.environ.get("GITHUB_TOKEN"))
auth = Auth.Token(token)
github = Github(auth=auth)
repo = github.get_repo("TeeMidNight/teeworlds-data")
branch = repo.get_branch("main")

def FindRelease(tag_name) -> GitRelease.GitRelease | None:
    releases = repo.get_releases()

    matched_releases = [release for release in releases if release.tag_name == tag_name]

    if matched_releases:
        return matched_releases[0]
    return None

def ReleaseFile(tag_name, ):
    github.update_release()

def CreateDirIfNotExists(dirpath):
    if os.path.exists(dirpath) == False:
        os.mkdir(dirpath)

def FastDownloadFile(url, save_path):
    response = requests.get(url, allow_redirects=True, stream=True)
    size = response.headers.get("content-length")

    file = open(save_path, "wb")
    count = 1
    for i in response.iter_content(chunk_size=2048):
        file.write(i)
        if count != 1:
            print("\r", end="")
        print(f"下载中..{round(count * 2048 / float(size) * 100, 2)}%", end="")
        count += 1
    print("\r下载完成")

def FetchDDNet():
    try:
        url = "https://update.ddnet.org/update.json"
        update = requests.get(url, allow_redirects=True)
        update_json = json.loads(update.content) #获取版本号
        
        Version = str(update_json[0]["version"])
        if FindRelease(f"DDNet-{Version}") == None:
            FileName = f"cache/DDNet/DDNet-{Version}.apk"
            print(f"正在拉取DDNet-Android-{Version}")
            CreateDirIfNotExists("cache/DDNet")
            FastDownloadFile(f"https://ddnet.org/downloads/DDNet-{Version}.apk", FileName)
            release = repo.create_git_release(f"ddnet-{Version}", f"DDNet-{Version}", "自动上传")
            release.upload_asset(FileName)

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
    except:
        print("搜索TaterClient失败!")

def main():
    CreateDirIfNotExists("cache")
    FetchDDNet()
    FetchTaterClient()

if __name__ == "__main__":
    sys.exit(main())