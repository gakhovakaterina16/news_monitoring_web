import requests

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        return False
