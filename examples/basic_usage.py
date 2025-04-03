import datetime
import json
from time import sleep
import pathlib
from playwright.sync_api import sync_playwright

from xhs import DataFetchError, XhsClient, help
from social_upload.conf import BASE_DIR, XHS_SERVER

def sign(uri, data=None, a1="", web_session=""):
    for _ in range(10):
        try:
            with sync_playwright() as playwright:
                #stealth_js_path = "/Users/reajason/ReaJason/xhs/tests/stealth.min.js"
                stealth_js_path = pathlib.Path(BASE_DIR / "utils/stealth.min.js")
                chromium = playwright.chromium

                # 如果一直失败可尝试设置成 False 让其打开浏览器，适当添加 sleep 可查看浏览器状态
                browser = chromium.launch(headless=True)

                browser_context = browser.new_context()
                browser_context.add_init_script(path=stealth_js_path)
                context_page = browser_context.new_page()
                context_page.goto("https://www.xiaohongshu.com")
                browser_context.add_cookies([
                    {'name': 'a1', 'value': a1, 'domain': ".xiaohongshu.com", 'path': "/"}]
                )
                context_page.reload()
                # 这个地方设置完浏览器 cookie 之后，如果这儿不 sleep 一下签名获取就失败了，如果经常失败请设置长一点试试
                sleep(1)
                encrypt_params = context_page.evaluate("([url, data]) => window._webmsxyw(url, data)", [uri, data])
                return {
                    "x-s": encrypt_params["X-s"],
                    "x-t": str(encrypt_params["X-t"])
                }
        except Exception:
            # 这儿有时会出现 window._webmsxyw is not a function 或未知跳转错误，因此加一个失败重试趴
            pass
    raise Exception("重试了这么多次还是无法签名成功，寄寄寄")


if __name__ == '__main__':
    cookie = "a1=1900fc12cadchoi9un6hqu7jx17vylyz1xxg0b7t650000283173;abRequestId=3fe1a21862d6cad7160412e3a0057a6a;access-token-creator.xiaohongshu.com=customer.creator.AT-68c517385895812640526852qdekjyix47b4dj9l;AMP_07c61c6ea8=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI0YzdkMDUyZi03YmQ0LTQzNDYtYWY1OS0yZjVjNTY4MTJiOTQlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE5NzUyODM1ODY1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxOTc1Mjg5OTgxMyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTYlN0Q=;AMP_MKTG_07c61c6ea8=JTdCJTdE;customer-sso-sid=68c51738589581264052684845b7b6569eb16e73;customerClientId=308942040862408;gid=yj88iSy44Kyqyj88iSyJSCDW0fSxl3j7IKxAC9K7WVCyWk28hv1vu8888JYqyWq80qiWj2dJ;loadts=1742023734737;sec_poison_id=cad11943-cf4b-4d89-a3e4-cd2bc1436427;unread={%22ub%22:%2267d415fb000000000900c544%22%2C%22ue%22:%2267d5060f000000001b03f287%22%2C%22uc%22:21};web_session=040069b4fd03d9dacced0f62e0354b50d5ffe9;webBuild=4.60.1;webId=3fe1a21862d6cad7160412e3a0057a6a;websectiga=59d3ef1e60c4aa37a7df3c23467bd46d7f1da0b1918cf335ee7f2e9e52ac04cf;x-user-id-creator.xiaohongshu.com=658940910000000022009cbb;xsecappid=xhs-pc-web;acw_tc=0a00d67e17420232149828175ef7937c62e7cae1cdc5b5a22df4a446928109;"

    xhs_client = XhsClient(cookie, sign=sign)
    print(datetime.datetime.now())

    for _ in range(1):
        # 即便上面做了重试，还是有可能会遇到签名失败的情况，重试即可
        try:
            note = xhs_client.get_note_by_id("67c1a1a7000000000603bb08","ABaudHMqRg35_gli9zPPPWHXY5qNpNG4oOteJ-ddYQKc8=")
            print(note)
            print(json.dumps(note, indent=4))
            print(help.get_imgs_url_from_note(note))
            break
        except DataFetchError as e:
            print(e)
            print("失败重试一下下")
