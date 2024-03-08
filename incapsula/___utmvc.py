from requests import Session, post
from re import search

def is_challenge(response):
    pattern = r'src="(/_Incapsula_Resource\?[^"]+)"'
    match = search(pattern, response.text)
    return f"https://{response.url.split('/')[2]}/{match.group(1)}" if match else False

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Your api key here

    session = Session()
    url = "https://tickets.rolandgarros.com/fr/"
    headers = {
        'Host': 'tickets.rolandgarros.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="112", "Chromium";v="112", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en;q=0.9',
    }
    response = session.get(url, headers=headers)
    if not (challenge_url := is_challenge(response)):
        print("Page loaded successfully")
        exit(0)

    print(f"Found challenge, solving...")

    # Load challenge
    challenge = session.get(challenge_url, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    })

    # Solve the challenge
    takion_response = post(
        f"https://takionapi.tech/incapsula/utmvc?api_key={API_KEY}",
        json={
            "content": challenge.text,
            "cookies": [[name, value] for name, value in session.cookies.items()]
        },
        headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }
    ).json()
    if (error := takion_response.get("error")):
        print(f"Error: {error}")
        exit(1)
    
    # Set the utmvc cookie
    utmvc = takion_response["___utmvc"]
    session.cookies.set("___utmvc", utmvc)
    print(f"Got cookie: {utmvc[:15]}...{utmvc[-15:]}")
    # Now we send the original request again
    response = session.get(url, headers=headers)
    print(f"Challenge {'' if is_challenge(response) else 'not '}found using cookie")