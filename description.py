from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Load data from CSV
df = pd.read_csv('Analyst.csv')
links = df[['Title', 'Link']]

# Configure Chrome options
chrome_options = Options()

# List to store results
loop_list = []

# Initialize Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)

for index, row in links.iterrows():
    print(f"Processing: {row['Title']} - {row['Link']}")

    try:
        # Navigate to the link
        driver.get(str(row['Link']))
        
        # Try to find the description within a <section> tag
        description = driver.find_element(By.TAG_NAME, "section")
        
        # Append title and description to the list
        loop_list.append({
            "Title": row['Title'],
            "Description": description.text
        })

    except NoSuchElementException:
        print(f"Description not found for link: {row['Link']}")
        # Append title with a placeholder description
        loop_list.append({
            "Title": row['Title'],
            "Description": "Description not found"
        })

# Quit the driver
driver.quit()

# Create a DataFrame from the list
result_df = pd.DataFrame(loop_list)

# Save to a new CSV file
result_df.to_csv('Descriptions.csv', index=False)

print("Descriptions saved to 'Descriptions.csv'.")
