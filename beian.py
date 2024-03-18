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


def icp_search(domain):
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
