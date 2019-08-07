#!/usr/bin/python3

import re
import time
import random
import requests
from fake_useragent import UserAgent
import proxy

try:
    import config
except ImportError:
    class ConfigClass:
        click_depth = 10
        min_wait = 1
        max_wait = 3
        proxy_rotation = 10
        debug = True

        root_urls = [
            "espn.com"
        ]

    config = ConfigClass


def make_request(url, proxy, random_ua, session):
    global data_meter
    global good_requests
    global bad_requests

    sleep_time = random.randrange(config.min_wait, config.max_wait)

    headers = {'user-agent': random_ua}

    if config.debug:
        print(f"requesting: {url}")
        print(f"using UA: {random_ua}")
        print(f"using proxy: {proxy}")

    try:
        r = session.get(url, headers=headers, proxies=proxy, timeout=5)
    except:
        time.sleep(30)
        return False

    status = r.status_code
    page_size = len(r.content)
    data_meter = data_meter + page_size

    if config.debug:
        print(f"page size: {page_size}")
        if data_meter > 1000000:
            print(f"data meter: {data_meter / 1000000} MB")
        else:
            print(f"data meter: {data_meter} bytes")

    if status != 200:
        bad_requests += 1
        if config.debug:
            print(f"response status: {status}")
        if status == 429:
            print("we are requesting too frequently...adding to sleep time")
            sleep_time += 10
    else:
        good_requests += 1

    if config.debug:
        print(f"good requests: {good_requests}")
        print(f"bad requests: {bad_requests}")
        print(f"sleeping for {sleep_time} seconds")

    time.sleep(sleep_time)
    return r


def get_links(page):
    links = []
    pattern = r"(?:href\=\")(https?:\/\/[^\"]+)(?:\")"
    matches = re.findall(pattern, str(page.content))

    for match in matches:
        if any(bl in match for bl in config.blacklist):
            pass
        else:
            links.append(match)

    return links


def browse(urls):
    proxy_count = 1
    curr_url = 1
    proxies = proxy.get_proxy()
    current_proxy = random.choice(proxies)
    proxy_rotation = random.randrange(config.min_proxy_pages, config.max_proxy_pages)
    ua = UserAgent()
    random_ua = ua.random
    for url in urls:
        url_count = len(urls)
        session = requests.session()
        page = make_request(url, current_proxy, random_ua, session)
        proxy_count += 1
        if proxy_count > proxy_rotation:
            proxies = proxy.get_proxy()
            current_proxy = random.choice(proxies)
            ua = UserAgent()
            random_ua = ua.random
            proxy_count = 0
            if config.debug:
                print("fetching new proxies and ua's...")
        if page:
            links = get_links(page)
            link_count = len(links)
        else:
            if config.debug:
                print(f"error requesting {url}")
            continue
        depth = 0
        while depth < config.click_depth:
            if len(links) > 1:
                if proxy_count > proxy_rotation:
                    ua = UserAgent()
                    random_ua = ua.random
                    proxies = proxy.get_proxy()
                    current_proxy = random.choice(proxies)
                    proxy_count = 0
                    if config.debug:
                        print("fetching new proxies and ua's...")
                random_link = random.randrange(0, link_count-1)
                if config.debug:
                    print(f"URL: {curr_url} / {url_count} -- depth: {depth} / {config.click_depth}")
                    print(f"choosing random url from total: {link_count}")
                    print(f"we have made {proxy_count} requests with this proxy")
                try:
                    click_link = links[random_link]
                except IndexError:
                    link_count -= 1
                    random_link = random.randrange(0, link_count-1)
                    click_link = links[random_link]
                if config.debug:
                    print(f"link chosen: {random_link} of {link_count}")
                try:
                    session = requests.session()
                    sub_page = make_request(click_link, current_proxy, random_ua, session)
                    links = get_links(sub_page)
                    link_count = len(links)
                    proxy_count += 1
                    if sub_page:
                        check_link_count = len(get_links(sub_page))
                    else:
                        if config.debug:
                            print(f"error requesting {url}")
                        break
                    if check_link_count > 1:
                        links = get_links(sub_page)
                    else:
                        if config.debug:
                            print(f"not enough links found... found {check_link_count}, going back up a level")
                        config.blacklist.append(click_link)
                except:
                    if config.debug:
                        print(f"exception on URL: {click_link}, removing from list and trying again")
                        config.blacklist.append(click_link)
                        pass
                depth += 1
            else:
                if config.debug:
                    print("hit a dead end, moving to the next root url...")
                config.blacklist.append(click_link)
                depth = config.click_depth
        curr_url +=1
        print('\n')
    if config.debug:
        print("done...")

data_meter = 0
good_requests = 0
bad_requests = 0
