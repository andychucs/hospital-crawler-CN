import csv
import requests
from bs4 import BeautifulSoup


def init():
    url = 'https://www.zgylbx.com/index.php?m=content&c=index&a=lists&catid=106&page='
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
    }
    return url, headers


def get_rows(msg):
    row_list = []
    row = []
    sub_row = False
    for line in msg[1:]:
        data = line.find_all('td')
        if not sub_row:
            prov_city = data[1].text.strip().split('-')
            row = [
                data[0].text,
                prov_city[0],
                prov_city[1],
                data[2].text,
                data[3].text
            ]
            sub_row = True
        else:
            data = str(data[0]).split('<br/>')
            add = data[0].strip().split('医院地址:')[-1]
            tel = data[1].strip().split('医院电话:')[-1]
            mail = data[2].strip().split('医院邮箱:')[-1]
            site = data[3].strip().split('医院网站:')[-1][:-5]
            row.extend([add, tel, mail, site])
            row_list.append(row)
            sub_row = False
    return row_list


def crawler(u, h):
    rows = [["医院名称", '省份', '城市', "医院等级", '擅长病症', '医院地址', '医院电话', '医院邮箱', '医院网站']]
    for i in range(1, 1530):
        r = requests.get(str(u) + str(i) + "&k1=0&k2=0&k3=0&k4=", headers=h, timeout=20)
        print('url:'+str(u) + str(i) + "&k1=0&k2=0&k3=0&k4=")
        soup = BeautifulSoup(r.text, "html.parser")
        message = soup.find_all('tr')
        rows.extend(get_rows(message))
    return rows


if __name__ == '__main__':
    url, headers = init()
    with open('hospital.csv', 'a') as f:
        write = csv.writer(f)
        write.writerows(crawler(url, headers))
