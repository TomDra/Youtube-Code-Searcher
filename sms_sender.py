import requests
from twilio.rest import Client
import config as c


def send(codes):
    client = Client(c.SMS['CLIENT_ID'], c.SMS['API_KEY'])
    message = "https://www.amazon.co.uk/gc/redeem/ref=gc_lp_atya?siteState=clientContext%3D261-2958363-2405635%2CsourceUrl%3Dhttps%253A%252F%252Fwww.amazon.co.uk%252Fgc%252Fredeem%252Fref%253Dgc_lp_atya%2Csignature%3Dm5xbjx66IaZoQcM6CERGe3Lgu6wj3D\nCodes:\n"
    client.messages.create(to=c.SMS['TO'],
                           from_=c.SMS['FROM'],
                           body=message)
    for code in codes:
        client.messages.create(to=c.SMS['TO'],
                               from_=c.SMS['FROM'],
                               body=code)


def get_jpg_files(path):
    """
    Get all mp4 files in the given path
    """
    import os
    jpg_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                jpg_files.append(os.path.join(root, file))
    return jpg_files


def webhook_message(code_file):
    file = code_file

    url = c.discord_webhook['URL']  # webhook url, from here: https://i.imgur.com/f9XnAew.png
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    if True:
        data = {
            "username": "Code Found"
        }

        data["embeds"] = [
            {
                "description": "text in embed",
                "title": "embed title",
                "image": {
                }
            }
        ]

        # send a message to the webhook which includes an embeded image as part of the data
        result = requests.post(url, json=data, files={'file': (file, open(file,
                                                                          'rb'))})  # , headers={"Content-Type": "multipart/form-data"}#,"file":'3EYZ_3ELTMF_5VBC_frame18330.jpg'})#, file='@3EYZ_3ELTMF_5VBC_frame18330.jpg')#, files={'code' : 'codes/3EYZ_3ELTMF_5VBC_frame18330.jpg'})

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
