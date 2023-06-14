# Disclaimer

Notwithstanding anything that may be contained to the contrary in your agreement(s) with Sysdig, Sysdig provides no support, no updates, and no warranty or guarantee of any kind with respect to these script(s), including as to their functionality or their ability to work in your environment(s).  Sysdig disclaims all liability and responsibility with respect to any use of these scripts. 

# Sysdig Risk Reset
Example python code that allows you to reset all yours risks to xx days from todays date

***NOTE: This script uses unsupported, undocumented API's that may change at any point.***



## Command Line Parameters
| Parameter | Mandatory? | Example | Environment Variable Name | Usage |
|---|---|---|---|---|
| days | N | 30 | DAYS | Any risks with an expiration date > "Today + \<DAYS\>" will be set to "Today + \<DAYS\>".  I.E, if a risk is 60 days into the future when days=30, it will have its expiration date set to "Today + 30 days" |
| apiurl | N | https://app.au1.sysdig.com | API_URL | Base API URL to use Will also attempt to retrieve from API_URL environment variable if not specified here |

## Passing API Token
Your SYSDIG API TOKEN needs to be set as the 'SECURE_API_TOKEN' environment variable.  You will receive an error if this is not the case

```
Please set the SECURE_API_TOKEN environment variable to continue
```

## Usage
```
pip3 install -r requirements.txt
python3 risk-reset.py --days xx --apiurl https://app.xxx.sysdig.com
```

## Example Output

```
SUCCESS: 'CVE-2018-8088' updated to '2023-07-14'

Done, have a nice day! 
```
