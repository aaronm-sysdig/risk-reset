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
    except requests.exceptions.RequestException as e:
        print(e)

    return objResult


def main() -> None:
    objParser = argparse.ArgumentParser(description='Risk Reset')
    objParser.add_argument('--days', required=True,
                           type=int,
                           default=30,
                           help='Reset all acceptance dates to xx days in advance of today (Default: 30')
    objParser.add_argument('--apitoken',
                           required=False,
                           type=str,
                           default=os.environ.get('SECURE_API_TOKEN', None),
                           help='API token (Default: SECURE_API_TOKEN environment variable)')
    objParser.add_argument('--apiurl',
                           required=True,
                           type=str,
                           help='API URL (i.e https://app.au1.sysdig.com)')

    objParser.parse_args(args=None if sys.argv[1:] else ['--help'])
    objArgs = objParser.parse_args()

    auth_header = {
        "Authorization": f"Bearer {objArgs.apitoken}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    api_token = objArgs.apitoken
    api_url = objArgs.apiurl
    strRiskURL = f"{api_url}/api/scanning/riskmanager/v2/definitions"
    arrExistingRisks = []

    # Retrieve list of current risks
    objResult = sysdig_request(method='GET', url=strRiskURL, params={'limit': 2}, headers=auth_header)
    print(objResult.status_code)
    while objResult.json()['page']['next'] != "":
        for row in objResult.json()['data']:
            arrExistingRisks.append(row)
        objResult = sysdig_request(method='GET',
                                   url=strRiskURL,
                                   params={'cursor': objResult.json()['page']['next'], 'limit': 2},
                                   headers=auth_header)

    # Reset days
    rem_list = ['createdAt', 'updatedAt', 'status', 'riskAcceptanceDefinitionID']

    for row in arrExistingRisks:
        updated_row = row
        riskAcceptanceDefinitionID = row['riskAcceptanceDefinitionID']
        [updated_row.pop(key) for key in rem_list]
        updated_row['expirationDate'] = str(datetime.date.today() + datetime.timedelta(days=int(objArgs.days)))
        objResult = sysdig_request(method='PUT',
                                   url=f'{strRiskURL}/{riskAcceptanceDefinitionID}',
                                   headers=auth_header,
                                   _json=updated_row)
        print(objResult.status_code)
    print("Done")


if __name__ == "__main__":
    main()
