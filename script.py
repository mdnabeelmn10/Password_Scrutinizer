import requests
import hashlib
import sys

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query 
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fetching: {res.status_code}, Check api for errors')
    
    return res

def leak_count(response,hash_to_check):
    passwords = response.text.split('\n')
    passwords = [pwd.strip('\r') for pwd in passwords]
    hashes = {pwd.split(':')[0]:pwd.split(':')[1] for pwd in passwords}
    for h in hashes:
        if h==hash_to_check:
            return hashes[h]
    # print(passwords[0:5])
    return 0


def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_chars,tail = sha1_password[:5],sha1_password[5:]
    response = request_api_data(first5_chars)
    # print(response.text)
    # print(first5_chars,tail)
    return leak_count(response,tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if(count):
            print(f'The {password} was found {count} times. Better change it.')
        else:
            print(f"The {password} was not found. You are good to go!")
if __name__ == "__main__":
    main(sys.argv[1:])