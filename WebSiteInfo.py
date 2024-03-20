import requests
from bs4 import BeautifulSoup
import ipaddress
from urllib.parse import urlparse
import beian


def get_external_links(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'Referer': 'https://www.baidu.com/'
    }
    # 发送请求并获取网页内容
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=3)
        if response.status_code != 200:
            return []
    except:
        return []
    # 使用 BeautifulSoup 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取所有链接
    links = soup.find_all('a', href=True)

    # 过滤外链
    external_links = []
    for link in links:
        href = link['href']
        # 判断是否是外链
        if is_external_link(href):
            external_links.append(href)

    return external_links


def is_external_link(href):
    # 忽略锚链接
    if href.startswith('#'):
        return False

    # 忽略javascript链接
    if href.startswith('javascript:'):
        return False

    # 判断是否以http或https开头
    if not href.startswith('http://') and not href.startswith('https://'):
        return False

    return True


def filter_external_links(extern_links, url):
    result = {
        'url_subdomain': set(),
        'subdomain': set(),
        'url_ip': set(),
        'ip': set(),
    }

    for link in extern_links:
        # 判断链接类型
        if is_ip_address(link):
            # IP 地址
            result['url_ip'].add(link)
            result['ip'].add(urlparse(link).hostname)
        else:
            # 域名
            # 判断link是否包含login或admin关键字
            if 'login' in link.lower() or 'admin' in link.lower() or 'sign' in link.lower() or 'auth' in link.lower():
                result['url_subdomain'].add(link)
            # 判断是否与输入 URL 具有相同主域名
            domain = urlparse(link).hostname
            if is_same_subdomain(domain, urlparse(url).hostname):
                result['url_subdomain'].add(link)
                result['subdomain'].add(domain)
            else:
                # 判断是否同备案（需要根据实际情况实现）
                if is_recorded(domain, urlparse(url).hostname):
                    result['url_subdomain'].add(link)
                    result['subdomain'].add(domain)
    return {key: list(value) for key, value in result.items()}


def is_ip_address(link):
    try:
        parse_link = urlparse(link)
        ipaddress.ip_address(parse_link.hostname)
        return True
    except ValueError:
        return False


def is_same_subdomain(domain1, domain2):
    parts1 = domain1.split('.')
    parts2 = domain2.split('.')

    # 至少需要两个部分
    if len(parts1) < 2 or len(parts2) < 2:
        return False
    # 比较主域名
    return parts1[-2] == parts2[-2]


def is_recorded(domain1, domain2):
    # domain type: test.com
    domain_part1 = domain1.split('.')
    domain_part2 = domain2.split('.')

    # 至少需要两个部分
    if len(domain_part1) < 2 or len(domain_part2) < 2:
        return False

    try:
        parts1 = beian.icp_search(domain_part1[-2])['Company_Name']
        parts2 = beian.icp_search(domain_part2[-2])['Company_Name']
        print(domain_part1[-2], domain_part2[-2])
        if parts1 == parts2:
            return True
        else:
            return False
    except:
        return False


def get_site_info_result(url):
    return filter_external_links(get_external_links(url), url)


if __name__ == '__main__':
    url = 'https://www.example.cn/'
    external_links = get_external_links(url)
    result = filter_external_links(external_links, url)
    print(result)
