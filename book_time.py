# LIBRARIES ####
# Playwright Libraries and Anti-bot Measures
from playwright.sync_api import Playwright, sync_playwright

# Browser fingerprint injection to bypass Duo 2FA
from browserforge.injectors.playwright import NewContext
from browserforge.fingerprints import FingerprintGenerator

## Human-like cursor movement to bypass Duo 2FA
from python_ghost_cursor.playwright_sync import create_cursor

# Other tools
from datetime import datetime, timedelta, date
import time
import random

# PARAMETERS ##############################################################

# CWL Login
username = "****"
password = "****"

# Court Number
court = 11

# Attendees
attendees = 4

# Booking Time (For Tomorrow) (24hr clock)
booking_time = 12

# Google Chrome Application Path
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

#############################################################################

# Pre-process inputs into correct formats ####
# Format time_str as "HH:MM AM/PM-HH:MM AM/PM"
start_dt = datetime.strptime(f"{booking_time:02d}:00", "%H:%M")
end_dt = start_dt + timedelta(hours=1)
time_str = f"{start_dt.strftime('%I:%M %p')}-{end_dt.strftime('%I:%M %p')}"

# Set time_execute to today at booking_time (24 hours before the booking)
today = date.today()
time_execute = datetime(today.year, today.month, today.day, booking_time, 0, 0)
time_login = time_execute - timedelta(minutes = 3)

# DEFINE CONSTANTS ####
# Court booking urls
urls = [
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=c0668c1c-1fd6-4432-a20e-4c50aaad5baa&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=e2d99dda-cdc4-4af4-8df6-6c8061ffd56f&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=c117a102-0ba0-4aa8-b8cf-eb8a1480be55&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=47f78e62-2ac0-4d39-8ffa-5d331f60e14e&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=e5432c07-c2a6-46d1-a5d7-25c58567046c&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=f7000b6c-0d93-472b-97af-e0f22915439f&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=5dac0879-1fbb-4dfe-ac67-5dcaa925d2f5&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=ccbf3aa0-f263-44eb-b394-a603115f587a&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=9f475d76-dbc1-463e-9097-210f31681e2f&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=d5894b7a-2b61-4345-a1a8-ea8a50c921ae&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=d3a55644-6681-42a7-b8f5-09d796d35c07&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=00dc0e70-6536-4a5a-b60b-9f6b0d0ba050&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e",
    "https://ubc.perfectmind.com/24063/Clients/BookMe4LandingPages/Facility?facilityId=308fd9d5-0de2-442e-8bd7-3fa6b607d170&widgetId=c7c36ee3-2494-4de2-b2cb-d50a86487656&calendarId=e65c1527-c4f8-4316-b6d6-3b174041f00e"
]

# HELPER FUNCTIONS ####

# Function: human_sleep
# Purpose: To simulate random, human-like delays using time.sleep for a random amount of time between min_sec and max_sec
# Inputs:
# - min_sec (float): minimum time in seconds for random sleep
# - max_sec (float): maximum time in seconds for random sleep
# Outputs:
# - N/A
def human_sleep(min_sec=0.5, max_sec=0.8):
    time.sleep(random.uniform(min_sec, max_sec))

# Function: slow_type
# Purpose: To simulate human-like typing
# Inputs:
# - min_sec (float): minimum time in seconds for pause between typed characters
# - max_sec (float): maximum time in seconds for pause between typed characters
# Outputs:
# - N/A
def slow_type(element, text, min_sec=0.1, max_sec=0.2):
    for char in text:
        element.type(char, delay=random.randint(int(min_sec * 1000), int(max_sec * 1000)))
    human_sleep()

