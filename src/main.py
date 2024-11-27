import requests,os
from bs4 import BeautifulSoup
from manga import Manga
from pprint import pprint
import inquirer,certifi

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Accept': 'image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://chapmanganelo.com/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=5, i',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

def clear_console():
    # Clear command for Windows
    if os.name == 'nt':
        os.system('cls')
    # Clear command for Unix/Linux/Mac
    else:
        os.system('clear')


def search_manga(manga_name):

    # Format manga name for URL
    manga_name = manga_name.replace(" ", "_")
    base_url = "https://m.manganelo.com/search/story/"
    manga_url = base_url + manga_name

    # Make request and parse content
    response = requests.get(manga_url,verify=certifi.where())
    soup = BeautifulSoup(response.content, "html.parser")

    # Find manga items
    manga_item = soup.find_all("div",class_="search-story-item")
    manga_choices = {}

    for item in manga_item:

        manga_item_info = item.select_one(".item-right")

        manga_name = manga_item_info.select_one("h3 a")

        manga_url = manga_name["href"]

        manga_views = manga_item_info.select("span.item-time")

        manga_author = manga_item_info.select_one("span.item-author")

        #manga_questions.append(manga_name.text+" | " + manga_views[1].text +" |  By " + manga_author.text)

        display = {
            "name":manga_name.text,
            "views":manga_views[1].text,
            "author":manga_author
        }

        manga_choices[display["name"]] = manga_url
        #print(f"display: {display} (type: {type(display)})")  # Debugging line

    

    
    #clear_console()
    question = [
        inquirer.List(
            "manga",
            message = "Choose one of the manga below",
            choices = list(manga_choices.keys()),
        )
    ]
        
    answer = inquirer.prompt(question)
    chosen_manga = answer["manga"]

    chosen_url = manga_choices[chosen_manga]
    print(f"Selected manga url: {chosen_url}")

    

    return chosen_url
        

def get_manga_info(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Get manga details

    manga_details = soup.select_one("html body div.body-site div.container.container-main div.container-main-left")

    # Get cover images

    cover = manga_details.select_one(".story-info-left")
    cover = cover.find("img")
    cover = cover.get("src")

    # Get title of manga

    details = manga_details.select_one(".story-info-right")
    title = details.find("h1")
    
    # Get author , status and genres

    table = manga_details.select_one(".story-info-right")
    author = table.select_one(".variations-tableInfo > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) ")
                            #    > a:nth-child(1)
                            #   .variations-tableInfo > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)
    status = table.select_one(".variations-tableInfo > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2)")
    genres = table.select_one(".variations-tableInfo > tbody:nth-child(1) > tr:nth-child(3)")
    genres = genres.find_all("a")
    print(author)

    #Get chapters of manga

    chapters = manga_details.select_one(".panel-story-chapter-list")
    chapters = chapters.select_one(".row-content-chapter")
    chapters = chapters.find_all("a")
    
    manga = Manga(title.text,author.text,cover,status.text,genres,chapters)

    return manga

def download_chapters(chapter_links,title):
    save_directory = title
    os.makedirs(save_directory, exist_ok=True)

    links = []

    for chapter_index, chapter in enumerate(chapter_links):

        chapter_link = chapter["href"]
        chapter_name = chapter.text.replace(" ", "_")
        chapter_directory = os.path.join(save_directory,chapter_name)
        os.makedirs(chapter_directory,exist_ok=True)


        print(f"Downloading images for chapter {chapter_index + 1}: {chapter_link}")
        response = requests.get(chapter_link)
        soup = BeautifulSoup(response.content, "html.parser")
        manga_images = soup.select_one("html body div.body-site div.container-chapter-reader")
        manga_images = manga_images.find_all("img")
        for img_index,img in enumerate(manga_images):
            url = img.get("src")
            filename = f"{img["alt"]}.jpg"  # Change extension as needed
            save_as = os.path.join(chapter_directory, filename)

            # Download the image
            img_response = requests.get(url,headers=headers)
            if img_response.status_code == 200:  # Check if the request was successful
                with open(save_as, 'wb') as file:
                    file.write(img_response.content)
                    print(f"Saved {filename}")
            else:
                    print(f"Failed to download image: {url}")



def latest_updates():

    url = "https://m.manganelo.com/genre-all-update-latest"
    response = requests.get(url,verify = certifi.where())
    soup = BeautifulSoup(response.content,"html.parser")

    manga_items = soup.find_all("div",class_="content-genres-item")

    list_of_latest = []

    for item in manga_items:

        manga_item_cover = item.select_one("img")['src']
        manga_item_title = item.select_one(".genres-item-info h3 a")

        api = {
                "title" : manga_item_title.text ,
                "cover" : manga_item_cover
                }

        list_of_latest.append(api)


    return list_of_latest
        

#manga = input("enter manga to download (ensure it is writen well and with spaces) ")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="downloads for manga pages")
    parser.add_argument('--link',type=str,default=None,help="Link of the manga")
    parser.add_argument('--title',)
    args = parser.parse_args()

    if args.link is None:
        print("Please provide a manga link using --link")
    else:
        manga_data = search_manga(args.link)
        manga_info = get_manga_info(manga_data)
        download_chapters(manga_info.chapters,manga_info.title)
        

latest_updates()
