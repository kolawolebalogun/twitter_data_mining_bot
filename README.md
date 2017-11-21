# Twitter Data Mining Bot
A bot that extracts the following from people’s Twitter bio (on public/open accounts), into a Google spreadsheet:

* Email address 
* Twitter profile name 
* Number of followers

Target accounts using either of these criteria:
* Based on hashtags used
* Based on number of followers; Between 1,000 - 50,000

## Requirement

Twitter Data Mining bot has been tested in the following environments

* Python (3.6)


## Installation

First you create a virtual environment with `virtualenv venv` and enter it with `source venv/bin/activate` in order to keep everything contained. 

Then you run `pip install -r requirements.txt` to install all dependencies

Start bot by running this command `python main.py`

## Demo
![screen shot](https://user-images.githubusercontent.com/8668661/33088863-330b4250-ceef-11e7-9e9c-b4fd9ca299d8.gif)

You can view google spreadsheet [here](https://docs.google.com/spreadsheets/d/1xMJKDKP90hgihQsUaeiWiXH5KhDPNgEKuMxwSB0_79c)

## Challenge
Getting users email from twitter api will require Privacy Policy URL and Terms of Service URL and requires the user to allow collection of email, I skipped getting the user email from their profile, in lieu I mined the user bio for any email address if available  
