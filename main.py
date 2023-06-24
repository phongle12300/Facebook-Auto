# This is a sample Python script.
import os, sys, requests, re, bs4
import time

from bs4 import BeautifulSoup as bs
from queue import Queue
from threading import Thread
from time import sleep
from random import randint


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Token:
    def __init__(self, cookie):
        self.xyz = requests.Session()
        self.cookie = {'cookie': cookie}
        self.app_id = [
            '1348564698517390|007c0a9101b9e1c8ffab727666805038',  # --> Meta Portal
            '1174099472704185|0722a7d5b5a4ac06b11450f7114eb2e9',  # --> Messenger Kids for iOS
            '155327495133707|a151725bc9b8808a800f4c891505e558',  # --> Facebook Watch for Oculus
            '1331685116912965|e334a1eca4d4ea9ac0c0132a31730663',  # --> Facebook Watch for Xbox
            '867777633323150|446fdcd4a3704f64e5f6e5fd12d35d01',  # --> Facebook Watch for Amazon Fire TV
            '437340816620806|04a36c2558cde98e185d7f4f701e4d94',  # --> Facebook Watch for Android TV
            '661587963994814|ffe07cc864fd1dc8fe386229dcb7a05e',  # --> Facebook Watch for Apple TV
            '1692575501067666|3168904bd42ebb12bf981327de99179f',  # --> Facebook Watch for Samsung TV
        ]
        self.accessToken = self.get_kode(self.app_id[0])
        # for x in app_id:
        #     self.get_kode(x)

    def get_kode(self, act):
        data = {
            'access_token': act,
            'scope': ''}
        req = self.xyz.post('https://graph.facebook.com/v16.0/device/login/', data=data).json()
        try:
            cd, ucd = req['code'], req['user_code']
            url = 'https://graph.facebook.com/v16.0/device/login_status?method=post&code=%s&access_token=%s' % (cd, act)
            self.verify1(ucd, act)
            return self.get_token(url)
        except Exception as e:
            print('Login Gagal --> %s' % (act))

    def verify1(self, ucd, act):
        req = bs(self.xyz.get('https://mbasic.facebook.com/device', cookies=self.cookie).content, 'html.parser')
        raq = req.find('form', {'method': 'post'})
        dat = {
            'jazoest': re.search('name="jazoest" type="hidden" value="(.*?)"', str(raq)).group(1),
            'fb_dtsg': re.search('name="fb_dtsg" type="hidden" value="(.*?)"', str(req)).group(1),
            'qr': '0',
            'user_code': ucd}
        rel = 'https://mbasic.facebook.com' + raq['action']
        pos = bs(self.xyz.post(rel, data=dat, cookies=self.cookie).content, 'html.parser')
        self.verify2(pos, ucd, act)

    def verify2(self, req, ucd, act):
        dat = {}
        raq = req.find('form', {'method': 'post'})
        for x in raq('input', {'value': True}):
            try:
                if x['name'] == '__CANCEL__':
                    pass
                else:
                    dat.update({x['name']: x['value']})
            except Exception as e:
                pass
        rel = 'https://mbasic.facebook.com' + raq['action']
        pos = bs(self.xyz.post(rel, data=dat, cookies=self.cookie).content, 'html.parser')
        if 'Sukses!' in str(pos):
            pass
        else:
            print('Login Gagal --> %s' % (act))

    def get_token(self, url):
        req = self.xyz.get(url, cookies=self.cookie).json()
        tok = req['access_token']
        return tok
        # self.req_info_token(tok)

    def req_info_token(self, tok):
        try:
            url = 'https://developers.facebook.com/tools/debug/accesstoken/?access_token=%s&version=v16.0' % (tok)
            req = bs(self.xyz.get(url, cookies=self.cookie).content, 'html.parser')
            try:
                gtx = req.find_all('tr')[0].find_all('td')[1].text
            except Exception as e:
                gtx = 'App : Unknown'
            try:
                crf = req.find('a', href='/docs/reference/login/#permissions').text
            except Exception as e:
                print(e)
            print('')
            print(gtx)
            print(tok)
        except Exception as e:
            pass


def parseCookieRaw(cookies: str):
    result = dict()
    cookiesArr = cookies.split(";")
    cookiesArr = [cookieItem.strip() for cookieItem in cookiesArr]
    for cookieItem in cookiesArr:
        cookieItemArr = cookieItem.split("=")
        result[cookieItemArr[0]] = cookieItemArr[1]
    return result


