import requests
import json
import sys


def main():
	if len(sys.argv) > 1:
		fname = sys.argv[1]
	else:
		fname = "test.jl"


	with open(fname, 'r') as f:
		for i, l in enumerate(f.readlines()):
			url = "http://jmpe.me:8080/api/docs"
			headers = {'Content-type': 'application/json'}
			response = requests.post(url, headers=headers, data = l)
			print i, response.json()


if __name__ == '__main__':
	main()