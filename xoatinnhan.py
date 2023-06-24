import time

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service


def parseCookieRaw(cookies: str):
    result = dict()
    cookiesArr = cookies.split(";")
    cookiesArr = [cookieItem.strip() for cookieItem in cookiesArr]
    for cookieItem in cookiesArr:
        cookieItemArr = cookieItem.split("=")
        result[cookieItemArr[0]] = cookieItemArr[1]
    return result


cookie_raw = input("Xin mời ngài nhập cookie:: ")
time_delay = int(input("Xin mời ngày nhập thời gian delay (> 1 giây):: "))
service_object = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service_object, options=options)
driver.get("https://mbasic.facebook.com")
cookies = parseCookieRaw(cookie_raw)
for key, value in cookies.items():
    driver.add_cookie({"name": key, "value": value, "domain": ".facebook.com"})
driver.refresh()
driver.get("https://mbasic.facebook.com/messages")
script_get_link_delete = '''
var section = document.querySelector('section');
var table = section.querySelector('table');
var a = table.querySelector("a");
var href = a.href;
return href;
'''
count = 0
while 1:
    time.sleep(time_delay)
    try:
        result = driver.execute_script(script_get_link_delete)
        print(result)
        if result is not None:
            driver.get(result)
            btn_delete = driver.find_element("name", "delete")
            if btn_delete:
                btn_delete.click()
                script_delete = '''
                var elements = document.getElementById('root').querySelectorAll('a');
                var hrefs = [];
                elements.forEach(function(a) {
                    hrefs.push(a.href);
                });
                return hrefs;
                '''
                hrefs = driver.execute_script(script_delete)
                if len(hrefs) == 2:
                    count += 1
                    driver.get(hrefs[-1])
                    print(f"Đã xoá được {count} tin nhắn, thời gian delay là {time_delay} giây giữa mỗi lần xoá")
    except Exception as e:
        print("Inbox đã trống")
        break
driver.close()
driver.quit()
input("Nhấn Enter để thoát...")