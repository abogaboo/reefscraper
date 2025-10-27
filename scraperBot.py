from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import openpyxl

driver = webdriver.Chrome()
repo = openpyxl.load_workbook("repo.xlsx")

insights_url = "https://www.statbotics.io/teams#insights"
breakdown_url = "https://www.statbotics.io/teams#breakdown"
district_dropdown_css = "#react-select-filter-selectdistrict-input"
paginate_dropdown_css = "#react-select-paginate-select-input"
district_dropdown_xpath = "/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[1]/div/div[4]/div/div[1]/div[2]/input"
paginate_dropdown_xpath = "/html/body/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/div[3]/div/div/div[1]/div[2]/div/div[1]/div[2]/input"

def print_sheet(rank, data):
    for colIndex, value in enumerate(data, start = 1):
        repo.active.cell(row = rank, column = colIndex + 2, value = value)

def type_in_dropdown_insights(css_selector, text):
    dropdown = driver.find_element(By.CSS_SELECTOR, css_selector)
    dropdown.click()
    dropdown.send_keys(text)
    dropdown.send_keys(Keys.ENTER)

def type_in_dropdown_breakdown(xpath, text):
    dropdown = driver.find_element(By.XPATH, xpath)
    dropdown.click()
    dropdown.send_keys(text)
    dropdown.send_keys(Keys.ENTER)

def prep(district):
    repo.active = repo.worksheets[district]
    match district:
            case 0:
                district_text = "Peachtree"
                num_of_teams = 74
            case 1:
                district_text = "South Carolina"
                num_of_teams = 34
            case 2:
                district_text = "North Carolina"
                num_of_teams = 86

    # INSIGHTS PAGE
    driver.get(insights_url) # opens insights in primary tab
    time.sleep(1) # delay for letting elements load
    type_in_dropdown_insights(district_dropdown_css, district_text)
    type_in_dropdown_insights(paginate_dropdown_css, "100")

    # BREAKDOWN PAGE
    driver.execute_script("window.open('https://www.statbotics.io/teams#breakdown', '_blank');") # opens breakdown page in secondary tab
    time.sleep(1) # delay for letting elements load
    driver.switch_to.window(driver.window_handles[1]) # switch to breakdown page
    type_in_dropdown_breakdown(district_dropdown_xpath, district_text)
    type_in_dropdown_breakdown(paginate_dropdown_xpath, "100")
    
    return num_of_teams

def scrape_all_teams(district): # 0 for peachtree, 1 for south carolina, 2 for north carolina
    num_of_teams = prep(district)
    for i in range(1, num_of_teams + 1):
        # GETTING EPA DATA:
        driver.switch_to.window(driver.window_handles[0]) # switch to insights page
        curr_epa_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[5]/div[1]/div[1]"
        curr_auto_epa_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[6]/div[1]/div[1]"
        curr_teleop_epa_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[7]/div[1]/div[1]"
        curr_endgame_epa_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[8]/div[1]/div[1]"
        epa = driver.find_element(By.XPATH, curr_epa_path).text
        auto_epa = driver.find_element(By.XPATH, curr_auto_epa_path).text
        teleop_epa = driver.find_element(By.XPATH, curr_teleop_epa_path).text
        endgame_epa = driver.find_element(By.XPATH, curr_endgame_epa_path).text

        # GETTING ALGAE AND CORAL DATA:
        driver.switch_to.window(driver.window_handles[1]) # switch to breakdown page
        curr_algae_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[6]/div[1]/div[1]"
        curr_l1_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[9]/div[1]/div[1]"
        curr_l2_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[10]/div[1]/div[1]"
        curr_l3_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[11]/div[1]/div[1]"
        curr_l4_path = f"/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/table[1]/tbody[1]/tr[{i}]/td[12]/div[1]/div[1]"
        algae = driver.find_element(By.XPATH, curr_algae_path).text
        l1 = driver.find_element(By.XPATH, curr_l1_path).text
        l2 = driver.find_element(By.XPATH, curr_l2_path).text
        l3 = driver.find_element(By.XPATH, curr_l3_path).text
        l4 = driver.find_element(By.XPATH, curr_l4_path).text

        data = [epa, auto_epa, teleop_epa, endgame_epa, algae, l1, l2, l3, l4] # aggregate data into a list
        print_sheet(i, data) # print list to excel sheet
        print(i, data)
    repo.save("repo.xlsx")
    driver.quit()
    curr_time = str(datetime.now())
    print("Finished at " + curr_time)

scrape_all_teams(0)
driver = webdriver.Chrome()
scrape_all_teams(1)
driver = webdriver.Chrome()
scrape_all_teams(2)
repo.active = repo.worksheets[0]

