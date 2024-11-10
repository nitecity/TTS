import requests
import uuid
import random
from playsound import playsound
from colorama import Fore, Style
from ids import ids

token: str = "YOUR_TOKEN"
path: str ="ids.py"
mp3: str = f"{uuid.uuid4()}.mp3"

headers: dict = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": token
}

data: dict = {
  "text": "",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

def post(url: str, data: dict, headers: dict) -> None:

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"{Fore.LIGHTGREEN_EX}done!{Style.RESET_ALL}")
        with open(mp3, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        playsound(mp3)

    else:
        print(f"{Fore.LIGHTRED_EX}Something went wrong. See the message below:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTYELLOW_EX}{response.text}{Style.RESET_ALL}")

def add(new_name: str, new_id: str) -> None:
    with open(path , 'r') as r:
        lines = r.readlines()

    with open(path , 'w') as w:
        lines[-1] = f'\t"{new_name}": "{new_id}",\n' + '}'
        w.writelines(lines)
    print("Succussfuly added the new ID")

def main() -> None:
    url: str = "https://api.elevenlabs.io/v1/text-to-speech/"
    names: list[str] = []
    for name in ids:
        names.append(name)
    print(f"{Fore.LIGHTMAGENTA_EX}Characters: {Fore.LIGHTBLUE_EX}{names}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}How To Use:{Style.RESET_ALL}")
    user_input: str = input(f"{Fore.CYAN}- Just enter some TEXT: e.g, > {Fore.GREEN}Hello World!{Style.RESET_ALL}\n{Fore.CYAN}- Pick one of the names above, two semicolons \";;\" then the TEXT: e.g, > {Fore.GREEN}sarah ;; Hello World!{Style.RESET_ALL}\n{Fore.CYAN}- If you'd like to add more Voices: e.g, > {Fore.GREEN}add ;; ethan ;; g5CIjZEefAph4nQFvHAz{Style.RESET_ALL}\n{Fore.LIGHTMAGENTA_EX}- Ids: https://elevenlabs.io/app/voice-lab{Style.RESET_ALL}\n> ")

    sp: list = user_input.split(';;')

    if len(sp) == 1 and sp[0] != '':
        data['text'] = sp[0]
        random_name = random.choice(list(ids.keys()))
        url = url + ids[random_name]
        print(f'{Fore.YELLOW}"{random_name}" is going to speak...{Style.RESET_ALL}')
        post(url, data, headers)

    elif len(sp) == 2:
        first_value = sp[0].lower().strip()
        second_value = sp[1].strip()
        if first_value in ids:
            url = url + ids[first_value]
            data['text'] = second_value
            post(url, data, headers)
        else:
            print(f"{Fore.YELLOW}The name \"{first_value}\" is not in the library!\nI'm going to use a random name...{Style.RESET_ALL}")
            random_name = random.choice(list(ids.keys()))
            url = url + ids[random_name]
            print(f'{Fore.YELLOW}"{random_name}" is going to speak...{Style.RESET_ALL}')
            data['text'] = second_value
            post(url, data, headers)

    elif len(sp) == 3:
        first_value = sp[0].lower().strip()
        if first_value == 'add':
            for id in ids.values():
                if id == sp[2].strip():
                    print(f"{Fore.YELLOW}The ID is already in the library!{Style.RESET_ALL}")
                    return
            url = url + sp[2].strip()
            response = requests.post(url, json=data, headers=headers)
            if response.status_code != 400:
                add(sp[1].lower().strip() , sp[2].strip())
            else:
                print(f"{Fore.LIGHTRED_EX}Wrong Id!{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTRED_EX}Syntax Error!{Style.RESET_ALL}")

main()
