import pandas as pd
import time
import os
import yt_dlp
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

def check_youtube(url_loc: str) -> bool:
    return url_loc.startswith("https://www.youtube.com/") and "/shorts" in url_loc

def parser(url_local: str) -> List[List[str]]:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url_local)
        driver.implicitly_wait(10)
        
        contents = driver.find_element(By.ID, "contents")
        links, titles, views = [], [], []

        while True:
            video_elements = contents.find_elements(By.ID, "content")
            for el in video_elements:
                try:
                    el_link = el.find_element(By.CSS_SELECTOR, "a.shortsLockupViewModelHostEndpoint").get_attribute("href")
                    el_title = el.find_element(By.CSS_SELECTOR, "h3.shortsLockupViewModelHostMetadataTitle span").text
                    el_view = el.find_element(By.CSS_SELECTOR, "div.shortsLockupViewModelHostMetadataSubhead span").text
                    
                    if el_link and el_link not in links:
                        links.append(el_link)
                        titles.append(el_title)
                        views.append(el_view)
                except Exception:
                    continue
            
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)
            
            new_video_elements = contents.find_elements(By.ID, "content")
            if len(new_video_elements) == len(video_elements):
                break
        
        return [links, titles, views]
    except Exception as e:
        print(f"Error: {e}")
        return [[], [], []]
    finally:
        driver.quit()

def save_to_csv(links: List[str], titles: List[str], views: List[str], filename: str) -> None:
    df = pd.DataFrame(list(zip(titles, links, views)), columns=['Title', 'Link', 'View'])
    os.makedirs("data", exist_ok=True)
    df.to_csv(f"data/{filename}.csv", index=False)
    
    for _ in tqdm(titles, desc="Saving data"):
        time.sleep(0.01)
    print(f"Data saved to data/{filename}.csv")

def download_videos(links: List[str], download_path: str = "downloads"):
    if download_path is None:
        download_path = os.path.join(os.getcwd(), "downloads")
    os.makedirs(download_path, exist_ok=True)
    
    ydl_opts = {
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'format': 'mp4',
        'retries': 10,  # Повторные попытки при ошибках
        'socket_timeout': 30,  
        'proxy': '', # Введите ваш прокси
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},  # Обход ограничений
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        time.sleep(5)
        for link in tqdm(links, desc="Downloading videos"):
            try:
                # Скачиваем видео
                ydl.download([link])
            except Exception as e:
                print(f"Failed to download {link}: {e}")

if __name__ == "__main__":
    while True:
        url = input("Enter a YouTube Shorts page URL: ")
        if check_youtube(url):
            links, titles, views = parser(url)
            if links:
                filename = url.split("/")[-1]
                save_to_csv(links, titles, views, filename)
                
                print("Do you want to download the videos? (yes/no)")
                if input().strip().lower() == "yes":
                    download_videos(links)
            else:
                print("No videos found.")
        else:
            print("Invalid URL. Make sure it's a YouTube Shorts page.")
