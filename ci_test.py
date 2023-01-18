import requests
import hashlib


TESTING_URL = 'http://localhost:9889/'


class TestFailedException(Exception):

	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def test_response_code(res: requests.Response):
	if res.status_code != 200:
		raise TestFailedException(message='Hashsums are different, test failed.')


def check_hash_sum(res: requests.Response):
	with open('index.html') as f:
		i_hash = hashlib.md5(f.read()).hexdigest()
	o_hash = hashlib.md5(res.content).hexdigest()
	if i_hash != o_hash:
		raise TestFailedException(message='Hashsums are different, test failed.')


def send_telegram_message(message):
	pass


if __name__ == '__main__':
	r = requests.get(TESTING_URL)

	try:
		test_response_code(r)
		check_hash_sum(r)

	except TestFailedException as e:
		print(e.message)
		send_telegram_message(e.message)
