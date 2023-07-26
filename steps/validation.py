from behave import step
import csv
import sys
import json
from haralyzer import HarParser
import base64

csv.field_size_limit(sys.maxsize)

class PrintInColor:
    COLOR = '\033[93m'
    END = '\033[0m'
    ORANGE = '\033[33m'

    @classmethod
    def red(cls, s, **kwargs):
        print(cls.COLOR + s + cls.END, **kwargs)
#insert path to csv file
path_csv = ''
#insert path to har file
path_har = ''


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
                    print(PrintInColor.COLOR + key + '=' + value + PrintInColor.END)


@step('Create full data list {param}')
def strong_list(context, param):
    print("\nParams:")
    for match in context.list_CSV:
        if match is not None:
            if param in match.keys() and match[param]:
                print(PrintInColor.COLOR + param + '=' + match[param] + PrintInColor.END, end="\n")


@step('3p beacons check')
def three_p_beacons_check(context):
    # Load the HAR file as a JSON object
    with open(path_har, 'r', encoding='utf-8-sig') as f:
        har_data = json.load(f)

    # Create a HarParser instance with the HAR data
    har_parser = HarParser(har_data)

    # Get the entries from the HAR file
    entries = har_parser.har_data['entries']

    # Extract the data you need from each entry
    for entry in entries:
        request = entry['request']
        response = entry['response']

        # Get the URL of the request
        url = request['url']

        # Check if the URL contains the target string
        if 'ads.digital.disneyadvertising.com' in url:
            # Get the response content and extract the text
            response_content = response['content']
            response_text = response_content.get('text', '')
            decoded_data = base64.b64decode(response_text).decode('utf-8')

            print(json.dumps(json.loads(decoded_data), indent=2))
