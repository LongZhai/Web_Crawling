from urllib.parse import urlparse


# Get domain name (google.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        if len(results) >= 2:
            return results[-2] + '.' + results[-1]
    except Exception as e:
        print(str(e))
    return ''


# Get sub domain name (map.google.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except Exception as e:
        print(str(e))
        return None
