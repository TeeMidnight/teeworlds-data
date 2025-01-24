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

    matched_releases = [release for release in releases if release.tag_name.find(tag_name) != -1]

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
    except Exception as e:
        print("拉取DDNet部分失败!")
        print(repr(e))

def BuildWeb():
    CreateDirIfNotExists("web-build")

    file = open("example_html", "r")
    buffer = file.read()

    # generate json
    json_dump = [{"name" : "DDraceNetwork (Android)", "items": []}, 
                {"name": "TaterClient (Windows, Gores)", "items": []},
                {"name": "InfClass-Client (Windows, 感染模式)", "items": []}]
    for i in FindReleases("ddnet", repo):
        item = {"title": f"{i.title}", "source": f"https://github.com/TeeMidnight/teeworlds-data/releases/download/{i.tag_name}/{i.title}.apk"}
        json_dump[0]["items"].append(item)

    for i in FindReleases("V", github.get_repo("sjrc6/TaterClient-ddnet")):
        item = {"title": f"{i.title}", "source": f"https://github.com/sjrc6/TaterClient-ddnet/releases/download/{i.tag_name}/DDNet.exe"}
        json_dump[1]["items"].append(item)

    for i in FindReleases("v", github.get_repo("infclass/infclass-client")):
        # find file
        for file in i.get_assets():
            if(file.name.find("win64") != -1):
                item = {"title": f"{i.title}", "source": f"https://github.com/infclass/infclass-client/releases/download/{i.tag_name}/{file.name}"}
                json_dump[2]["items"].append(item)
                break

    buffer = buffer.format(json.dumps(json_dump, ensure_ascii=False))

    file = open("web-build/index.html", "w")
    file.write(buffer)
    file.close()
    file = open("web-build/CNAME", "w")
    file.write("data.teemidnight.online")
    file.close()

def main():
    CreateDirIfNotExists("cache")
    FetchDDNet()
    BuildWeb()

if __name__ == "__main__":
    sys.exit(main())