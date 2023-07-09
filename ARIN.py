import csv
import requests
import os

def get_whois_info(ip):
    url = f"https://whois.arin.net/rest/ip/{ip}.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

file_path = os.path.join(os.getcwd(), 'whois_results.csv')
csv_file_path = os.path.join(os.getcwd(), 'ipcsv.csv')

with open(file_path, 'w') as file, open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        ip = row[0]
        file.write(f"{ip},")
        whois_info = get_whois_info(ip)
        
        if whois_info and 'net' in whois_info:
            org = whois_info['net'].get('orgRef', {}).get('@name')
            if org:
                file.write(f" {org}\n")
            else:
                file.write("Organization information not found.\n")
        else:
            file.write("Failed to retrieve WHOIS information.\n")
        
        file.write("\n")

print(f"Results saved to: {file_path}")
