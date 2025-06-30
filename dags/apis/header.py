import os

adprofex = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru',
        'Authorization': f'Bearer {os.getenv("ADPROFEX_TOKEN")}',
        'Connection': 'keep-alive',
        'Origin': 'https://advertiser.adprofex.com',
        'Referer': 'https://advertiser.adprofex.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }