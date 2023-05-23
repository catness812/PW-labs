from flask import Flask
from flask import request
from flask import Response
import requests
import json
import random
import sqlite3

with open('token.json') as t:
    data = json.load(t)

conn = sqlite3.connect("news.sqlite", check_same_thread=False)

TOKEN = data['token']
app = Flask("Pusheen News")


def analyze_msg(mess):
    try:
        chat_id = mess['message']['chat']['id']
        try:
            msg = mess['message']['text'].lower()
            if msg == "/start" or msg == "hi" or msg == "hello":
                start(chat_id)
            elif msg == "/help":
                help(chat_id)
            elif msg.startswith("/latest_news"):
                if msg == "/latest_news":
                    latest_news(chat_id)
                    send_msg(chat_id, "If you want to specify the topic, please use the '/latest_news topic' command.")
                else:
                    str = msg.split()
                    if str and str[0] == "/latest_news":
                        str.remove("/latest_news")
                        topic = '+'.join(str)
                        latest_news_topic(chat_id, topic)
                    else:
                        undefined(chat_id)
                        print(mess['message'])
            elif msg.startswith("/save_news"):
                if msg == "/save_news":
                    send_msg(chat_id, "Please use the '/save_news URL' command to save news links (one at a time).")
                else:
                    str = msg.split()
                    if str and str[0] == "/save_news" and len(str) == 2:
                        str.remove("/save_news")
                        url = ''.join(str)
                        save_news(chat_id, url)
                    else:
                        undefined(chat_id)
                        print(mess['message'])
            elif msg == "/saved_news":
                saved_news(chat_id)
            elif msg.startswith("/delete_news"):
                if msg == "/delete_news":
                    send_msg(chat_id, "Please use the '/delete_news URL' command to delete any of the saved news links (one at a time).")
                else:
                    str = msg.split()
                    if str and str[0] == "/delete_news":
                        str.remove("/delete_news")
                        url = ''.join(str)
                        delete_news(chat_id, url)
                    else:
                        undefined(chat_id)
                        print(mess['message'])
            elif msg == "/empty_news":
                empty_news(chat_id)
            elif msg.startswith("/meow"):
                if msg == "/meow":
                    random_cat(chat_id)
                    send_msg(chat_id, "Try the '/meow gif' or '/meow *anything*' for additional surprises :3")
                else:
                    str = msg.split()
                    if str and str[0] == "/meow":
                        str.remove("/meow")
                        if len(str) == 1 and str[0] == "gif":
                            random_cat_gif(chat_id)
                        else:
                            says = '+'.join(str)
                            random_cat_topic(chat_id, says)
                    else:
                        undefined(chat_id)
                        print(mess['message'])
            elif msg == "meow":
                random_cat(chat_id)
                send_msg(chat_id, "Try the '/meow gif' or '/meow *anything*' for additional surprises :3")
            else:
                undefined(chat_id)
                print(mess['message'])
        except:
            try:
                msg = mess['message']['sticker']
                pusheen_stickers = ['CAACAgIAAxkBAAEJEglkbLtikPQIfSsF65HMNdvk5BqThgACyhEAAujW4hKY0PnLoDrRBC8E', 'CAACAgIAAxkBAAEJEgtkbLtkE4t-tH1GVuSt2qE420UagAACyxEAAujW4hKpHJgOixD0uC8E', 'CAACAgIAAxkBAAEJEg1kbLtlLAj1OfDIOX7qQ5BlBrC3FAACzBEAAujW4hJwH3b5eukemS8E', 'CAACAgIAAxkBAAEJEg9kbLtnNeOyrDOAoZ0by2X-uDcQIQACzREAAujW4hLhXiK1MUBxAS8E', 'CAACAgIAAxkBAAEJEhFkbLtoraXY9-FHfuEKOI-CYgTBewACzhEAAujW4hJmKxJbFCMZcS8E', 'CAACAgIAAxkBAAEJEhNkbLtqZYdcx6x-Jf3xEbWMD1wKxAACzxEAAujW4hKuoO8QqR8Q5S8E', 'CAACAgIAAxkBAAEJEhVkbLtsQZzlvghaUVParwuAUgQ1lwAC0BEAAujW4hKe372xPmCETi8E', 'CAACAgIAAxkBAAEJEhdkbLtt7_kKzSh3RZOkVSvkqBplagAC0REAAujW4hJU_U2Shi92cy8E', 'CAACAgIAAxkBAAEJEhlkbLtvFZ7dzV1n6rmbVPZ0JNlbJgAC1REAAujW4hL56NbVY7lgmS8E', 'CAACAgIAAxkBAAEJEhtkbLtwapEtqfaLQaiio-LqNP4YVwAC1BEAAujW4hL5KUDmDZX15C8E', 'CAACAgIAAxkBAAEJEh1kbLt0qb2CvWETyjHQNcseOb5DBQAC1hEAAujW4hIzcmCXWHyWoS8E', 'CAACAgIAAxkBAAEJEh5kbLt0qK-SlZAfKjk9rYKays5YlwAC1xEAAujW4hKOHStXURFdzS8E', 'CAACAgIAAxkBAAEJEiFkbLt4NvrHDKYJ-99Z0Mm0hf00AAPYEQAC6NbiEqvx_lM5P0LZLwQ', 'CAACAgIAAxkBAAEJEiJkbLt5wI0Eg-x4R4TP59E2flekEQAC2REAAujW4hLwFijxt0KtrS8E', 'CAACAgIAAxkBAAEJEiRkbLt5BrqWkfWw3q4cLz0QoL3RpQAC2hEAAujW4hIrI0h9LHijJy8E', 'CAACAgIAAxkBAAEJEiZkbLt6Pox46N8O84pmlJEEz_jpswAC2xEAAujW4hK9oD2AQRI81S8E', 'CAACAgIAAxkBAAEJEihkbLt726gUZ2bU4d1i8GIq1N4lQAAC3BEAAujW4hJvMX-Al8HuQC8E', 'CAACAgIAAxkBAAEJEilkbLt7x1vw-S0HAAGX-XIHCQe-mQ4AAt0RAALo1uISNaYkTh9wfG0vBA', 'CAACAgIAAxkBAAEJEitkbLt8ou89scFyGwXTt7KU7bYc7gAC3hEAAujW4hIUbP51wtnOoC8E', 'CAACAgIAAxkBAAEJEi1kbLt9R7uh_8EeDxBKhIZY8uH0SwAC3xEAAujW4hJB0UcYM2OULy8E', 'CAACAgIAAxkBAAEJEi9kbLt-J3fvJdke99Tme9zAiMtaXAAC4BEAAujW4hKpixDW96C-eS8E', 'CAACAgIAAxkBAAEJEjFkbLt-r2BZFr8I-UfEKMXpgRKHBQAC4REAAujW4hL7vW7JNsnFtS8E', 'CAACAgIAAxkBAAEJEjJkbLt_kRrKJqNqthbbZFVhmTcPHQAC4hEAAujW4hI4qhcWJCa_Bi8E', 'CAACAgIAAxkBAAEJEjRkbLuAy-DFPiGYhk-MnTNuXrT9WwAC6REAAujW4hJoWkkVJx3VcS8E', 'CAACAgIAAxkBAAEJEjZkbLuAEGccace3R78lvm48eitYfgAC4xEAAujW4hJHbq9sFsh4_y8E', 'CAACAgIAAxkBAAEJEjhkbLuBkZWcr3LeBtL9G0JDdf8qlAAC5BEAAujW4hJvrEkZarHNPy8E', 'CAACAgIAAxkBAAEJEjlkbLuCpEQxF73Nxmdzhsir3EWEOQAC5REAAujW4hKAjP6IqJAoXC8E', 'CAACAgIAAxkBAAEJEjtkbLuCh_CigzCtjxXA0s1xxbLm0wAC5hEAAujW4hLRAhYqGhA3oC8E', 'CAACAgIAAxkBAAEJEj1kbLuDg1cfnJ2hV6TXxmLqwAOUxAAC5xEAAujW4hJJHy2ZUgQooS8E', 'CAACAgIAAxkBAAEJEj5kbLuEpH2WRaak3ahJ1mOOjOyYeAAC6BEAAujW4hKf5jp1J02B9S8E', 'CAACAgIAAxkBAAEJEkBkbLuEnhSS-opbYL08AVZMr096uAAC6hEAAujW4hLBZ1149_EtES8E', 'CAACAgIAAxkBAAEJEkJkbLuFYJw0uWMgzQ1I7Fcz_KB3SQAC6xEAAujW4hIwEd_gxON7By8E', 'CAACAgIAAxkBAAEJEkNkbLuFVLhyiyMtJlEyNLiOfVieDAAC7BEAAujW4hILliJTOnlVrS8E', 'CAACAgIAAxkBAAEJEkVkbLuGWdQ0Tk-p5B0_8OrkQ80MFwAC7REAAujW4hLSW1ocHAABnFMvBA', 'CAACAgIAAxkBAAEJEkZkbLuHDzsu-NG5S4eqMLpq3kVdvgAC7hEAAujW4hLU2DB8yZ0kuS8E', 'CAACAgIAAxkBAAEJEkhkbLuHqRL9GmDtNRND6AHXT2tpjAAC7xEAAujW4hLGSAABUhm7_xYvBA', 'CAACAgIAAxkBAAEJEkpkbLuIrB43cXvJlfUD94jk4SZIswAC8BEAAujW4hKlk9KJHLy_qC8E', 'CAACAgIAAxkBAAEJEktkbLuIIwsMbmnqCq5Wsg8_rKsbxwAC8REAAujW4hLP0wm7pLxHiS8E', 'CAACAgIAAxkBAAEJEk1kbLuJmoEByegNNzlGuZ4xZw3Q_wAC8hEAAujW4hI_N1CBYelpVC8E', 'CAACAgIAAxkBAAEJEk5kbLuJK6cFOH7KeC7s6Oa60DPKFAAC8xEAAujW4hI8ISjPBNl0wi8E', 'CAACAgIAAxkBAAEJElBkbLuKgtTPkRPoRP5sEgH1Mi6R4wAC9BEAAujW4hKPgyPuHFKEYC8E', 'CAACAgIAAxkBAAEJElJkbLuKQnGChFEZkHqRAAHrNbXRyUgAAvURAALo1uIS-PU2_bl6rOsvBA', 'CAACAgIAAxkBAAEJElNkbLuLyYgvAen3ZcT5ZDbli9L4vQAC9hEAAujW4hLqwWatxumAyC8E', 'CAACAgIAAxkBAAEJElVkbLuL9wXe0alKDOFj3f0-4EQhOgAC9xEAAujW4hJmdUN_pHKUYC8E', 'CAACAgIAAxkBAAEJElZkbLuMg43yF6nSojMxi5eH8Xu-3wAC-BEAAujW4hJETlgAAdqyPYwvBA', 'CAACAgIAAxkBAAEJElhkbLuNrkS5mZH0jD5p_R30ynkjvQAC-REAAujW4hKtUYHMpWII1i8E', 'CAACAgIAAxkBAAEJEllkbLuNwemXONbCgJ5xrg9pROZfbwAC-hEAAujW4hLNXzQsr6ltWi8E', 'CAACAgIAAxkBAAEJEltkbLuNO1o8sIW83tBJLRXA5XSJkAAC-xEAAujW4hJflXw9P-2kjy8E', 'CAACAgIAAxkBAAEJElxkbLuO1umOcUeNIGHqc3Sit6FimQAC_BEAAujW4hJI69X1WPFFxi8E', 'CAACAgIAAxkBAAEJEl5kbLuOYMBcr-Nn0k0mbIqyHFbf1gAC_REAAujW4hJpwCS9ur8mDy8E', 'CAACAgIAAxkBAAEJEmdkbLuWMQRgRrQsS7gKX-hbPWxJMQAC_hEAAujW4hKfsOCBU4riuS8E', 'CAACAgIAAxkBAAEJEnFkbLunwX7pMMspgyJnygWa6a_CAwAC_xEAAujW4hJG4Oa36C4iSy8E', 'CAACAgIAAxkBAAEJEnNkbLuu6V57jfga-4S6IpvRNubLWAADEgAC6NbiEq45hOKK769eLwQ', 'CAACAgIAAxkBAAEJEnVkbLuwTfX3rEBgurzsGMYoTwIqUAACARIAAujW4hKeeiqBUGUzTC8E', 'CAACAgIAAxkBAAEJEndkbLuxCKzTHCu8sH7N2TDclbQbBAACAhIAAujW4hKCzVzMemZd-y8E', 'CAACAgIAAxkBAAEJEnlkbLuyCG6H58NtUKazYPcm10BCfwACAxIAAujW4hJS8YTL-Ct8KC8E', 'CAACAgIAAxkBAAEJEnpkbLuzUXleD23vF-erCRFnqlAdRgACBBIAAujW4hKVTwjzTR08aS8E', 'CAACAgIAAxkBAAEJEnxkbLuz7sHyjgMuqQEr5rnLn_28rgACBRIAAujW4hKU-p4lq21bZy8E', 'CAACAgIAAxkBAAEJEn1kbLu0hcf6Vnv7pxnmIfxrrdEPPAACBhIAAujW4hLecevMx8GTbC8E', 'CAACAgIAAxkBAAEJEn9kbLu0Xy-zCwrufQli_16y1Pq-GQACBxIAAujW4hKBSH4HZ4SGpS8E', 'CAACAgIAAxkBAAEJEoFkbLu1MRBPsgNi0aXbI2bsPoA3JgACCBIAAujW4hLq843iNsxvnC8E', 'CAACAgIAAxkBAAEJEoJkbLu1G2gHOULfdtfhHhTk_zTqJQACCRIAAujW4hIWHOr-cM0m9S8E', 'CAACAgIAAxkBAAEJEoRkbLu2Rg0p5_t2-OQLIcngzm-MugACChIAAujW4hJs5BtKttBIGS8E', 'CAACAgIAAxkBAAEJEoVkbLu2mcpXSmXMoREPaZv2M6pmcwACCxIAAujW4hJabhT_YQABjZ8vBA', 'CAACAgIAAxkBAAEJEodkbLu3kNczRnmKBRqJhoZVX0BoQAACDBIAAujW4hJmWgISjNkQ0i8E', 'CAACAgIAAxkBAAEJEohkbLu3iBlGR9jXUCufEJ2LoYx6nQACIhIAAujW4hI2uqloM5rL2i8E', 'CAACAgIAAxkBAAEJEopkbLu4HVsF8zbQ0RkRN90uQaf8kwACIxIAAujW4hKmNWA9_qLUQi8E', 'CAACAgIAAxkBAAEJEotkbLu4f7pKVB2wsaop70FnSBOMWQACJBIAAujW4hICpChNDNy89i8E', 'CAACAgIAAxkBAAEJEo1kbLu5DrkSOn85T7OGl4Ba9cOFGAACJRIAAujW4hL6OZMjAmw6Dy8E', 'CAACAgIAAxkBAAEJEo5kbLu5nw8l-tlnMNkCfeANEuJe5wACJhIAAujW4hJPIxvSx4KXmS8E', 'CAACAgIAAxkBAAEJEpBkbLu6t7fefSGrN4BXxmBdqknGGAACJxIAAujW4hIsJIOcoUjdOS8E', 'CAACAgIAAxkBAAEJEpFkbLu6DJRLdOCSt71D32WxFJe7VgACKBIAAujW4hIie9vZ5zY1mC8E', 'CAACAgIAAxkBAAEJEpNkbLu6QoBGwE1gZs7kCDiH69oOvQACKRIAAujW4hLvNjyFA0pwsi8E', 'CAACAgIAAxkBAAEJEpRkbLu7nZB-cBFZ_E0U6SMBMhfkcAACKhIAAujW4hIYiKfZQSKzLC8E', 'CAACAgIAAxkBAAEJEplkbLu_XDvvA4ftChy8Ev39N3OhCgACKxIAAujW4hIZCXsGD_k8kS8E', 'CAACAgIAAxkBAAEJEpxkbLvBzl901fJKOSVYuKR3h5l8PgACRxIAAujW4hKwSYMk0QqfVy8E', 'CAACAgIAAxkBAAEJEp5kbLvBIF_31yXC-H-y7EUhwVduwQACSBIAAujW4hK7HT1JLpiONS8E', 'CAACAgIAAxkBAAEJEqBkbLvCxXfATHh-EZtORJ7ZW_Gr3gACSRIAAujW4hIxz5Lgt9Ephy8E', 'CAACAgIAAxkBAAEJEqJkbLvDnv6iqlfQzUtftWstY8g0_QACShIAAujW4hJ12yTcSs3mZy8E', 'CAACAgIAAxkBAAEJEqNkbLvDvipUrBmXeDa1UKKtTG2emQACSxIAAujW4hJP8u1NFgW2ly8E', 'CAACAgIAAxkBAAEJEqVkbLvE40djrk8M2YiCGIX5bIhpFQACTBIAAujW4hLXojsRH7XPoC8E', 'CAACAgIAAxkBAAEJEqZkbLvEdvtxehScSuuRyYLOHFhU-AACTRIAAujW4hL5eY-zZfpXEC8E', 'CAACAgIAAxkBAAEJEqhkbLvFhu-XNOUAAblnYUYQKz9cFCkAAk4SAALo1uIS_wvvHMRoVSUvBA', 'CAACAgIAAxkBAAEJEqlkbLvFZU8OEkOP_napvwQ03xjaIQACTxIAAujW4hLYE_bQm9WjRy8E', 'CAACAgIAAxkBAAEJEqtkbLvGHP4TsKGOJftVKJcezde-_wACUBIAAujW4hIw8ZqemhHBTi8E', 'CAACAgIAAxkBAAEJEq1kbLvG2qhSGND1kf93NuryRJu-PQACURIAAujW4hKQt6rKNJ9WpC8E', 'CAACAgIAAxkBAAEJEq5kbLvHcqKCBV7bxwyFf9QYQBELQQACUhIAAujW4hLvfjIuj2fRpy8E', 'CAACAgIAAxkBAAEJErBkbLvHUUZrm9vuytsXr-f7BYjndwACUxIAAujW4hJqAw5ywXrkJy8E', 'CAACAgIAAxkBAAEJErFkbLvIn9rE4GN77t1TmMLV5ZIfsAACVBIAAujW4hLhkx2XFvE-gS8E', 'CAACAgIAAxkBAAEJErNkbLvIwf0sSYIWglBHi88e3xU2RgACVRIAAujW4hKPkpvAFhZvKS8E']
                send_sticker(chat_id, random.choice(pusheen_stickers))
            except:
                try:
                    msg = mess['message']['document']
                    gifs = ['CgACAgQAAxkBAAIBT2RssRxTsUv7FEfUj-aWTl2VxbnBAAIiAwACScENU66PDkVa8A0dLwQ', 'CgACAgQAAxkBAAIBX2RssykQSZ2ewwABSFnYRjcAAf5567wAAvACAAKd8g1TAvP_5ICL52EvBA', 'CgACAgQAAxkBAAIBbmRstE70YlpYe6OE0bJ1m6ZIqHdMAAL6AgACIswMUwzwuQ1hJoTELwQ', 'CgACAgQAAxkBAAIBXWRssxXhUFnJAAEEcp_W5yKQrgm_zgAC-QIAAnprHVN-xe-40v7ZbC8E', 'CgACAgQAAxkBAAIBbWRstDp2PcBCzEh4_Wo9GGf4RqI7AALfAgACdGQNU9NpMs9A3-_GLwQ', 'CgACAgQAAxkBAAIBh2Rstu6BFj2MHN1bR5LUdG8dNFHQAAI2AwAC0m0NU2IEjJcsPHPQLwQ']
                    send_animation(chat_id, random.choice(gifs))
                except:
                    stickers = ['CAACAgIAAxkBAAEJEflkbLYeSiEhIjYd9s15417uhvVztwACJRIAAujW4hL6OZMjAmw6Dy8E', 'CAACAgIAAxkBAAEJEftkbLYtful9uXJk6ynEPGJ3i9KuPAACJBIAAujW4hICpChNDNy89i8E', 'CAACAgIAAxkBAAEJEf1kbLY6pGzOg8EksdNzNT1zp30BAQACIhIAAujW4hI2uqloM5rL2i8E', 'CAACAgIAAxkBAAEJEgFkbLZgWlOphyWUPlJLdhfgsaxnTwAC5REAAujW4hKAjP6IqJAoXC8E', 'CAACAgIAAxkBAAEJEf9kbLZLLYv8d-_daYiT6P_wpK-ufAACIgADXQWCFtBPvQdMawHcLwQ', 'CAACAgIAAxkBAAEJEgNkbLa7BclccS1n9ARiXdyo6BCIgQACSwADXQWCFtSLidr3e83ALwQ']
                    send_sticker(chat_id, random.choice(stickers))
                    print(mess['message'])
        print(mess['message'])
    except:
        try:
            msg = mess['callback_query']['data']
            chat_id = mess['callback_query']['message']['chat']['id']
            if msg == "help":
                help(chat_id)
            elif msg == "latest_news":
                latest_news(chat_id)
                send_msg(chat_id, "If you want to specify the topic, please use the '/latest_news topic' command.")
            elif msg == "save_news":
                send_msg(chat_id, "Please use the '/save_news URL' command to save news links (one at a time).")
            elif msg == "saved_news":
                saved_news(chat_id)
            elif msg == "delete_news":
                send_msg(chat_id, "Please use the '/delete_news URL' command to delete any of the saved news links (one at a time).")
            elif msg == "empty_news":
                empty_news(chat_id)
            elif msg == "meow":
                random_cat(chat_id)
                send_msg(chat_id, "Try the '/meow gif' or '/meow *anything*' for additional surprises :3")
        except:
            undefined(chat_id)
            print(mess['message'])


