from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import os
import csv

#change this driver path
DRIVER_PATH = '/Users/malaikasheikh/python/chromedriver'
Street_name = "YORK ST"

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

driver.get('https://assessors.portlandmaine.gov/forms/htmlframe.aspx?mode=content/home.htm')
time.sleep(2)

link = driver.find_element_by_link_text("Search For Property Records")
link.click()
time.sleep(2)

# Check if the disclaimer page appears and click "Agree" if it does
disclaimer_page_url = "https://assessors.portlandmaine.gov/Search/Disclaimer.aspx?FromUrl=../search/commonsearch.aspx?mode=realprop"
if driver.current_url == disclaimer_page_url:
    agree_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btAgree"))
    )
    agree_button.click()
    time.sleep(2)


# Enter "Cumberland" in the "Street" field
street_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "inpStreet"))
)
street_field.clear()
street_field.send_keys(Street_name)

a = input("press any key to continue: ")

# Click the "Search" button
search_button = driver.find_element_by_id("btSearch")
search_button.click()
time.sleep(4)

def get_rows():
    result_table = driver.find_element(By.XPATH, "//table[@id='searchResults']")
    result_rows = result_table.find_elements(By.TAG_NAME, "tr")
    return result_rows

def side_menu_tags():
    side_menu = driver.find_element(By.XPATH, "//div[@id='sidemenu']")
    a_tags = side_menu.find_elements(By.TAG_NAME, "a")
    return a_tags

def get_profile_details():
    data = {"Street Name":Street_name,"Parcel ID":[],"Property Location":[],"Unit":[],"Living Unit":[],"Land Use Code":[],"Zoning":[],
            "Land Area (acreage)":[],"Land Area (square footage)":[],"Notes":[],"Utilities":[],"Owner":[],
            "Address":[],"City, State, Zip":[],"Deed Date":[],"Book":[],"Page":[]}
    try:
        parcel_table = driver.find_element(By.XPATH, "//table[@id='Parcel']")
        parcel_data = parcel_table.find_elements(By.TAG_NAME, "tr")
        # extraction of data for parcel
        current_attribute = "Parcel ID"
        for tr in parcel_data:
                try:
                    td_tags = tr.find_elements(By.TAG_NAME, "td")
                    if(td_tags[0].text != " "):
                        current_attribute = td_tags[0].text
                        data[current_attribute].append(td_tags[1].text)
                    else:
                        data[current_attribute].append(td_tags[1].text)
                except Exception as e:
                    print(e)
                    pass
    except:
        pass
    #extraction of data for owner
    try:
        owner_table = driver.find_element(By.XPATH, "//table[@id='Owners']")
        owner_data = owner_table.find_elements(By.TAG_NAME, "tr")

        for tr in owner_data:
                try:
                    td_tags = tr.find_elements(By.TAG_NAME, "td")
                    if(td_tags[0].text != " "):
                        current_attribute = td_tags[0].text
                        data[current_attribute].append(td_tags[1].text)
                    else:
                        data[current_attribute].append(td_tags[1].text)
                except Exception as e:
                    pass
    except:
        pass
    city = data["City, State, Zip"]
    data["City State Zip"] = city
    del data["City, State, Zip"]
    return data

def get_values_details():
    data = {"Land":[],"Building":[],"Total":[],"Homestead / Veterans Exemption":[],"Other Exemptions":[],"Taxable Value":[],
           "Tax Amount":[]}
    try:
        values_table = driver.find_element(By.XPATH, "//table[@id='Assessed Values']")
        values_data = values_table.find_elements(By.TAG_NAME, "tr")
        values_data = values_data[0:9]
        # extraction of data for parcel
        current_attribute = "Land"
        for tr in values_data:
                try:
                    td_tags = tr.find_elements(By.TAG_NAME, "td")
                    if(td_tags[0].text != " "):
                        current_attribute = td_tags[0].text
                        data[current_attribute].append(td_tags[1].text)
                    else:
                        data[current_attribute].append(td_tags[1].text)
                except Exception as e:
                    print(e)
                    pass
    except:
        pass
    return data

