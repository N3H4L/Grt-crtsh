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
    subdomains = []
    for i in data:
        nvs = i['name_value'].split("\n")
        cns = i['common_name'].split("\n")
        for nv in nvs:
            if nv not in subdomains and nv != domain and not nv.startswith("*"):
                subdomains.append(nv)
        for cn in cns:
            if cn not in subdomains and cn != domain and not cn.startswith("*"):
                subdomains.append(cn)
    return subdomains


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
                                             
           Coded By - Nehal Zaman and Shivank Sharma (@pwnersec)
    """
    print(colored(banner, "blue"))
    subdomains = get_crtsh(domain)
    for subdomain in subdomains:
        print(colored(f"  {subdomain}", "green"))
    if output_file:
        with open(output_file, "w") as wf:
            for subdomain in subdomains:
                wf.write(subdomain + "\n")
