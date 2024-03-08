from requests import post
from tls_client import Session

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Fill it with your api key

    session = Session(
        "chrome_121", 
        header_order=list({
            "authority": "www.zocdoc.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": '"Google Chrome";v="110", "Chromium";v="110", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        })
    )

    # An example Datadome protected page
    url = "https://www.footlocker.pt/en/product/~/314206535404.html"
    response = session.get(url, headers={
        "authority": "www.footlocker.pt",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Google Chrome";v="110", "Chromium";v="110", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    })
    if not (("geo.captcha-delivery.com" in response.text or \
            "interstitial.captcha-delivery.com" in response.text) \
                and response.status_code == 403): # Check if we need to solve a challenge
        print("Page loaded successfully")
        exit(0)
    
    print("Challenge returned by Datadome")

    # 1. Build challenge URL
    response = post(
        f"https://datadome.takionapi.tech/build", 
        headers={
            "x-api-key": API_KEY
        },
        json={
            "datadome": session.cookies.get_dict().get("datadome"),
            "referer": url,
            "html": response.text
        }
    ).json()
    if (error := response.get("error")):
        print(error)
        exit(0)
    challenge_url = response["url"]

    # 2. Load challenge page
    print(f"Solving {response['challenge_type']} challenge...")
    challenge = session.get(challenge_url, headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en;q=0.9",
        "Accept-Encoding": "none",
        "Connection": "keep-alive",
        "Referer": "https://www.footlocker.pt/",
        "Sec-Fetch-Dest": "iframe",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="110", "Chromium";v="110", "Not?A_Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\""
    })

    # 3. Solve challenge
    data = post(
        f"https://datadome.takionapi.tech/solve", 
        headers={
            "x-api-key": API_KEY,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        },
        json={
            "html": challenge.text
        }
    ).json()
    if (error := data.get("error")):
        print(error)
        exit(0)

    # 4. Send payload to Datadome
    res = session.post(
        data["url"], 
        data=data["payload"], 
        headers=data["headers"]
    )

    # 5. Set cookie
    cookie = res.json()["cookie"].split("datadome=")[1].split("; ")[0]
    session.cookies.set("datadome", cookie)
    print(f"Got cookie: {cookie[:15]}...{cookie[-15:]}")

    # 6. Load again
    print("Loading page with cookie...")
    response = session.get(url, headers={
        "authority": "www.footlocker.pt",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": '"Google Chrome";v="110", "Chromium";v="110", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    })
    print(f"Got a response with status code {response.status_code} with the cookie")