from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from time import sleep

driver = webdriver.Chrome()

driver.maximize_window()

driver.get("https://plposweb.vancouver.ca/Public/Default.aspx?PossePresentation=PermitSearchByDate")
from_field = driver.find_element(By.ID, "CreatedDateFrom_1018439_S0")
from_field.send_keys("Jan 1, 2024")
from_field.send_keys(Keys.ENTER)

to_field = driver.find_element(By.ID, "CreatedDateTo_1018439_S0")
to_field.send_keys("Mar 30, 2024")
to_field.send_keys(Keys.ENTER)

type_field = driver.find_element(By.ID, "ObjectDefDescription_1018439_S0")
type_field.send_keys("Development Permit")
type_field.send_keys(Keys.ENTER)

#driver.find_element(By.ID, "ctl00_cphBottomFunctionBand_ctl03_PerformSearch").click()

sleep(2)
driver.save_screenshot("test.png")

table = driver.find_element(By.TAG_NAME, "table")

header = table.find_element(By.TAG_NAME, "thead")
header_values = ["link"]
for elem in header.find_elements(By.TAG_NAME, "th")[1:]:
    header_values.append(elem.text)
    
rows = []
for row in table.find_elements(By.TAG_NAME, "tbody")[:-1]:
    cells = row.find_elements(By.TAG_NAME, "td")

    link = cells[0].find_element(By.TAG_NAME, "a").get_dom_attribute("href")
    values = [link]
    values.extend([cell.text for cell in cells[1:]])
    rows.append(values)

df = pd.DataFrame(rows, columns = header_values)

print(df)
