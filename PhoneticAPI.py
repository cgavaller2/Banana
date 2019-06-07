from web import download_json
import json


def api_request(api_key, textMessage, phoneticlist):
    """



    :param api_key: Key sent to the API.
    :param textMessage: Message sent to the API.
    :return: dict
    """

    headers = {'X-RapidAPI-Host': 'phonetic-bad-word-filter.p.rapidapi.com',
               'X-RapidAPI-Key': api_key,
               'Content-Type': 'application/json'}

    data = {'phrase': textMessage, "phoneticlist": phoneticlist, "whitelist":[], "blacklist": []}

    reply = download_json("https://phonetic-bad-word-filter.p.rapidapi.com/PhoneticCheck", headers=headers,
                          data=bytes(json.dumps(data), encoding="utf-8"))
    return reply
