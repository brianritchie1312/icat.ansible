# Notes
 # Selenium Must be installed via pip
 # webdriver executables must be in system PATH
 # Python must be withn system PATH

# Steps
 # Open FireFox
 # Go to icat_url
 # Log in to Simple/root if it simple is installed
 # Checks login navigated to correct page
 # Checks Data exists
 # Checks cart doesn't exist (clears if it does)
 # If root user
  # Clicks on first row
  # Clicks on add-to-cart button
  # Checks Cart Appeared
  # Clicks on second row (Dataset 2)
  # Click first add-to-cart BUTTON
  # Checks the cart now has 2 items
  # Clears the cart
  # Checks the cart no longer exists
  # Clicks download button
  # TODO Check download was succesful
  # Clicks add-to-cart button
  # Opens cart
  # clicks download-all button
  # TODO Check download was succesful
  # Closes CART
  # TODO Add more steps
 # Logs out
 # Repeat non root user steps for db/root if it exists
 # TODO add support for LDAP and Anon
 # Close Firefox
 # Repeat all steps for Chrome
 # Output each check to Console
 # Travis will read this output and return pass or fail depending

#---IMPORTS---

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import time

#---
#---VARIABLES---
 # These should be modified by ansible in case someone modifies config.yml without modifing this

icat_url = "{{ icat_url }}"

authn_simple = {{ authn_simple }}         # Simple Authentication
simple_root = "{{ icat_root }}"
simple_pass = "{{ icat_pass }}"

authn_db = {{ authn_db }}             # DB Authentication
db_root = "root"
db_pass = "password"

authn_root = "{{ icat_mech | title }}"       # Main Plugin used for test data ingest

download_dir = "{{ download_dir }}Tests"

#---

#---Aliases---

#-Login as specific user
def login(plugin_name, plugin_root, plugin_pass):
    logout();
    wait_until((By.ID, "plugin"))
    Select(browser.find_element(By.ID, 'plugin')).select_by_visible_text(plugin_name)
    browser.find_element(By.ID, 'username').send_keys(plugin_root)
    browser.find_element(By.ID, 'password').send_keys(plugin_pass)
    browser.find_element(By.ID, 'login').click()
#-end of login()-

def logout():
        browser.get(icat_url + "/#/")   # Return to Home, Topcat saves browse path across multiple users, this should reset it
        time.sleep(1)
        browser.get(icat_url + "/#/logout")
#-END OF logout()

# Wait until element exists
def wait_until(element):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(element))

# Check if Cart icon exists
def cart_exists():
    try:
        browser.find_element(By.CSS_SELECTOR, '.glyphicon.glyphicon-shopping-cart')
        return True
    except NoSuchElementException:
        return False

# Empty Cart
def cart_clear():
    try:
        browser.find_element(By.CSS_SELECTOR, '.glyphicon.glyphicon-shopping-cart').click()

        wait_until((By.CSS_SELECTOR, 'button[translate="CART.REMOVE_ALL_BUTTON.TEXT"]'))
        time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'button[translate="CART.REMOVE_ALL_BUTTON.TEXT"]').click()
        time.sleep(1)
    except NoSuchElementException as ex:
        print("Cart already non-existent")
        print ex

# Downloads exists
def downloads_exists():
    try:
        browser.find_element(By.CSS_SELECTOR, '.glyphicon.glyphicon-download-alt')
        return True
    except NoSuchElementException:
        return False

# Remove download button Exists
def downloads_rm_exists():
    try:
        browser.find_element(By.CSS_SELECTOR, 'a[translate="DOWNLOAD.ACTIONS.LINK.REMOVE.TEXT"]')
        return True
    except NoSuchElementException:
        return False

# Clear downloads
def downloads_clear():
    try:
        browser.find_element(By.CSS_SELECTOR, '.glyphicon.glyphicon-download-alt').click()
        time.sleep(3)

        while (downloads_rm_exists() == True):
            browser.find_element(By.CSS_SELECTOR, 'a[translate="DOWNLOAD.ACTIONS.LINK.REMOVE.TEXT"]').click()
            time.sleep(1)

    except NoSuchElementException as ex:
        print("Downloads already non-existent")
        print ex



