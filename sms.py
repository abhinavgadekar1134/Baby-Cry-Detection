# print("SMS Sent Successfully :)")

import requests

def send_sms(message,mob_no):
	url = "https://www.fast2sms.com/dev/bulkV2"
	payload = "sender_id=FTWSMS&message="+ message +"&language=english&route=p&numbers="+ mob_no +""
	headers = {
	 'authorization': "M4dG7yC8obL09ExtFwrH6B3XWAqInKDVZliPpOaUh2Yse5jczSHQpJ5WOmn4lK6TtuSGaZwxhfUReYq7",
	 'Content-Type': "application/x-www-form-urlencoded",
	 'Cache-Control': "no-cache",
	 }
	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)

send_sms("Baby is crying","8010700592")
