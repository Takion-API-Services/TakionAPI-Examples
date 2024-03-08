from requests import get

if __name__ == "__main__":
    API_KEY = "TAKION_API_XXX" # Fill it with your api key

    response = get("https://epsf.ticketmaster.co.uk/vamigood", headers={
        "authority": "epsf.ticketmaster.co.uk",
        "accept": "*/*",
        "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
        "brand": "tm",
        "origin": "https://ticketmaster.co.uk",
        "referer": "https://www.ticketmaster.co.uk/",
        "requesting-host": "ticketmaster.co.uk",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "x-lang": "nl-nl"
    }).text
    gt = response.split('gt: "')[1].split('"')[0]
    challenge = response.split('challenge: "')[1].split('"')[0]

    print(f"Solving GeeTest: {gt=} {challenge=}")

    geetest_solved = get(f"https://takionapi.tech/geetest/{gt}/{challenge}?api_key={API_KEY}").json()
    if (error := geetest_solved.get("error")):
        print(error)
        exit(0)
    print(f"Solved! {geetest_solved}")