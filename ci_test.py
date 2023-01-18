import requests
import hashlib
import sys


TESTING_URL = 'http://xxxx/'
TG_BOT_TOKEN = 'xxxx'  # tg bot token
CHAT_ID = 3333  # tg chat id
INDEX_FILE_PATH = '/tmp/cicd/sf_project_11/index.html'


class TestFailedException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def test_response_code(res: requests.Response):
    print('status_code', res.status_code)
    if res.status_code != 200:
        raise TestFailedException(message='Return code is wrong, test failed.')


def check_hash_sum(res: requests.Response):
    with open(INDEX_FILE_PATH, 'rb') as f:
        file_content = f.read()
        i_hash = hashlib.md5(file_content).hexdigest()
    o_hash = hashlib.md5(res.content).hexdigest()
    print('i_hash', file_content, i_hash)
    print('o_hash', res.content, o_hash)
    if i_hash != o_hash:
        raise TestFailedException(message='Hashsums are different, test failed.')


def send_telegram_message(message):
    requests.get('https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'.format(TG_BOT_TOKEN, CHAT_ID, message))


if __name__ == '__main__':

    print('Hello world! Testing...')

    try:
        r = requests.get(TESTING_URL)
        test_response_code(r)
        check_hash_sum(r)

    except requests.RequestException as e:
        print(str(e))
        sys.exit(-1)

    except TestFailedException as e:
        print(e.message)
        send_telegram_message(e.message)
        sys.exit(-1)

    print('Testing done!')
