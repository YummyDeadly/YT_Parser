**# YT_Parser**# YouTube Shorts Parser & Downloader

## Description
This project is a Python-based YouTube Shorts parser and downloader. It uses Selenium to scrape video links from a given YouTube Shorts page and yt-dlp to download the extracted videos.

## Features
- Extracts video links, titles, and views from a YouTube Shorts page.
- Saves extracted data to a CSV file.
- Allows batch downloading of videos using yt-dlp.

## Requirements
- Python 3.7+
- Google Chrome
- Chrome WebDriver
- Required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-shorts-parser.git
   cd youtube-shorts-parser
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the script:
   ```bash
   python main.py
   ```
2. Enter a YouTube Shorts page URL when prompted.
3. The script will extract video links and save them to `data/{filename}.csv`.
4. Optionally, you can choose to download the videos.

## File Structure
```
📂 youtube-shorts-parser
├── 📂 data                # Contains saved CSV files
├── 📂 downloads           # Directory where downloaded videos are stored
├── main.py               # Main script
├── requirements.txt      # List of dependencies
├── README.md             # Project documentation
```

## Notes
- Ensure that your Chrome version matches the installed ChromeDriver.
- Some videos may be unavailable due to YouTube's restrictions.

## License
This project is licensed under the MIT License.

