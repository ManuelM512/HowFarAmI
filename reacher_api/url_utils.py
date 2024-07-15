from datetime import datetime
import requests


def get_url(session: requests.Session, url: str):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        r8_now = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"An error occurred: {e}")
        print(f"{r8_now} - URL: {url}")
        return False
