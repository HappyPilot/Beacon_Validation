from behave import step
import csv
import sys
import json
from haralyzer import HarParser
import base64
from colorama import Fore, Style
from urllib.parse import urlparse
import re

csv.field_size_limit(sys.maxsize)

#insert path to csv file
path_csv = '/Users/Dmytro.Dubovsky.-ND/Downloads/tvOS DAI adpossition #1.csv'
#insert path to har file
path_har = '/Users/Dmytro.Dubovsky.-ND/Downloads/iOS_2_22_0_adbeacons_pod.har'


@step('Parsing csv')
def pars_csv(context):

    context.list_CSV = []
    with open(path_csv) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['URL']  # replace 'url' with the actual column name
            params = params = dict(param.split('=', 1) for param in url.split('&') if '=' in param)
            context.list_CSV.append(params)

@step('Create url data list {param}')
def url_list(context, param):
    print("\nParams:")
    for match in context.list_CSV:
        if match is not None:
            for key, value in match.items():
                if param in key or param in value:
                    print(Fore.YELLOW + key + '=' + value + Style.RESET_ALL)


@step('Create full data list {param}')
def strong_list(context, param):
    print("\nParams:")
    for match in context.list_CSV:
        if match is not None:
            if param in match.keys() and match[param]:
                print(Fore.YELLOW + param + '=' + match[param] + Style.RESET_ALL, end="\n")

# List of domains to check
domains_to_count = [

    '2mdn.net',
    'activemetering.com',
    'adsafeprotected.com',
    'adsrvr.org',
    'doubleclick.net',
    'doubleverify.com',
    'extremereach.io',
    'flashtalking.com',
    'googlesyndication.com',
    'imrworldwide.com',
    'innovid.com',
    'ispot.tv',
    'moatads.com',
    'pix.pub',
    'pointmediatracker.com',
    'samba.tv',
    'samplicio.us',
    'scorecardresearch.com',
    'serving-sys.com',
    'tremorhub.com',
    'truoptik.com'
]

@step('3p beacons check')
def three_p_beacons_check(context):
    # Load the HAR file as a JSON object
    with open(path_har, 'r', encoding='utf-8-sig') as f:
        har_data = json.load(f)

    # Create a HarParser instance with the HAR data
    har_parser = HarParser(har_data)

    # Get the entries from the HAR file
    entries = har_parser.har_data['entries']

    # Initialize a dictionary to hold the counts for each domain
    domain_counts = {domain: 0 for domain in domains_to_count}

    # A set to store all unique domains extracted from decoded_data
    unique_domains = set()
    # Regular expression pattern to match domains in the decoded_data
    domain_pattern = r'"https://(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}'

    # Extract the data you need from each entry
    for entry in entries:
        request = entry['request']
        response = entry['response']

        # Get the URL of the request
        url = request['url']

        # Check if the URL contains the target string
        if 'ads.digital.disneyadvertising.com' in url:
            response_content = response['content']
            response_text = response_content.get('text', '')
            decoded_data = base64.b64decode(response_text).decode('utf-8')

            # Count occurrences of each domain in the decoded_data
            for domain in domains_to_count:
                if domain in decoded_data:
                    domain_counts[domain] += decoded_data.count(domain)

            # Extract all domains from decoded_data using regex
            matches = re.findall(domain_pattern, decoded_data)
            unique_domains.update(matches)

            print(json.dumps(json.loads(decoded_data), indent=2))

            # Print the domain counts for domains with count > 0
        print("Domain Counts:")
        for domain, count in domain_counts.items():
            if count > 0:
                print(Fore.YELLOW + f"{domain}: {count}" + "\n" + Style.RESET_ALL, end="\n")

        # Print all unique domains without subdomains
        print("Unique Domains without Subdomains:")
        for domain in unique_domains:
            domain_without_subdomain = domain.split('.')[-2:]  # Get the last two parts of the domain
            print(Fore.LIGHTGREEN_EX + '.'.join(domain_without_subdomain) + "\n" + Style.RESET_ALL)
