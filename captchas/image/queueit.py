from requests import post
from base64 import b64decode

def load_captcha():
    url = "https://footlocker.queue-it.net/challengeapi/queueitcaptcha/challenge/en-us"
    headers = { 
        "Host": "footlocker.queue-it.net",
        "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"macOS',
        "accept": "*/*",
        "origin": "https://footlocker.queue-it.net",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://footlocker.queue-it.net/",
        "accept-language": "en-GB,en;q=0.9",
        "x-queueit-challange-customerid": "footlocker",
        "x-queueit-challange-eventid": "cxcdtest02",
        "x-queueit-challange-hash": "sg7R/eOE9jBw1RMb1iI7d1M8uKgf6sErktuA3Q69hgw=",
        "x-queueit-challange-reason": "1"
    }
    return post(url, headers=headers).json()['imageBase64']


if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Fill it with your api key
    
    b64image = load_captcha()
    result = post(
        "https://takionapi.tech/ocr",
        json={
            "image": b64image
        },
        headers={
            "x-api-key": API_KEY
        }
    ).json()
    if (error := result.get("error")):
        print(error)
        exit(0)
    print(f"Solved! {result['result']}")

    # Save image for debugging
    with open("queueit.png", "wb") as fh:
        fh.write(b64decode(b64image))