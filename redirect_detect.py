#!/usr/bin/env python3

from time import time
import requests
import ssl

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class TLSv1(requests.adapters.HTTPAdapter):
    """
    A TransportAdapter that re-enables TLSv1 support in Requests.
    """
    def init_poolmanager(self, *args, **kwargs):
        context = requests.packages.urllib3.util.ssl_.create_urllib3_context(ssl_version=ssl.PROTOCOL_TLSv1)
        kwargs['ssl_context'] = context
        return super(TLSv1, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = requests.packages.urllib3.util.ssl_.create_urllib3_context(ssl_version=ssl.PROTOCOL_TLSv1)
        kwargs['ssl_context'] = context
        return super(TLSv1, self).proxy_manager_for(*args, **kwargs)


start_time = time()

urls = ['url1.com', 'url2.com']

for url in urls:
    try:
        url = 'https://' + url
        s = requests.Session()
        s.mount(url, TLSv1())
        response = s.head(url, timeout=10, verify=False)
        if response.is_redirect:
            if "page=948" in response.headers["Location"]:
                print(f'{url} redirected to {url}{response.headers["Location"]}')
            else:
                print(f'{url} redirected to {response.headers["Location"]}')
        else:
            print(f"Request was not redirected for {url}")
    except requests.ConnectTimeout:
        print(f'Request timed out for {url}')
        continue
    except requests.ConnectionError as something_happened:
        print(f'Connection aborted for {url} due to ', end='')
        if "doesn't match either of" in str(something_happened):
            print('certificate mismatch!')
        else:
            print(something_happened)
            continue


end_time = time()

print(f'Completed in {round(end_time-start_time)} seconds!')
