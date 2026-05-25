import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def get_header():
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Referer': 'https://www.douban.com/'
    }

def parse_info(info_text):
    """解析作者、出版社、出版年等混合信息"""
    info_dict = {'作者': '', '出版社': '', '出版年': ''}
    lines = info_text.split('\n')
    for line in lines:
        line = line.strip()
        if ':' in line or '：' in line:
            # 兼容中英文冒号
            sep = ':' if ':' in line else '：'
            key, value = line.split(sep, 1)
            key = key.strip()
            value = value.strip()
            if key in info_dict:
                info_dict[key] = value
    return info_dict

def scrape_doulist(doulist_id):
    base_url = "https://www.douban.com/doulist/{}/"
    books_data = []
    start = 0
    page_size = 25
    
    print(f"--- 开始爬取豆列 ID: {doulist_id} ---")

    while True:
        url = f"{base_url.format(doulist_id)}?start={start}"
        print(f"正在分析页面: {url}")
        
        try:
            response = requests.get(url, headers=get_header(), timeout=15)
            if response.status_code != 200:
                print(f"连接失败，状态码: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.find_all("div", class_="doulist-item")
            
            if not items:
                print("--- 爬取结束 (没有更多条目) ---")
                break
            
            for item in items:
                try:
                    # 跳过已被删除的条目或非书籍条目
                    title_div = item.find("div", class_="title")
                    if not title_div: continue 

                    # 1. 标题 & 链接
                    title_link = title_div.find("a")
                    book_name = title_link.get_text(strip=True)
                    book_url = title_link['href']
                    
                    # 2. 封面链接 (新增)
                    # 封面通常在 post 类的 div 下的 img 标签里
                    post_div = item.find("div", class_="post")
                    img_tag = post_div.find("img") if post_div else None
                    cover_url = img_tag['src'] if img_tag else ""

                    # 3. 评分 (映射为豆瓣均分)
                    rating_span = item.find("span", class_="rating_nums")
                    rating = rating_span.get_text(strip=True) if rating_span else ""

                    # 4. 评价时间 (新增，映射为加入豆列的时间)
                    # 通常在 actions 类下的 time span 中
                    action_div = item.find("div", class_="actions")
                    time_span = action_div.find("span", class_="time") if action_div else None
                    if time_span:
                        # 格式通常为 "2018年5月12日" 或 "2018-05-12 10:00:00"
                        rate_date = time_span.get_text(strip=True)
                    else:
                        rate_date = ""

                    # 5. 短评
                    comment_div = item.find("blockquote", class_="comment")
                    my_comment = comment_div.get_text(strip=True) if comment_div else ""

                    # 6. 出版信息 (作者/日期)
                    abstract_div = item.find("div", class_="abstract")
                    parsed_info = parse_info(abstract_div.get_text()) if abstract_div else {}

                    # 构建数据字典 (Key必须和下面保存时的列名对应)
                    book_entry = {
                        '封面链接': cover_url,
                        '标题': book_name,
                        '个人评分': rating,     # 注意：这里抓取的是公有评分
                        '打分日期': rate_date,  # 注意：这里抓取的是加入豆列日期
                        '我的短评': my_comment,
                        '出版日期': parsed_info.get('出版年', ''),
                        '作者': parsed_info.get('作者', ''),
                        '条目链接': book_url
                    }
                    books_data.append(book_entry)
                    
                except Exception as e:
                    print(f"跳过某一条目，原因: {e}")
                    continue

            start += page_size
            time.sleep(random.uniform(1.5, 3)) # 稍微加快一点速度
            
        except Exception as e:
            print(f"网络请求出错: {e}")
            break

    return books_data

def save_to_excel(data, filename="doulist_export.xlsx"):
    if not data:
        print("没有数据，无法保存。")
        return
        
    df = pd.DataFrame(data)
    
    # --- 关键修改：强制指定列顺序 ---
    # 这决定了 Excel 中从左到右的排列
    target_columns = [
        '封面链接', 
        '标题', 
        '个人评分', 
        '打分日期', 
        '我的短评', 
        '出版日期', 
        '作者', 
        '条目链接'
    ]
    
    # 防止因为某些字段抓取失败导致报错，我们取交集
    # (即：只保存那些既在数据里有，又在目标列表里的列)
    final_cols = [col for col in target_columns if col in df.columns]
    
    # 重新排序
    df = df[final_cols]
    
    try:
        df.to_excel(filename, index=False)
        print(f"成功！文件已保存为: {filename}")
    except Exception as e:
        print(f"保存 Excel 失败 (可能是文件被打开了?): {e}")

# ==========================================
# 在这里替换你的豆列 ID
# ==========================================
target_doulist_id = "155895837"  # 示例 ID，请替换

if __name__ == "__main__":
    books = scrape_doulist(target_doulist_id)
    save_to_excel(books, f"My_Doulist_{target_doulist_id}.xlsx")