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

def FindReleases(comp, check_repo=repo) -> list[GitRelease.GitRelease]:
    releases = check_repo.get_releases()

    matched_releases = [release for release in releases if release.tag_name.find(comp) != -1]

    if matched_releases:
        return matched_releases
    return []

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
    file.close()
    print("\r下载完成")

def FetchDDNet():
    try:
        url = "https://update.ddnet.org/update.json"
        update = requests.get(url, allow_redirects=True)
        update_json = json.loads(update.content) #获取版本号
        
        Version = str(update_json[0]["version"])
        if FindRelease(f"ddnet-{Version}") == None:
            FileName = f"cache/DDNet/DDNet-{Version}.apk"
            print(f"正在拉取DDNet-Android-{Version}")
            CreateDirIfNotExists("cache/DDNet")
            FastDownloadFile(f"https://ddnet.org/downloads/DDNet-{Version}.apk", FileName)
            release = repo.create_git_release(f"ddnet-{Version}", f"DDNet-{Version}", "自动上传")
            release.upload_asset(FileName)

        print("DDNet已更新到最新!")
    except:
        print("拉取DDNet部分失败!")

def BuildWeb():
    CreateDirIfNotExists("web-build")
    file = open("web-build/index.html", "w")
    def writebuffer(line):
        print(line, file=file)

    writebuffer("<!DOCTYPE html>")
    writebuffer("<html>")
    writebuffer("<head>")
    writebuffer("<meta charset=\"utf-8\">")
    writebuffer("<link rel=\"shortcut icon\" href=\"https://avatars.githubusercontent.com/u/101462745?s=32\">")
    writebuffer("<title>Teeworlds资源站</title>")
    writebuffer("</head>")
    writebuffer("<body>")
    writebuffer("<p>本项目由Mid·Night组织提供!</p>")

    writebuffer("<details>")
    writebuffer("<summary><h3>DDNet(Andorid)下载</h3></summary>")

    for i in FindReleases("ddnet"):
        writebuffer(f"##{i.title}")
        writebuffer("<p><a href=\"https://github.com/TeeMidnight/teeworlds-data/releases/download/{}/{}.apk\">github源链(能使用这个就用这个)</a></p>".format(i.tag_name, i.title))
        writebuffer("\n")
        writebuffer("<p><a href=\"https://github.moeyy.xyz/https://github.com/TeeMidnight/teeworlds-data/releases/download/{}/{}.apk\">github镜像站链</a></p>".format(i.tag_name, i.title))

    writebuffer("</details>")

    writebuffer("<details>")
    writebuffer("<summary><h3>TaterClient(Windows)下载(给予源github链接)</h3></summary>")

    for i in FindReleases("V", github.get_repo("sjrc6/TaterClient-ddnet")):
        writebuffer(f"##TaterClient{i.title}")
        writebuffer("<p><a href=\"https://github.com/sjrc6/TaterClient-ddnet/releases/download/{}/DDNet.exe\">github源链(能使用这个就用这个)</a></p>".format(i.tag_name))
        writebuffer("\n")
        writebuffer("<p><a href=\"https://github.moeyy.xyz/https://github.com/sjrc6/TaterClient-ddnet/releases/download/{}/DDNet.exe\">github镜像站链</a></p>".format(i.tag_name))
    writebuffer("</details>")
    writebuffer("</body>")
    writebuffer("</html>")

    file.close()

def main():
    CreateDirIfNotExists("cache")
    FetchDDNet()
    BuildWeb()

if __name__ == "__main__":
    sys.exit(main())