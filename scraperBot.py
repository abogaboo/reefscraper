from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import openpyxl

driver = webdriver.Chrome()
repo = openpyxl.load_workbook("repo.xlsx")

url = "https://www.statbotics.io/teams#breakdown"
driver.get(url)

def printSheet(rank, data):
    for colIndex, value in enumerate(data, start=1):
        repo.active.cell(row=rank, column=colIndex, value=value)

def scrapeAll(district): # 0 for peachtree, 1 for south carolina, 2 for north carolina
    repo.active = repo.worksheets[district]
    dropdown_element = driver.find_element(By.ID, "your_dropdown_id")
    select_object = Select(dropdown_element)
    
    match district:
        case 0:
            headerText = "Peachtree"
            numOfTeams = 74
        case 1:
            headerText = "South Carolina"
            numOfTeams = 34
        case 2:
            headerText = "North Carolina"
            numOfTeams = 86

    select_object.select_by_visible_text(headerText)
    
    for i in range(1, numOfTeams + 1):
        currEpaPath = f"/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/table/tbody/tr[{i}]/td[3]/div/div"
        currAutoEpaPath = f"" # ALL TO BE ADDED
        currTeleopEpaPath = f""
        currEndgameEpaPath = f""
        currAlgaePath = f""
        currL1Path = f""
        currL2Path = f""
        currL3Path = f""
        currL4Path = f""

        epa = driver.find_element(By.XPATH, currEpaPath).text
        autoEpa = driver.find_element(By.XPATH, currAutoEpaPath).text
        teleopEpa = driver.find_element(By.XPATH, currTeleopEpaPath).text
        endgameEpa = driver.find_element(By.XPATH, currEndgameEpaPath).text
        algae = driver.find_element(By.XPATH, currAlgaePath).text
        l1 = driver.find_element(By.XPATH, currL1Path).text
        l2 = driver.find_element(By.XPATH, currL2Path).text
        l3 = driver.find_element(By.XPATH, currL3Path).text
        l4 = driver.find_element(By.XPATH, currL4Path).text

        data = [epa, autoEpa, teleopEpa, endgameEpa, algae, l1, l2, l3, l4]
        printSheet(repo.active, i, data)

    repo.save("repo.xlsx")