#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------


def topcat_test(browser_name):
    browser.get(icat_url)

#-TODO- move these into a single repeatable function

    if (authn_simple == True):  # Simple Login Test
        print ('\033[3m' + browser_name + ": simple/" + simple_root + '\033[0m')
        test_login("Simple", simple_root, simple_pass)
        test_users(authn_root, "Simple")

    print("") # New Line for easier Console Reading

    if (authn_db == True):  # Simple Login Test
        print ('\033[3m' + browser_name + ": db/" + db_root + '\033[0m')
        test_login("DB", db_root, db_pass)
        test_users(authn_root, "DB")

    time.sleep(3)
    print("Closing " + browser_name)
    browser.quit()
#-end of topcat_test()-

def test_users(authn_root, plugin_name):
    # Non-root User Tests
    if (authn_root != plugin_name):
        test_data(False)
        test_emptycart()
        test_emptydownloads()
        logout()
        print ("Logging Out")
    # Root User Tests
    if (authn_root == plugin_name):
        test_data(True)
        test_emptycart()
        test_emptydownloads()
        test_cart()
        test_download()
        logout()
        print ("Logging Out")
#-END OF test_users()

#-Check that user can login as specific user without error
def test_login(plugin_name, plugin_root, plugin_pass):
    login(plugin_name, plugin_root, plugin_pass)

    time.sleep(2)
    if (browser.current_url == icat_url + "/#/my-data/LILS"):
        print("Login Test: Success")
    else:
        print("Login Test: Failed (On page '" + browser.current_url + "')")
#-end of test_login()-

#-Check if Data exists within the datbase
def test_data(root):
    data = browser.find_element(By.CLASS_NAME, 'empty-message').text
    if (data == ""):    # Data Does Exist
        if (root == True):
            print ("Data Existence Test: Success: Data elements exist")
        if (root == False):
            print ("Data Absence Test: Failed: Data elements exist")
    if (data != ""):    # Data Does not Exist
        if (root == True):
            print ("Data Existence Test: Failed: " + data)
        if (root == False):
            print ("Data Absence Test: Success: " + data)
#-end of test_data()-

#-Check that cart does not exist when first logging in
def test_emptycart():
    if (cart_exists() == True):
        print("Initial Cart Empty: Failed (" + browser.find_element(By.CSS_SELECTOR, 'span[ng-click="indexController.showCart()"]').text + ")")

        while (cart_exists() == True):
            cart_clear()
            time.sleep(1)

        if (cart_exists == False):
            print("Cart Now Empty")
        else:
            print("Cart Still Exists")
    else:
        print("Inital Cart Empty: Success")
#-END OF test_emptycart()-

#-Check that downloads does not exist when first logging in
def test_emptydownloads():
    if (downloads_exists() == True):
        print("Initial Downloads Empty: Failed")
        downloads_clear()
        time.sleep(1)
        if (downloads_exists() == False):
            print("Downloads Now Empty")
        else:
            print("Downloads still exist")
    else:
        print("Initial Downloads Empty: Success")

#-Test data links-
def test_cart():
    wait_until((By.CSS_SELECTOR, 'a[ng-click="grid.appScope.browse(row.entity)"]'))

