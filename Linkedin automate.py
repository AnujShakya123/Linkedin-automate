import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configuration and driver setup
LINKEDIN_EMAIL = 'anujshakya808@gmail.com'
LINKEDIN_PASSWORD = 'Anuj@8645'
POST_URL = 'https://www.linkedin.com/feed/update/urn:li:activity:7156969636683505664/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--mute-audio")

driver = webdriver.Chrome(options=chrome_options)

# Login to LinkedIn
def linkedin_login():
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    
    try:
        email_field = driver.find_element(By.ID, 'username')
        password_field = driver.find_element(By.ID, 'password')

        email_field.send_keys(LINKEDIN_EMAIL)
        password_field.send_keys(LINKEDIN_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for the global navigation bar to confirm login
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'global-nav'))
        )
        
        print("Login successful")
    except TimeoutException:
        print("Timeout: Login failed to complete within the specified time.")
        driver.quit()
    except NoSuchElementException as e:
        print(f"Login failed: {e}")
        driver.quit()

    # It can also be used for login
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'username'))).send_keys(LINKEDIN_EMAIL)
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'password'))).send_keys(LINKEDIN_PASSWORD + Keys.RETURN)
    # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'global-nav')))

# Verify login
def verify_login():
    try:
        driver.get('https://www.linkedin.com/feed/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'global-nav')))
        print("Verified login state.")
    except TimeoutException:
        print("Failed to verify login state.")
        driver.save_screenshot('verify_login_failure.png')
        driver.quit()

# Handle modal pop-ups
def handle_any_modal():
    modal_xpath = [
        '//button[text()="Sign in"]',
        '//button[text()="Skip"]',
        '//button[text()="Join now"]',
        '//button[text()="Not now"]'
    ]
    for xpath in modal_xpath:
        try:
            modal_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            modal_button.click()
            print(f"Handled modal: {xpath}")
            return True
        except TimeoutException:
            continue
        except NoSuchElementException:
            print(f"Modal not found: {xpath}")
    print("No modals to handle.")
    return False

# Scroll to load all comments
def scroll_to_load_all_comments():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Get commenter profiles
def get_commenters(post_url):
    driver.get(post_url)
    time.sleep(5)
    commenters = []
    while handle_any_modal():
        pass
    scroll_to_load_all_comments()
    comments_section = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, 'comments-comments-list')))
    comments = comments_section.find_elements(By.CLASS_NAME, 'comments-comment-item')
    for comment in comments:
        try:
            commenter_profile = comment.find_element(By.CSS_SELECTOR, 'a[href*="/in/"]')
            profile_url = commenter_profile.get_attribute('href')
            commenters.append(profile_url)
            print(f"Commenter profile found: {profile_url}")
        except NoSuchElementException:
            print("No profile link found in this comment")
    return commenters

# Send direct message
def send_direct_message(profile_url, message):
    print(f"Attempting to send a message to: {profile_url}")
    driver.get(profile_url)
    try:
        # Wait and click the message button
        print("Waiting for the message button to be clickable...")
        message_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button artdeco-button--2 artdeco-button--primary ember-view pvs-profile-actions__action')]"))
        )
        message_button.click()

        # Wait and send keys to the message box
        print("Waiting for the message box to appear...")
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'msg-form__contenteditable'))
        )
        message_box.send_keys(message)

        # Click the send button
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'msg-form__send-button artdeco-button artdeco-button--1')]"))
        )
        send_button.click()
        print("Message sent successfully.")
    except TimeoutException as e:
        print(f"Failed to send message due to a timeout: {e}")
        driver.save_screenshot("TimeoutException_" + profile_url.split("/")[-1] + ".png")
    except NoSuchElementException as e:
        print(f"Error: Could not send message to {profile_url}: {e}")
        driver.save_screenshot("NoSuchElementException_" + profile_url.split("/")[-1] + ".png")
    except WebDriverException as e:
        print(f"WebDriverException: Could not send message to {profile_url}: {e}")
        driver.save_screenshot("WebDriverException_" + profile_url.split("/")[-1] + ".png")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        driver.save_screenshot("UnexpectedException_" + profile_url.split("/")[-1] + ".png")


# Main execution block
try:
    linkedin_login()
    verify_login()
    driver.get(POST_URL)
    time.sleep(5)  # Allow some time for the page to load
    commenters = get_commenters(POST_URL)
    message_text = "Thank you for your comment on my post!"
    for commenter in commenters:
        send_direct_message(commenter, message_text)
        time.sleep(8)
finally:
    driver.quit()








# import time
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# # Replace with your LinkedIn login credentials
# LINKEDIN_EMAIL = 'anujshakya808@gmail.com'
# LINKEDIN_PASSWORD = 'Anuj@8645'
# POST_URL = 'https://www.linkedin.com/feed/update/urn:li:activity:7156969636683505664/'

# # Set up Chrome options to suppress WebRTC errors
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-web-security")
# chrome_options.add_argument("--allow-running-insecure-content")
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--mute-audio")

