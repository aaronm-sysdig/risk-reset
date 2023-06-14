import datetime
import sys
import argparse
import os
import requests
import time

SLEEP_429_SECONDS = 30


def sysdig_request(method, url, headers, params=None, _json=None) -> requests.Response:
    objResult = requests.Response
    try:
        objResult = requests.request(method=method, url=url, headers=headers, params=params, json=_json)
        objResult.raise_for_status()
        while objResult.status_code == 429:
            print(f"Got status 429, Sleeping for {SLEEP_429_SECONDS} seconds before trying again")
            time.sleep(SLEEP_429_SECONDS)
            objResult = requests.request(method=method, url=url, headers=headers, params=params, json=_json)
    except requests.exceptions.HTTPError as e:
        print(" ERROR ".center(80, "-"))
        print(e)
        exit(1)
    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)

    return objResult


def main() -> None:
    objParser = argparse.ArgumentParser(description='Risk Reset')
    objParser.add_argument('--days', required=False,
                           type=int,
                           default=os.environ.get('DAYS', None),
                           help='Reset acceptances > <DAYS> from today to <DAYS> (Default: DAYS Environment Variable)')
    objParser.add_argument('--api_url',
                           required=False,
                           type=str,
                           default=os.environ.get('API_URL', None),
                           help='API URL I.E https://app.au1.sysdig.com (Default: API_URL Environmenet variable')

    objArgs = objParser.parse_args()
    if objArgs.days is None or objArgs.api_url is None:
        objParser.parse_args(['--help'])
        exit(1)

    api_token = os.environ.get('SECURE_API_TOKEN')
    if api_token is not None:
        auth_header = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    else:
        print('Please set the SECURE_API_TOKEN environment variable to continue')
        exit(1)

    api_url = objArgs.api_url
    strRiskURL = f"{api_url}/api/scanning/riskmanager/v2/definitions"
    arrExistingRisks = []

    # Retrieve list of current risks
    objResult = sysdig_request(method='GET', url=strRiskURL, params={'limit': 50}, headers=auth_header)
    if objResult.json()['page']['returned'] > 0:
        for row in objResult.json()['data']:
            arrExistingRisks.append(row)

    # Iterate through until we get all the rows
    while objResult.json()['page']['next'] != "":
        for row in objResult.json()['data']:
            arrExistingRisks.append(row)
        objResult = sysdig_request(method='GET',
                                   url=strRiskURL,
                                   params={'cursor': objResult.json()['page']['next'], 'limit': 50},
                                   headers=auth_header)

    # If current expiration days are > --days property, reset to --days
    rem_list = ['createdAt', 'updatedAt', 'status', 'riskAcceptanceDefinitionID']

    for row in arrExistingRisks:
        updated_row = row
        riskAcceptanceDefinitionID = row['riskAcceptanceDefinitionID']
        [updated_row.pop(key) for key in rem_list]
        # Covers 'global' exceptions without an expiration date
        if 'expirationDate' not in row:
            row['expirationDate'] = str(datetime.date.today() +
                                        datetime.timedelta(days=int(objArgs.days+1)))
        if datetime.date.today() < (datetime.datetime.strptime(row['expirationDate'], "%Y-%m-%d").date() -
                                    datetime.timedelta(days=int(objArgs.days))):
            updated_row['expirationDate'] = str(datetime.date.today() + datetime.timedelta(days=int(objArgs.days)))
            objResult = sysdig_request(method='PUT',
                                       url=f'{strRiskURL}/{riskAcceptanceDefinitionID}',
                                       headers=auth_header,
                                       _json=updated_row)
            if objResult.status_code == 200:
                print(f"SUCCESS: '{updated_row['entityValue']}' updated to '{updated_row['expirationDate']}'")
    print("\nDone, have a nice day! ")


if __name__ == "__main__":
    main()

