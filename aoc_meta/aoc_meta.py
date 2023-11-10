import requests
import os
import re
import time
import tqdm

cookies = {"session": "COOKIE NOM NOM NOM"}
url = lambda year, day : f"https://adventofcode.com/{str(year)}/day/{str(day)}"

year = 0
day = 0

def aoc_init(y, d):
    global year, day
    year = y
    day = d

def get_input():
    if os.path.isfile(f"{str(year)}_{str(day)}.txt"):
        with open(f"{str(year)}_{str(day)}.txt", "r") as file:
            return file.read().strip()
    request = requests.get(url(year, day) + "/input", cookies=cookies)
    with open(f"{str(year)}_{str(day)}.txt", "w") as file:
        file.write(request.text)
    return get_input()

def p1(answer):
    return submit(answer, 1)

def p2(answer):
    return submit(answer, 2)

def submit(answer, part):
    request = requests.post(
        url = url(year, day) + "/answer",
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'origin': 'https://adventofcode.com',
            'referer': url(year, day)
        },
        data={'level': part, 'answer': answer},
        cookies=cookies
    )
    print(["", "P1: ", "P2: "][part] + str(answer))
    print("Res: " + (res := parse_response(request.text)))

    if result := re.search(r"ERROR: Cooldown (\d+)m (\d+)s", res):
        m, s = int(result.group(1)), int(result.group(2))
        s = m * 60 + s
        print(f"Resubmitting in {s} seconds (ctrl + c) to cancel")
        for i in tqdm.tqdm(range(1, s + 1)):
            time.sleep(1)
        return submit(answer, part)
    
    print()
    return res

# Snatched from https://github.com/brtwrst/aoc-tools/blob/main/aoctools/plumbing.py#L4
def parse_response(raw):
    if not raw.startswith('<!DOCTYPE html>'):
        return 'ERROR: No HTML Received'
    re_main = re.compile(r'(?s)<main>\n<article><p>(.*)</p></article>\n</main>')
    main_part = re_main.search(raw)

    if not main_part:
        return 'ERROR: No main part in website'

    main_text = main_part.group(1)

    if main_text.startswith("That's the right answer"):
        return 'SUCCESS - Answer accepted'

    if main_text.startswith('You gave an answer too recently'):
        time = re.search(r'(?:(\d+)m )?(?:(\d+)s)', main_text)
        minutes, seconds = time.groups()
        return f'ERROR: Cooldown {minutes if minutes else 0}m {seconds}s'

    if main_text.startswith("That's not the right answer"):
        reason = re.search(r'your answer is too (\w*)', main_text)
        return 'WRONG ANSWER' + (f': - Too {reason.group(1)}' if reason else '')

    if main_text.startswith("You don't seem to be solving the right level"):
        return 'ALREADY SOLVED'

    return None