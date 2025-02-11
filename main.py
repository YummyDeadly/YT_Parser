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
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading

def check_youtube(url_loc: str, format_choice: str) -> bool:
    if format_choice == "shorts":
        return url_loc.startswith("https://www.youtube.com/") and "/shorts" in url_loc
    elif format_choice == "video":
        return url_loc.startswith("https://www.youtube.com/watch?v=")
    return False

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

def download_videos(links: List[str], num_downloads: int, download_path: str = "downloads"):
    if download_path is None:
        # Получаем путь к директории, где находится скрипт
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Указываем папку рядом с этим скриптом для загрузки
        download_path = os.path.join(script_dir, "YouTube_Videos")
        
    os.makedirs(download_path, exist_ok=True)
    
    ydl_opts = { 
        'outtmpl': f'{download_path}/%(title)s.%(ext)s',
        'format': 'mp4',
        'retries': 10,
        'socket_timeout': 30,
        'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, link in enumerate(tqdm(links[:num_downloads], desc="Downloading videos")):
            try:
                ydl.download([link])
            except Exception as e:
                print(f"Failed to download {link}: {e}")

def main():
    format_choice = input("Choose format (shorts/video): ").strip().lower()
    if format_choice not in ["shorts", "video"]:
        print("Invalid format. Please choose 'shorts' or 'video'.")
        return
    
    url = input(f"Enter a YouTube {format_choice} page URL: ").strip()
    if not check_youtube(url, format_choice):
        print("Invalid URL. Make sure it's a valid YouTube page.")
        return
    
    if format_choice == "shorts":
        links, titles, views = parser(url)
        if not links:
            print("No videos found.")
            return
        
        print(f"Found {len(links)} videos.")
        num_downloads = input(f"How many videos do you want to download? (1 to {len(links)}): ").strip()
        try:
            num_downloads = int(num_downloads)
            if num_downloads < 1 or num_downloads > len(links):
                print("Invalid number of downloads.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return
        
        download_videos(links, num_downloads)
    else:
        download_videos([url], 1)

if __name__ == "__main__":
    main()
