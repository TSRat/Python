import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# ==============================================================================
# 【步骤 1】 在这里粘贴你的 Cookie (必须保留，否则看不到“我没读过”这个页面)
# ==============================================================================
your_cookie = 'bid=ZlzSxqs9Q6Y; ll="118254"; _vwo_uuid_v2=DCE08EBAF77E46BC8E7FDD6E8B92D84B1|c1894fcb5676fb4b9e03aa2479041538; _pk_id.100001.8cb4=7486e92c64f6b2f2.1748666989.; __utmc=30149280; viewed="25891318_34835082_1066586_26935098_35217841_35481713_36110302_1024279_36736639_1064841"; __yadk_uid=r1n2NqVA7LCMZJhU95MguPc74kwhsv2w; __utma=30149280.94536081.1747136049.1766935883.1767009689.4; __utmz=30149280.1767009689.4.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.1.94536081.1747136049; _ga_Y4GN1R87RG=GS2.1.s1767460994$o2$g1$t1767461002$j52$l0$h0; dbcl2="241889599:H2fZKc9jZO0"; ck=mP9X; frodotk_db="42fb85da5b549811c8f2918f11fdc833"; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1767497807%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D'

# ==============================================================================
# 【步骤 2】 这里不再填 ID，而是直接粘贴你点开“我没读过的书”后，浏览器地址栏里的 完整URL
# 例如：https://www.douban.com/doulist/153177341/?sort=seq&sub_type=4
# ==============================================================================
target_url_raw = "https://www.douban.com/doulist/155895837/?sort=time&sub_type=5" 

def get_header():
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Referer': 'https://www.douban.com/',
        'Cookie': your_cookie
    }

def parse_info(info_text):
    info_dict = {'作者': '', '出版社': '', '出版年': ''}
    lines = info_text.split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line or '：' in line:
            sep = ':' if ':' in line else '：'
            key, value = line.split(sep, 1)
            key = key.strip()
            value = value.strip()
            if key in info_dict:
                info_dict[key] = value
    return info_dict

def scrape_filtered_doulist(base_url):
    books_data = []
    start = 0
    page_size = 25
    
    print(f"--- 开始从以下链接爬取: ---")
    print(f"{base_url}")
    print("----------------------------")

    while True:
        # --- 智能翻页逻辑 ---
        # 你的 URL 可能已经包含了 '?' (比如 ?sort=seq)，所以我们得判断是用 '?' 还是 '&' 来拼接翻页参数
        separator = '&' if '?' in base_url else '?'
        url = f"{base_url}{separator}start={start}"
        
        print(f"正在抓取第 {start // page_size + 1} 页...")
        
        try:
            response = requests.get(url, headers=get_header(), timeout=15)
            if response.status_code != 200:
                print(f"连接失败，状态码: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all("div", class_="doulist-item")
            
            # 如果当前页没有书，或者书的数量为0，停止
            if not items:
                print("--- 爬取结束 (列表已到底) ---")
                break
            
            current_page_count = 0
            
            for item in items:
                try:
                    # 既然已经在“未读”页面了，不需要任何判断，直接抓！
                    
                    title_div = item.find("div", class_="title")
                    if not title_div: continue 

                    title_link = title_div.find("a")
                    book_name = title_link.get_text(strip=True)
                    book_url = title_link['href']
                    
                    # 封面
                    post_div = item.find("div", class_="post")
                    img_tag = post_div.find("img") if post_div else None
                    cover_url = img_tag['src'] if img_tag else ""

                    # 评分
                    rating_span = item.find("span", class_="rating_nums")
                    rating = rating_span.get_text(strip=True) if rating_span else ""

                    # 出版信息
                    abstract_div = item.find("div", class_="abstract")
                    parsed_info = parse_info(abstract_div.get_text()) if abstract_div else {}

                    book_entry = {
                        '封面链接': cover_url,
                        '标题': book_name,
                        '个人评分': rating, 
                        '出版日期': parsed_info.get('出版年', ''),
                        '作者': parsed_info.get('作者', ''),
                        '条目链接': book_url
                    }
                    books_data.append(book_entry)
                    current_page_count += 1
                    
                except Exception as e:
                    print(f"抓取某本书时出错: {e}")
                    continue
            
            print(f"  -> 本页成功抓取 {current_page_count} 本")
            
            # 翻页
            start += page_size
            time.sleep(random.uniform(2, 4)) 
            
        except Exception as e:
            print(f"网络请求出错: {e}")
            break

    return books_data

def save_to_excel(data, filename="My_Unread_Books.xlsx"):
    if not data:
        print("未抓取到数据，请检查Cookie或URL是否正确。")
        return
    df = pd.DataFrame(data)
    cols = ['封面链接', '标题', '个人评分', '出版日期', '作者', '条目链接']
    final_cols = [c for c in cols if c in df.columns]
    df = df[final_cols]
    df.to_excel(filename, index=False)
    print(f"成功！已将 {len(data)} 本未读书籍导出至 {filename}")

if __name__ == "__main__":
    # 去除可能存在的首尾空格
    clean_url = target_url_raw.strip()
    if not clean_url:
        print("错误：请先在代码中填入 URL！")
    else:
        books = scrape_filtered_doulist(clean_url)
        save_to_excel(books)