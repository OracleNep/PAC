import json
import os
import requests

def get_latest_version_from_website(website_url):
    api_url = f"{website_url.rstrip('/')}/config.json"
    try:
        response = requests.get(api_url, verify=True, timeout=15) 
        if response.status_code == 200:
            data = response.json()
            latest_version = data.get('version', 'unknown')
            return latest_version
        else:
            print(f"无法获取最新版本: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"由于网络错误，无法获取最新版本")
        return None

def download_file_from_website(website_url, filename):
    download_url = f"{website_url.rstrip('/')}/{filename}"
    try:
        response = requests.get(download_url, verify=True, timeout=5)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"正在下载最新版本的配置文件 {filename}.")
        else:
            print(f"下载失败 {filename}: {response.status_code}")
    except requests.RequestException as e:
        print(f"由于网络错误 而无法下载 {filename}")

def check_and_update_config_json(website_url, filename):
    if not os.path.exists(filename):
        print(f"未找到 {filename}。下载中......")
        download_file_from_website(website_url, filename)
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            local_version = data.get('version', 'unknown')
            print(f"本地 {filename} 版本: {local_version}")
    except Exception as e:
        print(f"读取 {filename} 时出错")
        return

    latest_version = get_latest_version_from_website(website_url)
    if latest_version:
        if local_version != latest_version:
            print(f"将 {filename} 从版本 {local_version} 更新为 {latest_version}。")
            download_file_from_website(website_url, filename)
        else:
            print("该版本为最新版本")

def load_config_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def check_processes(user_input, data):
    antivirus_software = data.get('antivirus_software', [])
    result = ''
    for software in antivirus_software:
        processes = software.get('processes', [])
        url = software.get('url', '')
        software_name = software.get('name', '')

        for process in processes:
            if process.lower() in user_input.lower():
                result += f"{process} ==> {software_name}: {url}\n"

    if not result:
        result = "无匹配的进程，欢迎提交至\nhttps://github.com/OracleNep/PAC/"

    return result


def clear_form():
    global user_input, result
    user_input = ''
    result = ''

def main():
    website_url = "https://kn1g78.github.io/pac" 
    filename = "config.json"
    check_and_update_config_json(website_url, filename)

    global user_input, result
    data = load_config_json(filename)
    
    version_number = data.get('version', 'unknown')
    print("杀软识别-黄豆安全实验室")
    print("https://github.com/OracleNep/PAC/")
    print(f"项目版本号 {version_number}")
    print("\n请输入进程关键词")

    while True:
        user_input = input("> ")
        result = check_processes(user_input, data)

        print("\n")
        print(result)
        print("\n")
        clear_form()

if __name__ == "__main__":
    user_input = ""
    result = ""
    main()