def get_residential_details():
    data = {"Card":[],"Style":[],"Year Built":[],"Stories":[],"Attic":[],"Fuel Type":[],
            "Heat System":[],"Heat/AC Type":[],"Fireplaces":[],"Total Rooms":[],"Bedrooms":[],
            "Full Baths":[],"Half Baths":[],"Basement":[],"Basement Garage Spaces":[],
            "Finished Basement Area":[],"Basement Rec Room Area":[],"Unfinished/Cathedral Area":[],"Living Area":[]}
    try:
        residential_table = driver.find_element(By.XPATH, "//table[@id='Residential']")
        residential_data = residential_table.find_elements(By.TAG_NAME, "tr")
        current_attribute = "Card"
        for tr in residential_data:
                try:
                    td_tags = tr.find_elements(By.TAG_NAME, "td")
                    if(td_tags[0].text != " "):
                        current_attribute = td_tags[0].text
                        data[current_attribute].append(td_tags[1].text)
                    else:
                        data[current_attribute].append(td_tags[1].text)
                except Exception as e:
                    pass
    except:
        pass
    data['Residential Card'] = data.pop('Card')
    data['Residential Style'] = data.pop('Style')
    data['Residential Year Built'] = data.pop('Year Built')
    data['Residential Stories'] = data.pop('Stories')
    data['Residential Attic'] = data.pop('Attic')
    data['Residential Fuel Type'] = data.pop('Fuel Type')
    data['Residential Heat System'] = data.pop('Heat System')
    data['Residential Heat/AC Type'] = data.pop('Heat/AC Type')
    data['Residential Fireplaces'] = data.pop('Fireplaces')
    data['Residential Total Rooms'] = data.pop('Total Rooms')
    data['Residential Bedrooms'] = data.pop('Bedrooms')
    data['Residential Full Baths'] = data.pop('Full Baths')
    data['Residential Half Baths'] = data.pop('Half Baths')
    data['Residential Basement'] = data.pop('Basement')
    data['Residential Basement Garage Spaces'] = data.pop('Basement Garage Spaces')
    data['Residential Finished Basement Area'] = data.pop('Finished Basement Area')
    data['Residential Basement Rec Room Area'] = data.pop('Basement Rec Room Area')
    data['Residential Unfinished/Cathedral Area'] = data.pop('Unfinished/Cathedral Area')
    data['Residential Living Area'] = data.pop('Living Area')
    return data

def get_sales_details():
    data = {"Date":[],"Price":[],"Grantee":[],"Grantor":[],"Sales Book":[],"Sales Page":[]}
    try:
        sales_table = driver.find_element(By.XPATH, "//table[@id='Sales History']")
        sales_data = sales_table.find_elements(By.TAG_NAME, "tr")
        sales_data = sales_data[1:]
        for tr in sales_data:
            td_tags = tr.find_elements(By.TAG_NAME, "td")
            data["Date"].append(td_tags[0].text)
            data["Price"].append(td_tags[1].text)
            data["Grantee"].append(td_tags[2].text)
            data["Grantor"].append(td_tags[3].text)
            data["Sales Book"].append(td_tags[4].text)
            data["Sales Page"].append(td_tags[5].text)
    except:
        pass
    return data

