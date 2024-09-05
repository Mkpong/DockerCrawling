import requests

def get_token(username, passwd):
    url = "https://hub.docker.com/v2/users/login/"

    payload = {
            "username": username,
            "password": passwd
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json().get('token')
        print("token : ", token)
        return token

    else:
        print(f"로그인 실패: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    username = input("Docker ID : ")
    passwd = input("Password : ")

    token = get_token(username, passwd)
