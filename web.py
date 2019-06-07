import json
import sys
import urllib


def download_website(url, headers=None, data=None):
    """

    Downloads website from url.

    :param url: url to open request to.
    :param headers: Form data sent to website.
    :param data: Form data sent to website.
    :return: str, int, None
    """
    try:
        from urllib.request import urlopen, Request
    except ImportError:
        sys.exit("Unsupported version of Python. You need Version 3 :<")

    if headers and data:
        request = Request(url, headers=headers, data=data)
    elif headers:
        request = Request(url, headers=headers)
    elif data:
        request = Request(url, data=data)
    else:
        request = Request(url)

    try:
        response = urlopen(request)
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        try:
            return e.read().decode('utf-8')
        except AttributeError:
            return None
        return None
    website_bytes = response.read()
    return website_bytes.decode('utf-8')


def download_json(url, headers=None, data=None):
    """

    Downloads website from url and parses download to a dict.

    :param url: url to open request to.
    :param headers: Form data sent to website.
    :param data: Form data sent to website.
    :return: str, int, Nones

    """

    def parse_json():
        """
        Parse Json
        """

        try:
            return json.loads(json_string)
        except TypeError:
            print("Failed to parse JSON.")
        return None

    json_string = download_website(url, headers=headers, data=data)
    if json_string is None:
        return None
    return parse_json()

