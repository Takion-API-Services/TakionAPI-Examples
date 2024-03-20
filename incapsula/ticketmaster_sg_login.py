from tls_client import Session
from requests import get
from bs4 import BeautifulSoup

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Fill it with your api key
    MAIL = "xxxx@xxxx.com" # Your TM SG Mail
    PASSWORD = "xxxxx" # Your TM SG Password

    session = Session("chrome_112")
    headers = {
        'Host': 'ticketmaster.sg',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://ticketmaster.sg/',
        'accept-language': 'en-GB,en;q=0.9',
    }

    # ------------------------- Generate reese84 ------------------------- #
    solving_browser = {
        "User-Agent": headers["user-agent"],
        "sec-ch-ua": headers["sec-ch-ua"]
    }
    response = get(f"https://takionapi.tech/incapsula/payload/www.ticketmaster.sg?api_key={API_KEY}", headers=solving_browser).json()
    if (error := response.get("error")):
        print(error)
        exit(0)
    challenge_url, challenge_headers, challenge_payload = response["url"], response["headers"], response["payload"]
    # Send challenge
    response = session.post(challenge_url, headers=challenge_headers, data=challenge_payload).json()
    # Set cookie
    session.cookies.set("reese84", response['token'])


    print("Starting...")
    # ------------------------- Load CSRF Token  ------------------------- #
    response = session.get('https://ticketmaster.sg/login', headers=headers)

    if (redirect := response.headers.get("Location")):
        response = session.get(redirect, headers=headers)

    headers = {
        'Host': 'main.login.ticketmaster.sg',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://main.login.ticketmaster.sg',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://main.login.ticketmaster.sg/login?client_id=6vdm5j83n4tc6i0ul4nm9ms6dm&redirect_uri=https%3A%2F%2Fticketmaster.sg%2Flogin&response_type=code&scope=phone+email+openid+aws.cognito.signin.user.admin',
        'accept-language': 'en-GB,en;q=0.9',
    }

    # ------------------------- Generate cognito ------------------------- #
    response = get(
        "https://takionapi.tech/aws/cognito",
        params={
            "api_key": API_KEY,
            "website": "www.ticketmaster.sg",
            "username": MAIL
        },
        headers=solving_browser
    ).json()["result"]

    # ------------------------- Login into acc.  ------------------------- #
    response = session.post(
        'https://main.login.ticketmaster.sg/login', 
        params={
            'client_id': '6vdm5j83n4tc6i0ul4nm9ms6dm',
            'redirect_uri': 'https://ticketmaster.sg/login',
            'response_type': 'code',
            'scope': 'phone email openid aws.cognito.signin.user.admin',
        },  
        headers=headers, 
        data={
            '_csrf': session.cookies.get_dict()["XSRF-TOKEN"],
            'username': MAIL,
            'password': PASSWORD,
            'cognitoAsfData': response,
            'signInSubmitButton': 'Sign in',
        }
    )
    if (redirect := response.headers.get("Location")):
        response = session.get(redirect, headers=headers)
    if (redirect := response.headers.get("Location")):
        response = session.get(redirect, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    if not (account_data := soup.find("div", {"id": "accountFunc"})):
        print(soup.find("p", {"id": "loginErrorMessage"}).text)
        exit(0)

    print("Logged in as " + account_data.find("div").text)