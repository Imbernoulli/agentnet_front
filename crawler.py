import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def save_resource(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)

# 目标网站URL
url = 'https://aypan17.github.io/machiavelli/'

# 本地保存的基本路径
base_path = 'website/'

# 发送HTTP GET请求
response = requests.get(url)
response.raise_for_status()

# 解析HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 保存HTML文件
html_path = os.path.join(base_path, 'index.html')
with open(html_path, 'w') as file:
    file.write(soup.prettify())

# 保存CSS文件
for link in soup.find_all('link', rel='stylesheet'):
    href = link.get('href')
    css_url = urljoin(url, href)
    css_path = os.path.join(base_path, 'css', os.path.basename(href))
    save_resource(css_url, css_path)
    link['href'] = os.path.join('css', os.path.basename(href))

# 保存图片
for img in soup.find_all('img'):
    src = img.get('src')
    img_url = urljoin(url, src)
    img_path = os.path.join(base_path, 'images', os.path.basename(src))
    save_resource(img_url, img_path)
    img['src'] = os.path.join('images', os.path.basename(src))

# 保存JavaScript文件
for script in soup.find_all('script'):
    src = script.get('src')
    if src:
        js_url = urljoin(url, src)
        js_path = os.path.join(base_path, 'js', os.path.basename(src))
        save_resource(js_url, js_path)
        script['src'] = os.path.join('js', os.path.basename(src))

# 保存修改后的HTML
with open(html_path, 'w') as file:
    file.write(soup.prettify())