# # Initialize the Chrome driver with options
# driver = webdriver.Chrome(options=chrome_options)

# def linkedin_login():
#     driver.get('https://www.linkedin.com/login')
#     time.sleep(2)
    
#     try:
#         email_field = driver.find_element(By.ID, 'username')
#         password_field = driver.find_element(By.ID, 'password')

#         email_field.send_keys(LINKEDIN_EMAIL)
#         password_field.send_keys(LINKEDIN_PASSWORD)
#         password_field.send_keys(Keys.RETURN)
        
#         # Wait for the global navigation bar to confirm login
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.ID, 'global-nav'))
#         )
        
#         print("Login successful")
#     except TimeoutException:
#         print("Timeout: Login failed to complete within the specified time.")
#         driver.quit()
#     except NoSuchElementException as e:
#         print(f"Login failed: {e}")
#         driver.quit()

# def verify_login():
#     try:
#         driver.get('https://www.linkedin.com/feed/')
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, 'global-nav'))
#         )
#         print("Verified login state.")
#     except TimeoutException:
#         print("Failed to verify login state.")
#         driver.save_screenshot('verify_login_failure.png')  # Save a screenshot for debugging
#         driver.quit()

# def handle_any_modal():
#     modal_elements = [
#         ('//button[text()="Sign in"]', 'Sign in button'),
#         ('//button[text()="Skip"]', 'Skip button'),
#         ('//button[text()="Join now"]', 'Join now button'),
#         ('//button[text()="Not now"]', 'Not now button')
#     ]
    
#     for xpath, description in modal_elements:
#         try:
#             button = WebDriverWait(driver, 5).until(
#                 EC.element_to_be_clickable((By.XPATH, xpath))
#             )
#             button.click()
#             time.sleep(2)
#             print(f"Handled '{description}' modal.")
#             return True
#         except TimeoutException:
#             continue
#         except NoSuchElementException as e:
#             print(f"Could not find '{description}': {e}")
    
#     print("No modals to handle.")
#     return False

# def scroll_to_load_all_comments():
#     SCROLL_PAUSE_TIME = 2
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(SCROLL_PAUSE_TIME)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

# def get_commenters(post_url):
#     try:
#         driver.get(post_url)
#         time.sleep(5)  # Adjust this wait as needed
#         commenters = []

#         while handle_any_modal():  # Handle any modal that may appear
#             pass

#         print("Scrolling to load all comments")
#         scroll_to_load_all_comments()
        
#         print("Waiting for the comments section to be present")
#         comments_section = WebDriverWait(driver, 120).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'comments-comments-list'))
#         )
#         print("Comments section found")

#         comments = comments_section.find_elements(By.CLASS_NAME, 'comments-comment-item')
#         print(f"Found {len(comments)} comments")

#         # for comment in comments:
#         #     try:
#         #         commenter_profile = comment.find_element(By.CSS_SELECTOR, '[aria-label="View Raj Kanojia’s profile"]')
#         #         profile_url = commenter_profile.get_attribute('href')
#         #         commenters.append(profile_url)
#         #         print(f"Commenter profile found: {profile_url}")
#         #     except NoSuchElementException:
#         #         print("No profile link found in this comment")
#         #         continue
#         for comment in comments:
#             commenter_profiles = comment.find_elements(By.CSS_SELECTOR, '[aria-label="View Raj Kanojia’s profile"]')
#             for commenter_profile in commenter_profiles:
#              profile_url = commenter_profile.get_attribute('href')
#              commenters.append(profile_url)
#              print(f"Commenter profile found: {profile_url}")


#     except TimeoutException:
#           print("Timeout: Comments section did not load in time.")
#     except NoSuchElementException as e:
#          print(f"Error: Unable to find an element: {e}")
#     except Exception as e:
#          print(f"An unexpected error occurred: {e}")

#     return commenters

# def send_direct_message(profile_url, message):
#     driver.get(profile_url)
#     time.sleep(3)  # Adjust this wait as needed

#     try:
#         message_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.CLASS_NAME, 'message-anywhere-button'))
#         )
#         message_button.click()
#         time.sleep(2)

#         message_box = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, 'msg-form__contenteditable'))
#         )
#         message_box.send_keys(message)

#         send_button = driver.find_element(By.CLASS_NAME, 'msg-form__send-button')
#         send_button.click()
#         time.sleep(2)
#         print(f"Message sent to {profile_url}")
#     except Exception as e:
#         print(f"Could not send message to {profile_url}: {e}")

# linkedin_login()
# time.sleep(2)  # Ensure the login completes and you are redirected properly

# verify_login()  # Verify the login was successful

# driver.get(POST_URL)  # Explicitly navigate to the post URL after login
# time.sleep(5)  # Allow some time for the page to load

# commenters = get_commenters(POST_URL)
# message_text = "Thank you for your comment on my post!"

for commenter in commenters:
    send_direct_message(commenter, message_text)

driver.quit()
