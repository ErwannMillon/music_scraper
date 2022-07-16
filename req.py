from time import sleep
from requests_html import HTMLSession
from bs4 import BeautifulSoup   
s = HTMLSession()
url = "https://www.youtube.com/results?search_query=Boris+Brejcha+-+Space+Dive/"
base_url = "https://www.youtube.com/watch?v="
response = s.get(url)
response.html.render(sleep=2)
soup = BeautifulSoup(response.html.text, "lxml")
print(dir(response.html))
with open("x.html", "w") as d:
    d.write(str(response.html.text))
x = soup.findAll('a', attrs={"id": "video-title"})
print(response.html.absolute_links)