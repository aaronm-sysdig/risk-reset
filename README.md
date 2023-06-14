# Disclaimer

Notwithstanding anything that may be contained to the contrary in your agreement(s) with Sysdig, Sysdig provides no support, no updates, and no warranty or guarantee of any kind with respect to these script(s), including as to their functionality or their ability to work in your environment(s).  Sysdig disclaims all liability and responsibility with respect to any use of these scripts. 

# Sysdig Risk Reseet
Example python code that allows you to reset all yours risks to xx days from todays date

***NOTE: This script uses unsupported, undocumented API's that may change at any point.***



## Parameters


| Parameter | Mandatory? | Example | Usage |
|---|---|---|---|
| days | Y | 30 | Number of days that you wish to extend all risks by |
| apiurl | Y | https://app.au1.sysdig.com | Base API URL to use |
| apitoken | N | 238b5402-9354-405a-8d62-08c5ce5d3e68 | Your API token.  Will also attempt to retrieve from SECURE_API_TOKEN environment variable if not specified here|

## Usage
```
pip3 install -r requirements.txt
python3 risk-reset.py --days xx --apiurl https://app.xxx.sysdig.com --apitoken 238b5402-9354-405a-8d62-08c5ce5d3e68
```
