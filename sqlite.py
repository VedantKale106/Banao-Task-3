import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sqlite3

# Load the CSV file containing Twitter profile links
csv_file = "twitter_links.csv"
df = pd.read_csv(csv_file)

# Set up Selenium with Edge
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

def scrape_twitter_profile(url, username, password):
    try:
        driver.get("https://twitter.com/i/flow/login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        username_input = driver.find_element(By.NAME, "text")
        username_input.send_keys(username)
        next_button = driver.find_element(By.XPATH, '//span[text()="Next"]')
        next_button.click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH, '//span[text()="Log in"]')
        login_button.click()
        time.sleep(2)
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        bio = "N/A"
        try:
            bio_tag = soup.find("div", {"data-testid": "UserDescription"})
            bio = bio_tag.text if bio_tag else "N/A"
        except AttributeError:
            bio = "N/A"

        following = followers = "N/A"
        try:
            following_element = soup.find("a", href=lambda href: href and "/following" in href)
            followers_element = soup.find("a", href=lambda href: href and "followers" in href)

            if following_element:
                count_span = following_element.find("span", class_="css-1jxf684")
                if count_span:
                    following = count_span.text

            if followers_element:
                count_span = followers_element.find("span", class_="css-1jxf684")
                if count_span:
                    followers = count_span.text

        except AttributeError:
            following = "N/A"
            followers = "N/A"

        print(f"Following: {following}, Followers: {followers}")

        location = "N/A"
        try:
            location_tag = soup.find("span", {"data-testid": "UserLocation"})
            location = location_tag.text if location_tag else "N/A"
        except AttributeError:
            location = "N/A"

        website = "N/A"
        try:
            website_tag = soup.find("a", {"data-testid": "UserUrl"})
            website = website_tag["href"] if website_tag else "N/A"
        except (AttributeError, TypeError):
            website = "N/A"

        return {"Bio": bio, "Following Count": following, "Followers Count": followers, "Location": location, "Website": website}

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Element not found or timeout occurred: {e}")
        return {"Bio": "Error", "Following Count": "Error", "Followers Count": "Error", "Location": "Error", "Website": "Error"}
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return {"Bio": "Error", "Following Count": "Error", "Followers Count": "Error", "Location": "Error", "Website": "Error"}

# List to store scraped data
scraped_data = []

username = "vedant9531"
password = "95314933"

# Process each Twitter profile link
for index, row in df.iterrows():
    profile_url = row[0]
    print(f"Scraping: {profile_url}")
    try:
        data = scrape_twitter_profile(profile_url, username, password)
        data["Profile_Link"] = profile_url
        scraped_data.append(data)
    except Exception as e:
        print(f"Error scraping {profile_url}: {e}")
        scraped_data.append({"Profile_Link": profile_url, "Bio": "Error", "Following Count": "Error", "Followers Count": "Error", "Location": "Error", "Website": "Error"})

# Close browser
driver.quit()

# Store data in SQLite database
conn = sqlite3.connect("twitter_profiles.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS twitter_profiles (
        Profile_Link TEXT PRIMARY KEY,
        Bio TEXT,
        Following_Count TEXT,
        Followers_Count TEXT,
        Location TEXT,
        Website TEXT
    )
''')

# Insert scraped data into the table
for data in scraped_data:
    cursor.execute('''
        INSERT OR REPLACE INTO twitter_profiles (Profile_Link, Bio, Following_Count, Followers_Count, Location, Website)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data["Profile_Link"], data["Bio"], data["Following Count"], data["Followers Count"], data["Location"], data["Website"]))

conn.commit()
conn.close()

print("Scraping completed! Data saved to twitter_profiles.db")