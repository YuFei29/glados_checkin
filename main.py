#!/usr/bin/env python3

import requests, json, os


# GLaDOS cookie
COOKIES = os.environ["COOKIES"]
cookies = COOKIES.split('&&')

# push switch: on or off
pushp = os.environ["PUSHP"]

# push token
push_token = os.environ["PTOKEN"]


def main():    
    curl = "https://glados.rocks/api/user/checkin"
    surl = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    payload = {
        'token': 'glados.network'
    }

    for cookie in cookies:
        checkin = requests.post(
            curl,
            headers = {
                'cookie': cookie,
                'referer': referer,
                'origin': origin,
                'user-agent': useragent,
                'content-type': 'application/json;charset=UTF-8'
            },
            data = json.dumps(payload)
        )
        status = requests.get(
            surl,
            headers = {
                'cookie': cookie,
                'referer': referer,
                'origin': origin,
                'user-agent': useragent
            }
        )

        left_days = status.json()['data']['leftDays'].split('.')[0]
        user_email = status.json()['data']['email']

        # if 'message' in checkin.text:
        #     if pushp == 'on':
        #         msg = checkin.json()['message']
        #         requests.get('http://www.pushplus.plus/send?token=' + push_token + '&title='+msg+'&content='+user_email+' left '+left_days+' day(s).')
        # else:
        #     requests.get('http://www.pushplus.plus/send?token=' + push_token + '&content='+user_email+' need update cookie!!!')

        if 'message' in checkin.text:
            if pushp == 'on':
                token = push_token
                title = checkin.json()['message']
                content = user_email + ' Left ' + left_days + ' Day(s).'
                url = 'http://www.pushplus.plus/send'
                data = {
                    "token":token,
                    "title":title,
                    "content":content
                }
                body=json.dumps(data).encode(encoding='utf-8')
                headers = {'Content-Type':'application/json'}
                requests.post(url,data=body,headers=headers)
        else:
            token = push_token
            title = 'Checkin Failed'
            content = user_email + 'Cookie Need Update!!!'
            url = 'http://www.pushplus.plus/send'
            data = {
                "token":token,
                "title":title,
                "content":content
            }
            body=json.dumps(data).encode(encoding='utf-8')
            headers = {'Content-Type':'application/json'}
            requests.post(url,data=body,headers=headers)


if __name__ == '__main__':
    main()
