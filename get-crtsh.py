# A script to scrape crt.sh
# Coded by - Nehal Zaman (@pwnersec)

import sys
import requests
from termcolor import colored
from bs4 import BeautifulSoup
from banner import banner


URL = "https://crt.sh"


def parse_domain(domain):

	if domain.startswith("http://"):
		domain = domain.replace(domain[0:7], "")

	if domain.startswith("https://"):
		domain = domain.replace(domain[0:8], "")

	if domain.endswith("/"):
		domain = domain.replace(domain[-1], "")

	return domain


def make_http_request(domain):

	data = {
		"q": domain
	}

	return requests.get(URL, params=data)


def get_crtsh_data(domain):

	raw_data = make_http_request(domain)

	raw_results = BeautifulSoup(raw_data.content, "html5lib").find_all("td", attrs={'style': None})[2:]
	
	results = []

	for raw_result in raw_results:

		if (len(raw_result.find_all()) == 0):

			results.append(raw_result)

	unique_data = []

	for result in results:
	
		if (result.get_text() not in unique_data) and (not result.get_text().startswith("*")):

			unique_data.append(result.get_text())

	return unique_data


if __name__ == "__main__":

	if len(sys.argv) != 2:
		print(colored(f"USAGE: {sys.argv[0]} <domain>", "red"))
		sys.exit(1)

	print(colored(banner, "yellow"))

	domain = parse_domain(sys.argv[1])
	
	crtsh_data = get_crtsh_data(domain)

	for data in crtsh_data:

		print(colored(data, "green"))