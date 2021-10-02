import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_artical_infor(url, depth, data):

    # Get artical infor
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    data["title"].append(soup.find("h1", class_= "title-detail").text)
    data["publish_date"].append(soup.find("span", class_="date").text)
    data["summary"].append(soup.find("p", class_="description").text)
    paras = soup.findAll("p", class_="Normal")
    data["body"].append("\n".join([p.text for p in paras[0:-1]]))
    data["author"].append(paras[-1].text)
    links = soup.findAll("a", rel="dofollow")
    print(depth, data["title"][-1])
    return links
def get_artical_family(url, data, depth=0, max_depth=5):
    if depth > max_depth:
        return
    # Get url in artical

    links = get_artical_infor(url, depth, data)
    for ll in [l.attrs["href"] for l in links]:
        i1 = ll.find("https://vnexpress.net/")
        i2 = ll.find("html")
        if i1 >= 0 and i2 > 0:
            get_artical_family(ll, data, depth+1, 5)


# get_artical_infor("https://vnexpress.net/benh-vien-dong-dan-sau-ba-ngay-mo-cua-4365582.html")
data = {
    "title" :[],
    "publish_date":[],
    "summary" : [],
    "body":[],
    "author":[]
}
get_artical_family("https://vnexpress.net/benh-vien-dong-dan-sau-ba-ngay-mo-cua-4365582.html", data)
print(len(data["body"]))
df = pd.DataFrame(data)
df.to_csv("result.csv", index = False)