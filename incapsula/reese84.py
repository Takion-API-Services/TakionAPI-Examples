from requests import get, Session

API_KEY = "TAKION_API_XXX" # Fill it with your api key

# Define protected url and headers
protected_url = "https://www.ticketmaster.com/event/1C005E959B003CA9"
headers = {
    "Host": "www.ticketmaster.com",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-ch-ua-mobile": "?0",
    "upgrade-insecure-requests": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "sec-fetch-mode": "navigate",
    "sec-fetch-dest": "document",
    "sec-ch-ua": '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-fetch-site": "same-site",
    "sec-fetch-user": "?1",
    "accept-language": "en-US,en;q=0.9"
}


def send_request_with_solving() -> None:
    '''
    Send request to protected url after solving the challenge
    '''
    # Create a new session
    session = Session()

    # If u want, you can select a specific browser/OS/chrome version to solve the challenge
    # just pass "Usear-Agent" and "sec-ch-ua" headers to the session
    # (not required)
    solving_browser = {
        "User-Agent": headers["user-agent"],
        "sec-ch-ua": headers["sec-ch-ua"]
    }
    response = get(f"https://takionapi.tech/incapsula/payload/www.ticketmaster.com?api_key={API_KEY}", headers=solving_browser).json()
    if (error := response.get("error")):
        print(error)
        exit(0)
    challenge_url, challenge_headers, challenge_payload = response["url"], response["headers"], response["payload"]
    # Send challenge
    response = session.post(challenge_url, headers=challenge_headers, data=challenge_payload).json()
    # Set cookie
    session.cookies.set("reese84", response['token'])

    # Sending request to protected url 
    res = session.get(protected_url, headers=headers)
    print(f"Response with solving -> {res.status_code}")

def send_request_without_solving() -> None:
    '''
    Send request to protected url without solving the challenge
    '''
    # Create a new session
    session = Session()

    # Sending request to protected url
    res = session.get(protected_url, headers=headers)
    print(f"Response without solving -> {res.status_code}")

if __name__ == "__main__":
    send_request_with_solving() # Will return 404, the URL is old
    send_request_without_solving() # Will return 403 or 401