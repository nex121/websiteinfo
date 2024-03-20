import time

import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore")


def extract_data(html):
    result = {}

    soup = BeautifulSoup(html, 'html.parser')

    type = soup.select_one('td.th:contains(备案类型) + td span').text
    company = soup.select_one('td.th:contains(备案主体) + td a').text
    number = soup.select_one('td.th:contains(备案号) + td a').text
    start = soup.select_one('td.th:contains(备案时间) + td span').text
    end = soup.select_one('td.th:contains(备案时间) + td span').next_sibling.text
    verify_time = start + "-" + end

    result["typ"] = type
    result["comName"] = company
    result["license"] = number
    result["verifyTime"] = verify_time

    return result


def icp_search0(domain):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            "Content-Type": "application/json"
        }
        res = requests.get("https://icplishi.com/" + domain + "/", headers=headers, verify=False).text

        if "备案主体" not in res:
            return None
        info = extract_data(res)
        formatted_data = {"ICP_Type": info["typ"].strip(), "Company_Name": info["comName"].strip(),
                          "ICP_Number": info["license"].strip(), "Verify_Time": info["verifyTime"].strip()}
        return formatted_data
    except Exception as e:
        return None


def icp_search1(domain):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
            "Content-Type": "application/json"
        }
        res = requests.get("https://www.aizhan.com/cha/" + domain + "/", headers=headers, verify=False).text

        if "备案信息" not in res:
            return None
        soup = BeautifulSoup(res, 'html.parser')
        icp_number = soup.find("a", id="icp_icp").text
        icp_type = soup.find("span", id="icp_type").text
        icp_company = soup.find("span", id="icp_company").text
        icp_passtime = soup.find("span", id="icp_passtime").text

        formatted_data = {"ICP_Type": icp_type.strip(), "Company_Name": icp_company.strip(),
                          "ICP_Number": icp_number.strip(), "Verify_Time": icp_passtime.strip()}
        # 防止请求过快被禁
        time.sleep(2)
        return formatted_data
    except Exception as e:
        return None


def icp_search(domain):
    if icp_search0(domain):
        return icp_search0(domain)
    else:
        return icp_search1(domain)
