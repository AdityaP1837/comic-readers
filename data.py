import requests
from bs4 import BeautifulSoup
# import urllib.request


class Link_Gather:
    def __init__(self):
        self.url = "https://xoxocomics.com"
        r = requests.get(self.url)
        self.htmlContent = r.content

    def parser(self):
        soup = BeautifulSoup(self.htmlContent, "html.parser")
        src = []
        img_Tags = soup.find_all('img')
        for link in img_Tags:
            src.append(link.get('data-original'))

        self.page_links = []
        for i in src:
            if i != None:
                self.page_links.append(i)
        return self.page_links

    def main_page_trending(self):
        soup = BeautifulSoup(self.htmlContent, 'html.parser')
        img_list = soup.find_all('img', class_='lazyOwl')

        trending_list = []
        for link in img_list:
            img_text = link['alt']
            img_link = soup.find('a', title=img_text)
            img_link_href = img_link["href"].replace(
                "https://xoxocomics.net/comic/", "")
            sample = {
                'text': img_text,
                'source': link['data-src'],
                'link': img_link_href
            }
            trending_list.append(sample)
        return trending_list

    def main_page_latest(self):
        soup = BeautifulSoup(self.htmlContent, 'html.parser')

        latest = soup.find_all('div', class_='image')
        latest_list = []

        for i in latest:
            sample = {
                'text': i.img["alt"],
                'source': i.img["data-original"],
                'page_link': (i.a["href"]).replace("https://xoxocomics.net/comic/", "")

            }
            latest_list.append(sample)
        return latest_list

    def Comic_List(self, aplphabet: str):
        self.alphabet = aplphabet
        r = requests.get(
            f"https://xoxocomics.net/comic-list/alphabet?c={self.alphabet}")
        response = r.content

        soup = BeautifulSoup(response, 'html.parser')

        cl_resource = soup.find_all('li', class_="row")
        list_0 = []
        comic_link = []
        for i in cl_resource:
            row_text = i.find('div', class_='title').text
            # row_img = i.img
            # row_img_link = row_img['data-original']
            row_comic_status = i.find('div', class_='col-xs-3').text
            row_comic_status = row_comic_status.replace('\n', "")
            c_link = i.find("a", class_="jtip")['href']
            l = c_link.replace("https://xoxocomics.net/comic/", "")
            comic_link.append(l)

            sample_list = {
                'title': row_text,
                'comic-status': row_comic_status,
                # 'img-src': row_img_link,
            }
            list_0.append(sample_list)
        final_list = {
            "list": list_0,
            "comic-links": comic_link
        }
        return final_list

    def comic_page(self, page_title):
        r = requests.get(f"https://xoxocomics.net/comic/{page_title}")
        response = r.content

        soup = BeautifulSoup(response, 'html.parser')

        title = soup.find("h1", class_="title-detail").text.replace("\n", "")
        img_link = soup.find("div", class_="col-xs-4").img["src"]
        try:
            other_name = soup.find("li", class_="othername").h2.text
        except AttributeError:
            other_name = "None"
        author_name = soup.find("li", class_="author").find(
            "p", class_="col-xs-8").text.replace("\n", "")
        status_of_comic = soup.find("li", class_="status").find(
            "p", class_="col-xs-8").text.replace("\n", "")
        genres_of_comic = soup.find("li", class_="kind").find(
            "p", class_="col-xs-8").text.replace("\n", "")
        summary = soup.find("div", class_="detail-content").p.text
        issues_links = soup.find_all("div", class_="col-xs-9")
        issues = []
        for links in issues_links:
            link = links.a
            if link != None:
                a = link["href"].replace("https://xoxocomics.net/comic/", "")
                text = (link.text).replace("\n", "")
                issue_list = {
                    "name": text,
                    "link": a
                }
                issues.append(issue_list)

        full_info = {
            "title": title,
            "img_link": img_link,
            "other_name": other_name,
            "author": author_name,
            "genres": genres_of_comic,
            "status": status_of_comic,
            "summary": summary,
            "issues": issues
        }
        return full_info

    def reading_page(self, issue_title, issue_num, issue_id):
        r = requests.get(
            f"https://xoxocomics.net/comic/{issue_title}/{issue_num}/{issue_id}/all")
        response = r.content

        soup = BeautifulSoup(response, 'html.parser')
        title = soup.find("h1")
        issue_title = title.text
        pages = soup.find_all("div", class_="page-chapter")
        page_images = []

        for i in pages:
            images = i.img["data-original"]
            page_images.append(images)

        reading_page_info = {
            "page_title": issue_title,
            "page_images": page_images
        }
        return reading_page_info

    def searched_results(self, query):
        query = query.strip().replace(" ", "+")
        