# PLAYWRIGHT FUNCTIONS ####
# Function: launch_chrome
# Purpose: Launch an instance of google chrome and save playwright objects for later use
# Inputs:
# - playwright (Playwright): playwright object
# - chrome_path (str): Path to chrome application
# - fingerprint (FingerprintGenerator fingerprint object): Browser fingerprint for anti-bot measures
# Outputs:
# - browser (Playwright browser object)
# - page (Playwright page object)
# - context (Playwright context object)
def launch_chrome(playwright: Playwright, chrome_path, fingerprint):
    browser = playwright.chromium.launch(
        headless = False,
        executable_path = chrome_path,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    )

    context = NewContext(browser, fingerprint = fingerprint)
    page = context.new_page()

    return browser, page, context

# Function: cwl_login
# Purpose: Log-in to CWL. Ensure that DUO 2FA has been previously "remembered" on browser and that no additional 2FA measures are enabled, such as a passkey.
# Inputs:
# - playwright (Playwright): playwright object
# - username (str): CWL username
# - password (str): CWL password
# - page (Playwright page object)
# Outputs:
# N/A
def cwl_login(playwright: Playwright, username, password, page) -> None:
    # Create cursor
    cursor = create_cursor(page)
    
    # Login to CWL in a human-like way
    login_button = page.get_by_role("link", name="Login")
    login_button.wait_for()
    cursor.click(login_button)

    human_sleep()

    cwl_login_button = page.get_by_role("link", name="CWL Login")
    cwl_login_button.wait_for()
    cursor.click(cwl_login_button)

    human_sleep()

    login_box = page.get_by_role("textbox", name = "Login Name")
    cursor.click(login_box)
    slow_type(login_box, username)

    human_sleep()

    password_box = page.get_by_role("textbox", name = "Password")
    cursor.click(password_box)
    slow_type(password_box, password)

    submit_cwl = page.get_by_role("button", name = "Login")
    cursor.click(submit_cwl)

# Function: checkout
# Purpose: Reserve court booking and checkout
# Inputs:
# - playwright (Playwright): playwright object
# - attendees (int): number of attendees for court booking (1-4)
# - time_str (str): character string defining the booking time, based on booking_time
# - page (Playwright page object)
# Outputs:
# N/A
def checkout(playwright: Playwright, attendees, time_str, page) -> None:
    # Set number of attendees
    button = page.get_by_role("button", name="Increase value")
    button.wait_for(state = "visible", timeout = 30000)

    for i in range(attendees):
        button.click()

    # Click "Book Now" for chosen time slot
    page.wait_for_selector(f'span[title="{time_str}"]', timeout = 30000)
    page.click(f'span[title="{time_str}"]')

    # Click "Reserve"
    page.wait_for_selector('button.button-book[name="book-button"]:not(.disabledBookButton)', timeout = 30000)
    page.click('button.button-book[name="book-button"]')

    # Click "Next"
    page.wait_for_load_state("domcontentloaded")
    next_button = page.get_by_text("Next")
    next_button.click()

    # ADD CODE HERE TO MAKE PAYMENT
    # pay_button = page.get_by_role("button", name = "Place My Order")
    # pay_button.wait_for(state="visible")
    # pay_button.click()

# RUN BOT ####
with sync_playwright() as playwright:
    # Define court url
    court_url = urls[court - 1]

    # Define browser fingerprint
    fingerprint = FingerprintGenerator().generate(browser='chrome', os='windows')

    # Wait until 3-minutes before booking opens to launch browser and login to CWL
    while datetime.now() < time_login:
        print("waiting")
        time.sleep(10)
    
    # Launch chrome browser
    browser, page, context = launch_chrome(playwright, chrome_path, fingerprint)

    # Navigate to page
    page.goto(court_url, wait_until="domcontentloaded")

    # Login to CWL
    cwl_login(playwright, username, password, page)

    # Wait for Login
    page.wait_for_url("**/24063/Clients/BookMe4LandingPages/**")

    # Wait until time is 24hrs before reserve time
    while datetime.now() < time_execute:
        time.sleep(1)

    # Reload page to refresh available times
    page.reload()

    # Reserve and Check-out
    checkout(playwright, attendees, time_str, page)

    input("Press Enter to close the browser...")
    context.close()
    browser.close()
    
    
