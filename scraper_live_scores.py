from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the Sofascore live scores page
url = "https://www.sofascore.com/football/live"
driver.get(url)

# Extract match details using Selenium
matches = driver.find_elements(By.CLASS_NAME, "event_cell")
for match in matches:
    try:
        left_team = match.find_element(By.CSS_SELECTOR, "[data-testid='left_team']").text.strip()
        right_team = match.find_element(By.CSS_SELECTOR, "[data-testid='right_team']").text.strip()
        scores = match.find_elements(By.CLASS_NAME, "currentScore")
        if scores:
            left_score = scores[0].text.strip()
            right_score = scores[1].text.strip()
        else:
            left_score, right_score = "N/A", "N/A"
        print(f"{left_team} {left_score} - {right_score} {right_team}")
    except Exception as e:
        print(f"Error extracting match: {e}")

# Close the browser
driver.quit()