def getFb_dtsg(cookies: str):
    cookies = parseCookieRaw(cookies)
    HEADERS_GET_FB_DTSG = {
        'authority': 'mbasic.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get('https://mbasic.facebook.com/me/', cookies=cookies, headers=HEADERS_GET_FB_DTSG)
        soup = bs(response.content, 'html.parser')
        fb_dtsg = soup.find('input', {'name': 'fb_dtsg'}).get('value')
        return fb_dtsg
    except Exception as e:
        print(e)
        return


def loadUrlFromFile(list_urls: Queue, file_name: str):
    try:
        data = open(file_name, "r", encoding="utf-8").read().split()
        _ = list(map(list_urls.put, data))
    except Exception as e:
        print(e)
        pass


def getPostIDFromUrl(cookies: str, list_urls_queue: Queue, list_id_not_delete: list):
    cookies = {'cookie': cookies}
    headers = {
        'authority': 'www.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-full-version-list': '"Not.A/Brand";v="8.0.0.0", "Chromium";v="114.0.5735.134", "Google Chrome";v="114.0.5735.134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'viewport-width': '852',
    }
    while True:
        url = list_urls_queue.get()
        print(url)
        if url is None:
            break
        else:
            with requests.Session() as ses:
                response = ses.get(url, cookies=cookies, headers=headers)
                post_id_match = re.search(r'"post_id":"(\d+)"', response.text)
                if post_id_match:
                    post_id = post_id_match.group(1)
                    list_id_not_delete.append(post_id)
                else:
                    if 'fbid' in url:
                        post_id_match = re.search(r'fbid=(\d+)', url)
                        post_id = post_id_match.group(1)
                        list_id_not_delete.append(post_id)


def getStoryIDFromUrl(cookies: dict[str], post_id: str):
    try:
        with requests.Session() as ses:
            response = ses.get(f'https://www.facebook.com/{post_id}', cookies=cookies, timeout=5)
            print(response.url)
            story_id_match = re.search(r'"storyID":"([^"]+)"', response.text)
            if story_id_match:
                story_id = story_id_match.group(1)
                return story_id
            else:
                return
    except Exception as e:
        print(e)
        pass


def getListPost(list_ids_post: Queue, cookies: str, list_id_not_delete: list):
    pre_accessToken = Token(cookies)
    accessToken = pre_accessToken.accessToken
    print('[Access Token]:: ', accessToken)
    cookies = parseCookieRaw(cookies)
    print('[Cookies]::', cookies)
    headers = {
        'authority': 'graph.facebook.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    def filterData(data):
        item = data['id'].split("_")[1]
        if item not in list_id_not_delete:
            return data['id']

    url = "https://graph.facebook.com/v2.8/me?fields=feed&limit=100"
    try:
        response = requests.get(
            'https://graph.facebook.com/v16.0/me?fields=feed.limit(999)&access_token=' + accessToken, headers=headers,
            cookies=cookies)
        resp = response.json()['feed']
        pre_list = list(map(filterData, resp['data']))
        _ = list(map(list_ids_post.put, pre_list))
    except Exception as e:
        print(e)


def removePost(cookies: str, list_ids_post: Queue, fb_dtsg: str):
    cookies = parseCookieRaw(cookies)
    headers = {
        'authority': 'www.facebook.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.facebook.com',
        'referer': 'https://www.facebook.com',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Chromium";v="103", ".Not/A)Brand";v="99"',
        'sec-ch-ua-full-version-list': '"Chromium";v="103.0.5060.134", ".Not/A)Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
        'viewport-width': '1132',
        'x-asbd-id': '129477',
        'x-fb-friendly-name': 'useCometTrashPostMutation',
        'x-fb-lsd': 'paVhHmefIHy5g8EsbMvA1c',
    }
    while True:
        time.sleep(randint(2, 4))
        idd = list_ids_post.get()
        if idd is None:
            continue
        elif idd == "Null":
            break
        else:
            story_id = getStoryIDFromUrl(cookies, idd)
            if story_id:
                data = {
                    'av': cookies['c_user'],
                    '__a': '1',
                    '__comet_req': '15',
                    'fb_dtsg': fb_dtsg,
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'useCometTrashPostMutation',
                    'variables': '{"input":{"story_id":"' + story_id + '","story_location":"TIMELINE","actor_id":"' +
                                 cookies['c_user'] + '","client_mutation_id":"1"}}',
                    'server_timestamps': 'true',
                    'doc_id': '7003056599769350',
                }
                try:
                    with requests.Session() as ses:
                        response = ses.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers,
                                            data=data)
                        print(response.text)
                except Exception as e:
                    print(e)
                    pass


def startRunApplication():
    try:
        list_id_not_delete = []
        cookies = input("Nhập cookie: ")
        file_name = 'list_link_khong_xoa.txt'
        fb_dtsg = getFb_dtsg(cookies)
        list_urls_queue = Queue()
        list_ids_post = Queue()
        thread_loadUrlFromFile = Thread(target=loadUrlFromFile, args=(list_urls_queue, file_name))
        thread_loadUrlFromFile.start()
        list_thread_getPostIdFromUrl = []
        for _ in range(3):
            thread_getPostIdFromUrl = Thread(target=getPostIDFromUrl,
                                             args=(cookies, list_urls_queue, list_id_not_delete))
            thread_getPostIdFromUrl.start()
            list_thread_getPostIdFromUrl.append(thread_getPostIdFromUrl)
        thread_loadUrlFromFile.join()
        for _ in range(len(list_thread_getPostIdFromUrl)):
            list_urls_queue.put(None)
        for thread in list_thread_getPostIdFromUrl:
            thread.join()
        getListPost(list_ids_post, cookies, list_id_not_delete)
        list_thread_remove_id = []
        for _ in range(5):
            thread_remove_id = Thread(target=removePost, args=(cookies, list_ids_post, fb_dtsg))
            thread_remove_id.start()
            list_thread_remove_id.append(thread_remove_id)
        for _ in range(len(list_thread_remove_id)):
            list_ids_post.put("Null")
        for thread in list_thread_remove_id:
            thread.join()
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    startRunApplication()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
