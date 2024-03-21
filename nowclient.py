#python3 ./nowclient.py
import requests

def login(url):
    """用户登录"""
    username = input("请输入用户名: ")
    password = input("请输入密码: ")
    response = requests.post(url, json={"username": username, "password": password})
    return response

def logout(url):
    """用户登出"""
    response = requests.get(url)
    return response

def upload_file(url, file_path, cookies):
    """上传文件并打印服务器响应"""
    files = {'document': open(file_path, 'rb')}
    response = requests.post(url, files=files, cookies=cookies)
    return response

if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    login_url = f"{base_url}/login"
    
    login_response = login(login_url)
    
    if login_response.status_code == 200:
        print("登录成功")
        cookies = login_response.cookies
        
        file_path = input("请输入要上传文件的路径: ")
        upload_response = upload_file(f"{base_url}/upload", file_path, cookies)
        
        if upload_response.status_code == 200:
            print("文件上传成功，以下是分析结果:")
            print(upload_response.json())
        else:
            print("文件上传失败，状态码:", upload_response.status_code)
        
        logout_response = logout(f"{base_url}/logout")
        
        if logout_response.status_code == 200:
            print("登出成功")
    else:
        print("登录失败，状态码:", login_response.status_code)