# Add 1 Dataset to Cart
    try:
        # Click first data entry link
        browser.find_element(By.CSS_SELECTOR, 'a[ng-click="grid.appScope.browse(row.entity)"]').click()

        # Click First Add-to-cart button
        wait_until((By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]'))
        browser.find_element(By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]').click()

        time.sleep(1)
        if (cart_exists() == True):
            #TODO ADD CHECK FOR DATASET INSIDE CART
            #TODO ADD CHECK FOR NO UNSLECTED BUTTONS INSIDE DATASET
            print("Add Dataset to Cart: Success (" + browser.find_element(By.CSS_SELECTOR, 'span[ng-click="indexController.showCart()"]').text + ")")
        else:
            print("Add Dataset to Cart: Failed (Cart does not exist)")

    except NoSuchElementException as ex:
        print("Add Dataset to Cart: Failed")
        print ex

# Add 1 File to Cart
    try:
        # Click Second data entry link
        browser.find_element(By.XPATH, '(//a[@ng-click="grid.appScope.browse(row.entity)"])[2]').click()

        # Click First Add-to-cart button
        wait_until((By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]'))
        browser.find_element(By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]').click()

        time.sleep(1)
        if (browser.find_element(By.CSS_SELECTOR, 'span[ng-click="indexController.showCart()"]').text == "2 items"):
            print("Add File to Cart: Success (" + browser.find_element(By.CSS_SELECTOR, 'span[ng-click="indexController.showCart()"]').text + ")" )
        else:
            print("Add File to Cart: Failed (" + browser.find_element(By.CSS_SELECTOR, 'span[ng-click="indexController.showCart()"]').text + ")" )

    except NoSuchElementException as ex:
        print("Add File to Cart: Failed")
        print ex

# Clear Cart before Next Login
    cart_clear()
    if (cart_exists == True):
        print("Clear Cart: Failed (Cart still exists)")
    else:
        print("Clear Cart: Success")

#-END OF test_cart()-

# Check Download BUTTONS
def test_download():
    # Click Download button
    try:
        wait_until((By.CSS_SELECTOR, 'a[translate="DOWNLOAD_ENTITY_ACTION_BUTTON.TEXT"]'))
        browser.find_element(By.CSS_SELECTOR, 'a[translate="DOWNLOAD_ENTITY_ACTION_BUTTON.TEXT"]').click()

        #-TODO-ADD CHECK FOR Download
        print("Download By Action: Success (file existence not checked)")

    except NoSuchElementException as ex:
        print("Download By Action: Failed")
        print ex

    # Download Cart
    try:
        # Click First Add-to-cart button
        wait_until((By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]'))
        browser.find_element(By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]').click()

        try:
            wait_until((By.CSS_SELECTOR, '.glyphicon.glyphicon-shopping-cart'))
            browser.find_element(By.CSS_SELECTOR, '.glyphicon.glyphicon-shopping-cart').click()

            wait_until((By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD_CART_BUTTON.TEXT"]'))
            time.sleep(1)
            browser.find_element(By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD_CART_BUTTON.TEXT"]').click()
            time.sleep(1)
            wait_until((By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD.MODAL.BUTTON.OK.TEXT"]'))
            time.sleep(1)
            browser.find_element(By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD.MODAL.BUTTON.OK.TEXT"]').click()
            time.sleep(1)

            if (cart_exists() == False):
                    # Check If downloads has appeared
                    if (downloads_exists() == True):
                        print("Download By Cart: Success (file existence not checked)")

                    else:    # Downloads has not appeared
                        print("Download By Cart: Failed (Download icon does not exist)")

            else:
                print("Download By Cart: Failed (Cart still exists)") # Cart has not been removed

        except NoSuchElementException as ex:    # Cart or Download button does not exist
            print("Download By Cart: Failed")
            print ex

    except NoSuchElementException as ex:        # Add-to-cart does not exist
        print("Download By Cart: Failed")
        print ex

    # Clear Cart before Next Login
    downloads_clear()
    if (downloads_exists == True):
        print("Clear Downloads: Failed (Downloads still exists)")
    else:
        print("Clear Downloads: Success")

#---
#---RUNTIME---

# Firefox
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference('browser.download.dir', download_dir + "/Firefox")
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
browser = webdriver.Firefox(profile, executable_path=download_dir+'/geckodriver.exe.')   # Firefox Test
topcat_test("FireFox")
print("")

# Chrome
chrome_options = webdriver.ChromeOptions()
chrome_prefs = {"download.default_directory" : download_dir + "/Chrome"}
chrome_options.add_experimental_option("prefs", chrome_prefs)
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=download_dir+'/chromedriver.exe.')    # Chrome Test
topcat_test("Chrome")

#---