def get_commercial_details():
    data = {"Card":[],"Building Number":[],"Structure Code/Description":[],"Improvement Name":[],
            "Units":[],"# of Identical Buildings":[],"Year Built":[],"Gross SF (including basement)":[],
            "Commercial Building Data Card":[],"Commercial Building Data Line":[],"Commercial Building Data From Floor":[],
            "Commercial Building Data To Floor":[],"Commercial Building Data Area":[],"Commercial Building Data Use Group":[],
            "Commercial Building Data Exterior Walls":[],"Commercial Building Data Wall Height":[],"Commercial Building Data Heating":[],
            "Commercial Other Features Card":[],"Commercial Other Features Int/Ext Line":[],"Commercial Other Features Structure":[],
            "Commercial Other Features Measurement 1":[],"Commercial Other Features Measurement 2":[],"Commercial Other Features identical Units":[]}
    # Building Description Data
    try:
        commercial_table = driver.find_element(By.XPATH, "//table[@id='Building Description']")
        commercial_data = commercial_table.find_elements(By.TAG_NAME, "tr")
        current_attribute = "Card"
        for tr in commercial_data:
                try:
                    td_tags = tr.find_elements(By.TAG_NAME, "td")
                    if(td_tags[0].text != " "):
                        current_attribute = td_tags[0].text
                        data[current_attribute].append(td_tags[1].text)
                    else:
                        data[current_attribute].append(td_tags[1].text)
                except Exception as e:
                    pass
    except:
        pass
    # Building Data details
    try:
        building_data_table = driver.find_element(By.XPATH, "//table[@id='Building Data']")
        building_data_data = building_data_table.find_elements(By.TAG_NAME, "tr")
        building_data_data = building_data_data[1:]
        for tr in building_data_data:
            td_tags = tr.find_elements(By.TAG_NAME, "td")
            data["Commercial Building Data Card"].append(td_tags[0].text)
            data["Commercial Building Data Line"].append(td_tags[1].text)
            data["Commercial Building Data From Floor"].append(td_tags[2].text)
            data["Commercial Building Data To Floor"].append(td_tags[3].text)
            data["Commercial Building Data Area"].append(td_tags[4].text)
            data["Commercial Building Data Use Group"].append(td_tags[5].text)
            data["Commercial Building Data Exterior Walls"].append(td_tags[6].text)
            data["Commercial Building Data Wall Height"].append(td_tags[7].text)
            data["Commercial Building Data Heating"].append(td_tags[8].text)
    except:
        pass

    # Other Feature Details
    try:
        other_data_table = driver.find_element(By.XPATH, "//table[@id='Other Feature Details']")
        other_data = other_data_table.find_elements(By.TAG_NAME, "tr")
        other_data = other_data[1:]
        for tr in other_data:
            td_tags = tr.find_elements(By.TAG_NAME, "td")
            data["Commercial Other Features Card"].append(td_tags[0].text)
            data["Commercial Other Features Int/Ext Line"].append(td_tags[1].text)
            data["Commercial Other Features Structure"].append(td_tags[2].text)
            data["Commercial Other Features Measurement 1"].append(td_tags[3].text)
            data["Commercial Other Features Measurement 2"].append(td_tags[4].text)
            data["Commercial Other Features identical Units"].append(td_tags[5].text)
    except:
        pass

    data['Commercial Building Description Card'] = data.pop('Card')
    data['Commercial Building Description Building Number'] = data.pop('Building Number')
    data['Commercial Building Description Structure Code/Description'] = data.pop('Structure Code/Description')
    data['Commercial Building Description Improvement Name'] = data.pop('Improvement Name')
    data['Commercial Building Description Units'] = data.pop('Units')
    data['Commercial Building Description # of Identical Buildings'] = data.pop('# of Identical Buildings')
    data['Commercial Building Description Year Built'] = data.pop('Year Built')
    data['Commercial Building Description Gross SF (including basement)'] = data.pop('Gross SF (including basement)')
    return data

def get_assesment_history_details():
    data = {"History Year":[],"History Land":[],"History Building":[],"History Total":[],"History Standard Exemption":[],"History Other Exemption":[],
            "History Taxable Value":[]}
    try:
        history_table = driver.find_element(By.XPATH, "//table[@id='Assessment History']")
        history_data = history_table.find_elements(By.TAG_NAME, "tr")
        history_data = history_data[1:]
        for tr in history_data:
            td_tags = tr.find_elements(By.TAG_NAME, "td")
            data["History Year"].append(td_tags[0].text)
            data["History Land"].append(td_tags[1].text)
            data["History Building"].append(td_tags[2].text)
            data["History Total"].append(td_tags[3].text)
            data["History Standard Exemption"].append(td_tags[4].text)
            data["History Other Exemption"].append(td_tags[5].text)
            data["History Taxable Value"].append(td_tags[6].text)
    except:
        pass
    return data

