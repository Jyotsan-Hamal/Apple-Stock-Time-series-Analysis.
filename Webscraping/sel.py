from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd



options = webdriver.FirefoxOptions()
options.add_argument("-headless")


driver = webdriver.Firefox(options=options)
def dictionary_to_dataframe(dictionary:dict):
    
    return pd.DataFrame(dictionary)

def page_source_to_dataframe(page_html):
    soup = BeautifulSoup(page_html, 'html.parser')
    one = soup.find_all('div',class_ = 'col-md-10')
    tr = one[1].find_all('tr')
    # Create a list to save data for each column
    index = []
    date = []
    Open = []
    High = []
    Low = []
    Ltp = []
    per_change = []
    Quantity = []
    turnover = []
    for i in range(12,62): #from list of table row => 'tr' the index -> 1 starts from 12 to 62 which is 50 rows of data
        index.append(tr[i].find_all('td')[0].text.strip())
        date.append(tr[i].find_all('td')[1].text.strip())
        Open.append(tr[i].find_all('td')[2].text.strip())
        High.append(tr[i].find_all('td')[3].text.strip())
        Low.append(tr[i].find_all('td')[4].text.strip())
        Ltp.append(tr[i].find_all('td')[5].text.strip())
        per_change.append(tr[i].find_all('td')[6].text.strip())
        Quantity.append(tr[i].find_all('td')[7].text.strip())
        turnover.append(tr[i].find_all('td')[8].text.strip())


    df = dictionary_to_dataframe({
        'Index':index,
        'Date':date,
        'Open':Open,
        'High':High,
        'Low':Low,
        'Ltp':Ltp,
        '% change':per_change,
        'turnover':turnover
    })

    return df



driver.get("https://www.sharesansar.com/company/hidcl")

price_history_xpath = "/html/body/div[2]/div/section[2]/div[3]/div/div/div/div[2]/div/div[1]/div[1]/ul/li[8]"
button = driver.find_element(By.XPATH,price_history_xpath)
button.click()
fifty_xpath = "/html/body/div[2]/div/section[2]/div[3]/div/div/div/div[2]/div/div[1]/div[2]/div/div[8]/div/div/div[1]/label/select/option[3]"
button = driver.find_element(By.XPATH,fifty_xpath)
button.click()
time.sleep(2)
# Get the HTML content of the page after clicking the button
page_html = driver.page_source
df = page_source_to_dataframe(page_html=page_html)
print(df)
driver.quit()