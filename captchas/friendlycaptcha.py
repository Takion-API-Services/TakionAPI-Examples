from requests import get, post
from json import loads
from bs4 import BeautifulSoup

def askforPuzzle(siteKey: str, url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 OPR/44.0.2510.857',
        'Accept': '*/*',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'none',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-us-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'dnt': '1',
        'x-frc-client': 'js-0.9.0'
    }

    res = get(url, headers=headers, params={'sitekey': siteKey})
    try: 
        return loads(res.text)['data']['puzzle']
    except: 
        print('Error getting Puzzle!')
        exit(0)

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Fill it with your api key

    # Generate and solve challenge
    puzzle = askforPuzzle('FCMGEMUD2KTDSQ5H', 'https://api.friendlycaptcha.com/api/v1/puzzle')
    print(f'Puzzle generated: {puzzle}, solving...')

    querystring = {
        "puzzle": puzzle,
        "api_key": API_KEY
    }

    data = get("https://takionapi.tech/friendlycaptcha", params=querystring).json()
    if (error := data.get("error")):
        print(error)
        exit(0)
    solution = data["solution"]
    print('Solved!', data)

    # Submit challenge
    payload = {
        "name": "bad captcha",
        "feedback": ":/",
        "thoughts": ":D",
        "frc-captcha-solution": solution
    }
    headers = {
        "authority": "friendlycaptcha.com",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "trp_language=en_US; pdfcc=12",
        "origin": "https://friendlycaptcha.com",
        "referer": "https://friendlycaptcha.com/demo",
        "sec-ch-ua": '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    response = post("https://friendlycaptcha.com/demo", data=payload, headers=headers)
    data = BeautifulSoup(response.text, 'html.parser')
    print(f"Response: {data.find('h3', {'class': 'title'}).text}")