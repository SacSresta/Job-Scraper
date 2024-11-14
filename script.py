from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

jobname = input("Please enter a job title")

# Set up Chrome options
chrome_options = Options()

# Initialize Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

# Perform operations with the driver
driver.get("https://www.seek.com.au/")
print("Page title is:", driver.title)  # Print the title of the page

assert "SEEK" in driver.title
print("Assertion passed: SEEK is in the title.")

# Search for a job
elem = driver.find_element(By.NAME, "keywords")
elem.clear()
elem.send_keys(jobname)
location = driver.find_element(By.NAME, "where")
location.send_keys('Queensland')
elem.send_keys(Keys.RETURN)

# Wait for the page to load
time.sleep(5)

# Save the original search URL
original_url = driver.current_url

# List to store job data
job_data = []

# Loop through the first 3 pages
for page in range(1, 15):
    # Construct the URL with the page number
    paginated_url = f"{original_url.split('?page=')[0]}?page={page}"
    print(f"Navigating to page {page}: {paginated_url}")
    
    # Navigate to the paginated URL
    driver.get(paginated_url)
    
    # Wait for the jobs to load
    try:
        WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-automation="normalJob"]'))
        )
    except TimeoutException:
        print(f"Page {page} took too long to load. Skipping...")
        continue

    print(f"Scraping page {page}")

    # Extract job details
    job_cards = driver.find_elements(By.CSS_SELECTOR, 'article[data-automation="normalJob"]')
    for job in job_cards:
        try:
            # Extract job title
            title_element = job.find_element(By.CSS_SELECTOR, 'a[data-automation="jobTitle"]')
            title = title_element.text

            # Extract company name
            company_element = job.find_element(By.CSS_SELECTOR, 'a[data-automation="jobCompany"]')
            company = company_element.text

            # Extract job location
            location_element = job.find_element(By.CSS_SELECTOR, 'a[data-automation="jobLocation"]')
            location = location_element.text

            # Extract job link
            job_link = title_element.get_attribute('href')

            # Store job data
            job_data.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Link": job_link
            })

            # Print the job details
            print(f"Title: {title}\nCompany: {company}\nLocation: {location}\nLink: {job_link}\n")
        except NoSuchElementException as e:
            print("A required element is missing. Skipping this job.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Quit the driver
driver.quit()

# Convert to pandas DataFrame
df = pd.DataFrame(job_data)

# Save to CSV
df.to_csv("job_listings.csv", index=False)
print("Job data saved to job_listings.csv")