def send_msg(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    r = requests.post(url, json=payload)
    return r


def send_sticker(chat_id, sticker):
    url = f'https://api.telegram.org/bot{TOKEN}/sendSticker'
    payload = {
        'chat_id': chat_id,
        'sticker': sticker
    }
    r = requests.post(url, json=payload)
    return r


def send_animation(chat_id, animation):
    url = f'https://api.telegram.org/bot{TOKEN}/sendAnimation'
    payload = {
        'chat_id': chat_id,
        'animation': animation
    }
    r = requests.post(url, json=payload)
    return r


def send_photo(chat_id, photo):
    url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
    payload = {
        'chat_id': chat_id,
        'photo': photo,
        'caption': 'meow'
    }
    r = requests.post(url, json=payload)
    return r


def start(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Meow!🐾\nPusheen here, your paw-some news reporter! Try the help button to see what I can do for you!",
        'reply_markup': {
            "inline_keyboard": [
                [
                    {
                        "text": "help",
                        "callback_data": "help"
                    }
                ]
            ]
        }
    }
    r = requests.post(url, json=payload)
    sticker = 'CAACAgIAAxkBAAOSZFwYVArBWyLrd7PTX4u-PWugklQAAvURAALo1uIS-PU2_bl6rOsvBA'
    send_sticker(chat_id, sticker)
    return r


def help(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Below you can find some shortcuts for the commands I can provide. Make sure to check the available menu for more details.",
        'reply_markup': {
            "inline_keyboard": [
                [
                    {
                        "text": "see the latest news worldwide or on some topic",
                        "callback_data": "latest_news"
                    }
                ],
                [
                    {
                        "text": "save a piece of news",
                        "callback_data": "save_news"
                    }
                ],
                [
                    {
                        "text": "show saved news",
                        "callback_data": "saved_news"
                    }
                ],
                [
                    {
                        "text": "delete an URL of choice",
                        "callback_data": "delete_news"
                    }
                ],
                [
                    {
                        "text": "delete all saved URLs",
                        "callback_data": "empty_news"
                    }
                ],
                [
                    {
                        "text": "meow",
                        "callback_data": "meow"
                    }
                ]
            ]
        }
    }
    r = requests.post(url, json=payload)
    sticker = 'CAACAgIAAxkBAAIH1WRtGBTawQV17-_QJqkuLGEm5-dzAAIGEgAC6NbiEt5x68zHwZNsLwQ'
    send_sticker(chat_id, sticker)
    return r


def latest_news(chat_id):
    url = ('https://newsapi.org/v2/everything?q=worldwide&sortBy=publishedAt&pageSize=5&apiKey=4417aadf78704d1a9b08a3306b716b21')
    response = requests.get(url)
    body = response.json()
    if body['status'] == 'ok':
        articles = body["articles"]
        for index, article in enumerate(articles, start=1):
            title = article["title"]
            news_url = article["url"]
            send_msg(chat_id, f"{index}. {title}\n{news_url}")
        random_cat(chat_id)
    else:
        undefined(chat_id)


def latest_news_topic(chat_id, topic):
    url = f'https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&pageSize=5&apiKey=4417aadf78704d1a9b08a3306b716b21'
    response = requests.get(url)
    body = response.json()
    if body['status'] == 'ok':
        articles = body["articles"]
        if len(articles) != 0:
            result = []
            for index, article in enumerate(articles, start=1):
                title = article["title"]
                news_url = article["url"]
                result.append(f"{index}. {title}\n{news_url}")
            for el in result:
                send_msg(chat_id, el)
            random_cat_topic(chat_id, topic)
        else:
            send_msg(chat_id, "Oh no, I couldn't find anything on that topic (= ＴェＴ=)")
            send_animation(chat_id, "CgACAgQAAxkBAAIDG2Rs2bSxTRblooT9LwIpvpuZEUL8AAJpAwACJNMEUyvWy9BcfvqYLwQ")
    else:
        undefined(chat_id)


def random_cat(chat_id):
    url = ('https://cataas.com/cat?json=true')
    response = requests.get(url).json()
    cat_url = response['url']
    send_photo(chat_id, 'https://cataas.com' + cat_url)


def random_cat_topic(chat_id, topic):
    topic = topic.replace("+", "%20")
    url = f'https://cataas.com/cat/says/{topic}?json=true'
    response = requests.get(url).json()
    cat_url = response['url']
    send_photo(chat_id, 'https://cataas.com' + cat_url)


def random_cat_gif(chat_id):
    url = ('https://cataas.com/cat/gif?json=true')
    response = requests.get(url).json()
    cat_url = response['url']
    send_animation(chat_id, 'https://cataas.com' + cat_url)


def save_news(chat_id, url):
    repeated = False
    try:
        response = requests.get(url)
        if response.status_code == 200:
            items = get_items(chat_id)
            for i in items:
                if url == i:
                    repeated = True
                    break
            if repeated == False:
                try:
                    add_item(url, chat_id)
                    send_msg(chat_id, "The link was successfully saved! Try '/saved_news' to see what other news you've got saved!")
                except:
                    send_msg(chat_id, "Oh no, there was an error while inserting data into the database (= ＴェＴ=)")
            else:
                send_msg(chat_id, "You already have this link saved! Check it under '/saved_news'")
        else:
            send_msg(chat_id, "Oh no, there was an error (= ＴェＴ=)")
    except requests.exceptions.RequestException:
        send_msg(chat_id, "Oh no, this is not a valid URL (= ＴェＴ=)")


def saved_news(chat_id):
    items = get_items(chat_id)
    if len(items) != 0:
        send_msg(chat_id, "Here are all the news links you currently have saved:")
        for index, item in enumerate(items, start=1):
            send_msg(chat_id, f"{index}. {item}")
        random_cat_gif(chat_id)
        send_msg(chat_id, f"Maybe you'd like to read this one:\n{random.choice(items)}")
    else:
        send_msg(chat_id, "Pretty empty here...")
        gif = 'CgACAgQAAxkBAAIHZWRtCC4X3ZwAATeW_TZAN6C2kSAhxgACIAMAAozKFFMvzrAnJvONpS8E'
        send_animation(chat_id, gif)


def delete_news(chat_id, url):
    found = False
    try:
        response = requests.get(url)
        if response.status_code == 200:
            items = get_items(chat_id)
            for i in items:
                if url == i:
                    found = True
                    break
            if found == True:
                try:
                    delete_item(url, chat_id)
                    send_msg(chat_id, "The link was successfully deleted.")
                except:
                    send_msg(chat_id, "Oh no, there was an error while deleting data from the database (= ＴェＴ=)")
            else:
                send_msg(chat_id, "You didn't have this linked saved.")
        else:
            send_msg(chat_id, "Oh no, there was an error (= ＴェＴ=)")
    except requests.exceptions.RequestException:
        send_msg(chat_id, "Oh no, this is not a valid URL (= ＴェＴ=)")


def empty_news(chat_id):
    try:
        empty_table(chat_id)
        send_msg(chat_id, "Data successfully deleted.")
    except:
        send_msg(chat_id, "Oh no, there was an error while deleting data from the database (= ＴェＴ=)")
    

def add_item(url, owner):
    stmt = "INSERT INTO items (url, owner) VALUES (?, ?)"
    args = (url, owner)
    conn.execute(stmt, args)
    conn.commit()


def delete_item(url, owner):
    stmt = "DELETE FROM items WHERE url = (?) AND owner = (?)"
    args = (url, owner )
    conn.execute(stmt, args)
    conn.commit()


def empty_table(owner):
    stmt = "DELETE FROM items WHERE owner = (?)"
    args = (owner, )
    conn.execute(stmt, args)
    conn.commit()


def get_items(owner):
    stmt = "SELECT url FROM items WHERE owner = (?)"
    args = (owner, )
    return [x[0] for x in conn.execute(stmt, args)]


def undefined(chat_id):
    sticker = 'CAACAgIAAxkBAAIBD2RjNPu2dWUOCzLYSS3u7gW1xE8SAALzEQAC6NbiEjwhKM8E2XTCLwQ'
    send_sticker(chat_id, sticker)
    send_msg(chat_id, 'Sorry, this is not something I can help you with (= ＴェＴ=)')


@app.route('/', methods=['GET', 'POST'])
def index():
    tblstmt = "CREATE TABLE IF NOT EXISTS items (url text, owner text)"
    itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (url ASC)" 
    ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
    conn.execute(tblstmt)
    conn.execute(itemidx)
    conn.execute(ownidx)
    conn.commit()
    if request.method == 'POST':
        msg = request.get_json()
        analyze_msg(msg)
        return Response('ok', status=200)
    else:
        return '<a href="https://t.me/faf201_patricia_capitan_bot">Pusheen News</a>'
    

app.run(debug=True)
