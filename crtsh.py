from termcolor import colored
import requests
import json
import sys

if len(sys.argv) < 2:
    print(colored(f"USAGE: {sys.argv[0]} <domain> [output file]", "red"))
    sys.exit()

domain = sys.argv[1]
if len(sys.argv) == 3:
    output_file = sys.argv[2]
else:
    output_file = None

def parse(data):
    subdomains = set()
    for i in data:
        for name in i['name_value'].split("\n") + i['common_name'].split("\n"):
            if name != domain and not name.startswith("*"):
                subdomains.add(name)
    return list(subdomains)

def make_request(d):
    url = "https://crt.sh"
    params = {"q": d, "output": "json"}
    try:
        data = json.loads(requests.get(url, params=params).text)
    except:
        print(colored("Error in making request.", "red"))
        sys.exit()
    return data

def get_crtsh(d):
    data = make_request(d)
    return parse(data)

if __name__ == "__main__":
    banner = """
     _______  _______ _________ _______          
    (  ____ \(  ____ )\__   __/(  ____ \|\     /|
    | (    \/| (    )|   ) (   | (    \/| )   ( |
    | |      | (____)|   | |   | (_____ | (___) |
    | |      |     __)   | |   (_____  )|  ___  |
    | |      | (\ (      | |         ) || (   ) |
    | (____/\| ) \ \__   | |   /\____) || )   ( |
    (_______/|/   \__/   )_(   \_______)|/     \|
                                             
           Coded By - Nehal Zaman, Shivank Sharma and Kaushal Sarda
    """
    print(colored(banner, "blue"))
    subdomains = get_crtsh(domain)
    for subdomain in subdomains:
        print(colored(f"  {subdomain}", "green"))
    if output_file:
        with open(output_file, "w") as wf:
            for subdomain in subdomains:
                wf.write(subdomain + "\n")
