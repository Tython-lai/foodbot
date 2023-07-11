from bs4 import BeautifulSoup
import requests
 
# 愛食記爬蟲
class IFoodie:
    def __init__(self, area):
        self.area = area  # 地區
    
    def scrape(self):
        """
        爬取 ifoodie.tw 網站，找出前五筆人氣最高，且營業中的餐廳
        :return str 餐廳名稱、評價及地址
        """
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list?sortby=rating&opening=true")
 
        # [TODO]: 以 bs4 解析網頁中前五筆餐廳資料
        soup = BeautifulSoup(response.content, "html.parser")
 
        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            # 'div', {'class': 'jsx-1776651079 restaurant-info'}, limit=5)
            'div', {'class': 'restaurant-info'}, limit=5)
 
        content = ""
        for card in cards:
 
            title = card.find(  # 餐廳名稱
                # "a", {"class": "jsx-1776651079 title-text"}).getText()
                "a", {"class": "title-text"}).getText()
 
            stars = card.find(  # 餐廳評價
                # "div", {"class": "jsx-1207467136 text"}).getText()
                "div", {"class": "text"}).getText()
 
            address = card.find(  # 餐廳地址
                # "div", {"class": "jsx-1776651079 address-row"}).getText()
                "div", {"class": "address-row"}).getText()
 
            #TODO: 將取得的餐廳名稱、評價及地址依所需格式連結一起並傳回
            content += f"{title} \n{stars}顆星 \n{address} \n\n"
 
        return content

if __name__ == '__main__':
    food = IFoodie('台中')  #使用者傳入的訊息文字
    print(food.scrape())  # 回應前五間最高人氣且營業中的餐廳訊息文字

