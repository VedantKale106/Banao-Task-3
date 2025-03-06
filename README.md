# Twitter Profile Scraper

##Video link - https://drive.google.com/file/d/1m2nyhIas3qEFBislK40xYTYFASO4Dv7c/view?usp=sharing

This project scrapes Twitter profile data (bio, following count, followers count, location, website) from a list of Twitter profile links provided in a CSV file and stores the data in an SQLite database.

## Prerequisites

- Python 3.x
- Required Python libraries:
  - pandas
  - selenium
  - webdriver-manager
  - beautifulsoup4
  - sqlite3

Install the required libraries using pip:

```bash
pip install pandas selenium webdriver-manager beautifulsoup4
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd vedantkale106-banao-task-3.git
    ```

2.  **Prepare the CSV file:**

    -   Create a CSV file named `twitter_links.csv` in the project directory.
    -   Add the Twitter profile links you want to scrape in a column named "Links".

    Example `twitter_links.csv`:

3.  **Add your Twitter credentials:**


    ```python
    username = "YOUR_USERNAME"
    password = "YOUR_PASSWORD"
    ```

    **Warning:** Storing your password directly in the code is not recommended for production environments. Consider using environment variables or a secure configuration file.

## Usage

1.  **Run the script:**

    ```bash
    python sqlite.py
    ```

2.  **Check the output:**

    -   The script will scrape the data and save it to `twitter_profiles.db`.
    -   The console will display the scraping progress and any errors encountered.

## Database Structure

The scraped data is stored in an SQLite database named `twitter_profiles.db` with the following table structure:

```sql
CREATE TABLE twitter_profiles (
    Profile_Link TEXT PRIMARY KEY,
    Bio TEXT,
    Following_Count TEXT,
    Followers_Count TEXT,
    Location TEXT,
    Website TEXT
);
```

## Notes

-   The script uses Selenium to automate the browser and scrape the data.
-   The script handles common errors like `NoSuchElementException` and `TimeoutException`.
-   Twitter's website structure may change, which could break the script. You may need to update the selectors in the code accordingly.
-   Be mindful of Twitter's terms of service and avoid excessive scraping.
-   Replace `YOUR_VIDEO_ID` with your actual youtube video id.
-   The script uses Microsoft edge. If you want to use another browser, you will need to change the Webdriver to the correct browser.

