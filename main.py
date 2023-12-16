from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pandas

list_role, list_company, list_location, list_salary, list_link = [
], [], [], [], []

opsi = webdriver.ChromeOptions()
opsi.add_argument('--headless')
servis = Service('chromedriver.exe')
driver = webdriver.Chrome(service=servis, options=opsi)

link_scrap = "https://www.jobstreet.co.id"
# jobs_role = "IT Support"
# jobs_location = "Bandung"
driver.maximize_window()
driver.get(link_scrap)
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[5]/div/div[1]/div/div/div/div[1]/section/div[2]/form/div[3]/div[3]/div/button")))
    print(f"Web Was Successfully Accessed")
    jobs_role = input("Please input your job position : ")
    jobs_location = input("Please input location you want : ")
except:
    print("Web Couldn't Access Successfully")
input_role = driver.find_element(
    By.XPATH, "/html/body/div[1]/div/div[5]/div/div[1]/div/div/div/div[1]/section/div[2]/form/div[3]/div[1]/div/div/div[1]/div/div/div[2]/div[1]/div/div[2]/div/div/input")
input_role.send_keys(jobs_role)
input_location = driver.find_element(
    By.XPATH, "/html/body/div[1]/div/div[5]/div/div/div/div/div/div[1]/section/div[2]/form/div[3]/div[2]/div/div/div[2]/div[1]/div/div[2]/div/div/input")
input_location.send_keys(jobs_location)
driver.find_element(
    By.XPATH, "/html/body/div[1]/div/div[5]/div/div/div/div/div/div[1]/section/div[2]/form/div[3]/div[3]/div/button").click()
# next page
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[5]/div/section/div[2]/div/div/div/div/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div/h1")))

content = driver.page_source  # Get data from browser

driver.quit()

# Scrape
data = BeautifulSoup(content, "html.parser")

for container in data.find_all("article", class_="_1wkzzau0 _1wkzzau1 a1msqi7i a1msqi6e a1msqi9q a1msqi8m a1msqi66 a1msqih a1msqi5e uo6mkb a1msqi4i a1msqi4b lnocuo18 lnocuo1b a1msqi32 a1msqi35"):
    # Sesuaikan dengan tag HTML pada web yang di scraping
    position = container.find(
        "h3", class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuol _1d0g9qk4 lnocuov lnocuo21").get_text()
    company = container.find(
        "span", class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuo1 lnocuo21 _1d0g9qk4 lnocuoa").get_text()
    location = container.find(
        "span", class_="_1wkzzau0 a1msqi4y lnocuo0 lnocuo1 lnocuo21 _1d0g9qk4 lnocuo7").get_text()
    salary = container.find(
        "span", class_="_1wkzzau0 _16v7pfz1 a1msqi4y a1msqi0 a1msqir _16v7pfz3")

    if salary != None:
        salary = salary.get_text()

    link = f"{link_scrap}" + container.find("a")["href"]

    print(position)
    print(company)
    print(location)
    print(salary)
    print(link)
    print("--------------------------------\n")

    list_role.append(position)
    list_company.append(company)
    list_location.append(location)
    list_salary.append(salary)
    list_link.append(link)

# Convert to excel
df = pandas.DataFrame({'Position': list_role, 'Company': list_company,
                       'Location': list_location, 'Salary': list_salary, "Detail": list_link})
df.to_excel(f'{jobs_role}-{jobs_location}.xlsx', index=False)
print(f'{jobs_role}-{jobs_location}.xlsx successfully downloaded')
