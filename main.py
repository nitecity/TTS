import requests
import time
import random
import sys
import os
from playsound import playsound
from colorama import Fore, Style
from dotenv import load_dotenv
from ids import ids

RED = Fore.RED
GREEN = Fore.GREEN
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
LIGHTGREEN = Fore.LIGHTBLACK_EX
LIGHTRED = Fore.LIGHTRED_EX
LIGHTMAGENTA = Fore.LIGHTMAGENTA_EX
LIGHTBLUE = Fore.LIGHTBLUE_EX
RESET = Style.RESET_ALL

try:
    if not os.path.exists('.env'):
        key = input("API KEY:\n> ")
        with open('.env', 'w') as f:
            f.write(f'API_KEY="{key}"\n')
except:
    print(f'{RED}Operation Canceled{RESET}')
    sys.exit(1)

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print(f'{RED}API_KEY not defined! Please assign your API_KEY manualy in ".env" file.\ne.g, API_KEY="sk_8ea11ed75345e8b59fbba36c9c33d1d8fbe82654a3164698"{RESET}')
    sys.exit(1)
ids_path: str = "ids.py"
mp3_path: str = f"results/{int(time.time() * 1000)}.mp3"

headers: dict = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": API_KEY
}

data: dict = {
  "text": "",
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

########################### Text To Speech ###########################
def generate_speech_and_play(url: str) -> None:
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"{LIGHTGREEN}done!{RESET}")
            with open(mp3_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            playsound(mp3_path)
        else:
            print(f"{LIGHTRED}Something went wrong. See the message below:{RESET}")
            print(f"{LIGHTRED}{response.text}{RESET}")
    except requests.exceptions.HTTPError as e:
        print(f'{RED}Http error: {e}{RESET}')
    except Exception as e:
        print(f'{RED}An unexpected error occurred: {e}{RESET}')

############################## Add Voice ##############################
def add_new_id(new_name: str, new_id: str) -> None:
    with open(ids_path , 'r') as r:
        lines = r.readlines()

    with open(ids_path , 'w') as f:
        lines[-1] = f'\t"{new_name}": "{new_id}",\n' + '}'
        f.writelines(lines)
    print(f"{GREEN}Succussfuly added new voice{RESET}")

########################## Validate Voice Id ###########################
def validate_new_id(url) -> bool:
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.HTTPError as e:
        print(f'{RED}Http error: {e}{RESET}')
    except Exception as e:
        print(f'{RED}An unexpected error occurred: {e}{RESET}')

################################ Main #################################
def main() -> None:
    url: str = "https://api.elevenlabs.io/v1/text-to-speech/"
    names: list[str] = []
    for name in ids:
        names.append(name)
    print(f"{LIGHTMAGENTA}Characters: {LIGHTBLUE}{names}{RESET}")
    print(f"{YELLOW}How To Use:{RESET}")
    try:
        user_input = input(
            f"{CYAN}- Text only: e.g., > {GREEN}Hello World!{RESET}\n"
            f"{CYAN}- Character & Text: e.g., > {GREEN}sarah ;; Hello World!{RESET}\n"
            f"{CYAN}- Add a new voice: e.g., > {GREEN}add ;; ethan ;; g5CIjZEefAph4nQFvHAz{RESET}\n"
            f"{LIGHTMAGENTA}- Find voice IDs here: https://elevenlabs.io/app/voice-lab{RESET}\n> "
        )
    except:
        print(f'{Fore.RED}Operation Canceled!{Style.RESET_ALL}')
        return

    parts: list = user_input.split(';;')

    if len(parts) == 1 and parts[0]:
        data['text'] = parts[0]
        random_voice = random.choice(list(ids.keys()))
        url = url + ids[random_voice]
        print(f'{Fore.YELLOW}"{random_voice}" is going to speak...{Style.RESET_ALL}')
        generate_speech_and_play(url)

    elif len(parts) == 2:
        character = parts[0].lower().strip()
        text = parts[1].strip()
        if character in ids and text:
            url = url + ids[character]
            data['text'] = text
            generate_speech_and_play(url)
        else:
            print(f"{Fore.RED}The name \"{character}\" is not in the library or Text is empty{Style.RESET_ALL}")

    elif len(parts) == 3:
        keyword, new_name, new_id = parts[0].lower().strip(), parts[1].lower().strip(), parts[2].strip()
        if keyword == 'add' and new_name:
            for id in ids.values():
                if id == new_id:
                    print(f"{Fore.YELLOW}The ID is already in the library!{Style.RESET_ALL}")
                    return
            if validate_new_id(url+new_id):
                add_new_id(new_name , new_id)
            else:
                print(f"{Fore.LIGHTRED_EX}The provided voice ID is invalid.{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTRED_EX}Invalid input format.{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
