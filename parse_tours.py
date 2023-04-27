from bs4 import BeautifulSoup as bs4


def get_all_tours(html: str):
    tours_urls = []
    soup = bs4(html, 'html.parser')
    tours = soup.find_all('a', class_='lmc__templateHref')
    for tour in tours:
        tours_urls.append(tour['href'])

    print(tours_urls)


if __name__ == "__main__":
    with open('tours.html', 'r', encoding='utf8') as f:
        file = f.read()
    get_all_tours(file)