def save_data(profile_data,values_data,sales_data,residential_data,commercial_data,history_data):
    file_path = 'data.csv'
    if not os.path.isfile(file_path):
    # Create a new DataFrame with desired columns
        column_names = ["Street Name","Parcel ID", "Property Location", "Unit","Living Unit","Land Use Code","Zoning",
            "Land Area (acreage)","Land Area (square footage)","Notes","Utilities","Owner","Address",
            "Deed Date","Book","Page","City State Zip","Land","Building","Total","Homestead / Veterans Exemption",
            "Other Exemptions","Taxable Value","Tax Amount","Date","Price","Grantee","Grantor","Sales Book",
            "Sales Page",'Residential Card', 'Residential Style', 'Residential Year Built', 
            'Residential Stories', 'Residential Attic', 'Residential Fuel Type', 
            'Residential Heat System', 'Residential Heat/AC Type', 'Residential Fireplaces', 
            'Residential Total Rooms', 'Residential Bedrooms', 'Residential Full Baths', 
            'Residential Half Baths', 'Residential Basement', 'Residential Basement Garage Spaces',
            'Residential Finished Basement Area','Residential Basement Rec Room Area', 'Residential Unfinished/Cathedral Area',
            'Residential Living Area','Commercial Building Data Card', 'Commercial Building Data Line',
            'Commercial Building Data From Floor','Commercial Building Data To Floor', 'Commercial Building Data Area',
            'Commercial Building Data Use Group','Commercial Building Data Exterior Walls', 'Commercial Building Data Wall Height', 'Commercial Building Data Heating'
            ,'Commercial Other Features Card','Commercial Other Features Int/Ext Line', 'Commercial Other Features Structure',
            'Commercial Other Features Measurement 1', 'Commercial Other Features Measurement 2', 'Commercial Other Features identical Units', 'Commercial Building Description Card',
            'Commercial Building Description Building Number', 'Commercial Building Description Structure Code/Description',
            'Commercial Building Description Improvement Name', 'Commercial Building Description Units',
            'Commercial Building Description # of Identical Buildings',
            'Commercial Building Description Year Built', 'Commercial Building Description Gross SF (including basement)',
            "History Year","History Land","History Building","History Total","History Standard Exemption","History Other Exemption",
            "History Taxable Value"]
        df = pd.DataFrame(columns=column_names)
        # Save the DataFrame as a CSV file
        df.to_csv(file_path, index=False)
    
    file_path = 'data.csv'

    # Extract the column values as a list
    merged_dict = {}
    merged_dict.update(profile_data)
    merged_dict.update(values_data)
    merged_dict.update(sales_data)
    merged_dict.update(residential_data)
    merged_dict.update(commercial_data)
    merged_dict.update(history_data)
    print(merged_dict)
    df = pd.read_csv(file_path)
    # Create a DataFrame with column names
    df = pd.DataFrame(columns=merged_dict.keys())

    # Append the dictionary as a single row
    df = df.append(merged_dict, ignore_index=True)
    df.to_csv('data.csv', mode='a', index=False, header =  False)

def get_information():
    
    result_rows = get_rows()
    for i in range(2,len(result_rows)):
        print(i - 1)
        row = result_rows[i]
        row.click()
        time.sleep(2)
        profile_data = get_profile_details()
        a_tags = side_menu_tags()
        for a in range(len(a_tags)):
            print()
            if(a_tags[a].text == "VALUES"):
                a_tags[a].click()
                time.sleep(2)
                values_data = get_values_details()
                a_tags = side_menu_tags()
            if(a_tags[a].text == "SALES"):
                a_tags[a].click()
                time.sleep(2)
                sales_data = get_sales_details()
                a_tags = side_menu_tags()
            if(a_tags[a].text == "RESIDENTIAL"):
                a_tags[a].click()
                time.sleep(2)
                residential_data = get_residential_details()
                a_tags = side_menu_tags()
            if(a_tags[a].text == "COMMERCIAL"):
                a_tags[a].click()
                time.sleep(2)
                commercial_data = get_commercial_details()
                a_tags = side_menu_tags()
            if(a_tags[a].text == "ASSESSMENT HISTORY"):
                a_tags[a].click()
                time.sleep(2)
                history_data = get_assesment_history_details()
                a_tags = side_menu_tags()
        
        
        save_data(profile_data,values_data,sales_data,residential_data,commercial_data,history_data)
        driver.execute_script("window.history.go(-6)")
        time.sleep(2)
        result_rows = get_rows()

next_page_found = True
while (next_page_found == True):
  #a = input("press any key to continue: ")
  get_information()
  table_tags = driver.find_elements(By.TAG_NAME, "table")
  a_tags = table_tags[9].find_elements(By.TAG_NAME, "a")
  i = 0
  for a in a_tags:
      if("Next >>" in a.text):
          a.click()
          time.sleep(2)
      else:
        i = i + 1
  if(i == len(a_tags)):
     print("All Pages Done")
     next_page_found = False

driver.quit()





