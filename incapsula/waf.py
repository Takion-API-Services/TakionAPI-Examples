from requests import Session, get
from re import search

def is_challenge(response):
    pattern = r'src="(/_Incapsula_Resource\?[^"]+)"'
    match = search(pattern, response.text)
    return f"https://{response.url.split('/')[2]}{match.group(1)}" if match else False

def extract_waf_details(response):
    geetest_pattern = r'xhr\.open\("GET",\s*"(/_Incapsula_Resource\?[^"]+)"'
    post_pattern = r'xhr2\.open\("POST",\s*"(/_Incapsula_Resource\?[^"]+)"'
    return {
        "geetest_url": None if not (geetest_match := search(geetest_pattern, response.text)) else f"https://{response.url.split('/')[2]}{geetest_match.group(1)}",
        "post_url": None if not (post_match := search(post_pattern, response.text)) else f"https://{response.url.split('/')[2]}{post_match.group(1)}"
    }

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Your api key here

    session = Session()

    url = "https://www.smythstoys.com/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    # 1. We use bad headers to trigger the WAF 
    response = session.get(url, headers=headers)
    if not (challenge_url := is_challenge(response)):
        print("Page loaded successfully")
        exit(0)
    
    # 2. If the content type isn't text/html means that isn't the
    # WAF (just the classic challenge)
    if response.headers.get('Content-Type') == 'text/html':
        print("WAF not triggered")
        exit(0)
    print("Waf challenge found")

    # 3. Load challenge page
    challenge = session.get(challenge_url, headers={
        'Host': 'www.smythstoys.com',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://www.smythstoys.com/',
        'accept-language': 'en-GB,en;q=0.9',
    })

    # 4. Extract needed data
    data = extract_waf_details(challenge)

    # 5. Solve the GeeTest
    print("Solving geetest challenge...")
    geetest_data = session.get(data["geetest_url"], headers=headers).json()
    geetest_solved = get(
        f"https://takionapi.tech/geetest/{geetest_data['gt']}/{geetest_data['challenge']}?api_key={API_KEY}",
        headers=headers
    )
    geetest_solved = geetest_solved.json()
    if (error := geetest_solved.get("error")):
        print(error)
        exit(0)

    # 6. Submit the challenge
    session.post(data["post_url"], data=geetest_solved, headers={
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
    })


    # 7. Load again the page
    response = session.get("https://www.smythstoys.com/", headers={
        'Host': 'www.smythstoys.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.smythstoys.com/',
        'accept-language': 'en-GB,en;q=0.9',
    })
    print(f"Challenge {'' if is_challenge(response) else 'not '}found using cookie")