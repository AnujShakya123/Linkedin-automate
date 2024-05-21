
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Replace with your LinkedIn login credentials
LINKEDIN_EMAIL = 'anujshakya808@gmail.com'
LINKEDIN_PASSWORD = 'Anuj@8645'
POST_URL = 'https://www.linkedin.com/feed/update/urn:li:activity:7156969636683505664/'

# Set up Chrome options to suppress WebRTC errors
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--mute-audio")

# Initialize the Chrome driver with options
driver = webdriver.Chrome(options=chrome_options)

# Function to log in to LinkedIn
def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    
    try:
        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')

        email_field.send_keys(LINKEDIN_EMAIL)
        password_field.send_keys(LINKEDIN_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)

        print("Login successful")
    except NoSuchElementException as e:
        print(f"Login failed: {e}")
        driver.quit()

# Function to navigate to the post and extract commenters
def get_commenters(post_url):
    driver.get(post_url)
    time.sleep(5)  # Adjust this wait as needed
    commenters = []

    try:
        # Wait for the comments section to be present
        print("Waiting for the comments section to be present")
        comments_section = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'comments-comments-list'))
        )
        print("Comments section found")

        # Find all individual comments within the comments section
        comments = comments_section.find_elements(By.CLASS_NAME, 'comments-comment-item')
        print(f"Found {len(comments)} comments")

      

        for comment in comments:
            try:
                # Find the commenter profile link within each comment
                # Adjust the selector based on actual structure. Example: 'a[data-control-name="identity_profile_photo"]'
                commenter_profile = comment.find_element(By.CSS_SELECTOR, '[aria-label="View Raj Kanojia’s profile"]')
                profile_url = commenter_profile.get_attribute('href')
                commenters.append(profile_url)
                print(f"Commenter profile found: {profile_url}")
            except NoSuchElementException:
                print("No profile link found in this comment")
                continue

    except TimeoutException:
        print("Timeout: Comments section did not load in time.")
    except NoSuchElementException as e:
        print(f"Error: Unable to find an element: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return commenters

# Function to send direct messages to commenters
def send_direct_message(profile_url, message):
    driver.get(profile_url)
    time.sleep(3)  # Adjust this wait as needed

    try:
        message_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'message-anywhere-button'))
        )
        message_button.click()
        time.sleep(2)

        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'msg-form__contenteditable'))
        )
        message_box.send_keys(message)

        send_button = driver.find_element(By.CLASS_NAME, 'msg-form__send-button')
        send_button.click()
        time.sleep(2)
        print(f"Message sent to {profile_url}")
    except Exception as e:
        print(f"Could not send message to {profile_url}: {e}")

# Main script
linkedin_login()
commenters = get_commenters(POST_URL)
message_text = "Thank you for your comment on my post!"

for commenter in commenters:
    send_direct_message(commenter, message_text)

# Close the driver
driver.quit()
 