# Notes
 # Selenium Must be installed via pip
 # webdriver executables must be in system PATH or specified in arguments
 # Geckodriver excutable should be bash script with '/path/to/executable "$@" --marionette-port 2828' INSIDE
 # Python2.7 must be withn system PATH
 # pyvirtualdisplay and xvfb are needed for virtual displays

# TODO
    # If possible, no reliance on ansible
      # Install chosen browser
      # Install webdrivers
      # Install selenium, pyvirtualdisplay, etc.
    # Replace time.sleep with reliable wait_until

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


# PyVirtualDisplay
from easyprocess import EasyProcess
from pyvirtualdisplay import Display

# OS
import os

# Delay
import time

# Argparse
import argparse

#-------------------------------------------------------------------------------
# Arguments, options
#-------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Gather variables from command line')
required = parser.add_argument_group('required arguments')

# Create Virtual Display if GUI unavailiable
parser.add_argument('--virtual-display',
                     action='store_true',
                     dest='virtual_display',
                     help='Creates a pyvirtualdisplay, use if GUI is unavailiable',
                     required=False)

parser.add_argument('--path',
                    action='store',
                    dest='download_dir',
                    help='Absolute path to directory containing webdrivers and download folders (default: parent directory to this script)',
                    required=False)

parser.add_argument('--browsers',
                    action='store',
                    dest='browsers',
                    help='List of browsers to test. eg. "--browsers firefox chrome" (default: firefox) (supported: firefox, chrome)',
                    required=False)

# parser.add_argument('--log-level',
#                     action='store',
#                     dest='log_level',
#                     help='Log level of webdrivers. (default: debug). eg. --log-level trace',
#                     required=False)

# ICAT URL
required.add_argument('--url',
                      action='store',
                      dest='icat_url',
                      help='The url of the icat build you wish to test, including port number.',
                      required=True)

# Priviillged user
required.add_argument('--root',
                      action='append',
                      nargs='+',
                      dest='root',
                      help='The user with rights to the testdata. syntax: "--root <mechanism> <username> <password>" eg. "--root simple root pass"',
                      required=True)

# Unprivillaged user
parser.add_argument('--non-root',
                    action='append',
                    nargs='+',
                    dest='non_root',
                    help='The user without rights to the testdata, used to ensure unprivileged users can not access data. syntax: "--non-root <mechanism> <username> <password>" eg. "--non-root simple user1 pass"',
                    required=False)

# Gather all arguments

#args = parser.parse_args(['--help'])

args = parser.parse_args()

#-------------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------------

# browsers
if (args.browsers != None):
    print(args.browsers)
    # Firefox
    if ('firefox' in args.browsers) or ('Firefox' in args.browsers):      # if --browser is used and firefox is in list
        firefox = True
    else:                   # if --browser is used and firefox is not in list
        firefox = False

    # Chrome
    if ('chrome' in args.browsers) or ('Chrome' in args.browsers):
        chrome = True
    else:
        chrome = False
else:                       # if --browser is not used
    firefox = True
    chrome = False

exc_firefox = 'gecko.sh'
exc_chrome = 'chromedriver'

# if (args.log_level != None):
#     log_level = args.log_level
# else:
#     log_level = 'debug'

icat_url = args.icat_url

root_mech = args.root[0][0]
root_name = args.root[0][1]
root_pass = args.root[0][2]

if (args.non_root != None):
    non_root_mech = args.non_root[0][0]
    non_root_name = args.non_root[0][1]
    non_root_pass = args.non_root[0][2]

# This should be called from elsewhere
if (args.download_dir == None):
    download_dir = (os.path.dirname(os.path.abspath(__file__)) + "/")

#-------------------------------------------------------------------------------
# Alliases
#-------------------------------------------------------------------------------

#-Login as specific user
def login(mechanism, username, password):
    logout()

    if (mechanism == "simple"):
        mechanism = (mechanism[:1].upper() + mechanism[1:])
    else:
        mechanism = mechanism.upper()

    wait_until((By.ID, "plugin"))
    Select(browser.find_element(By.ID, 'plugin')).select_by_visible_text(mechanism)
    browser.find_element(By.ID, 'username').send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
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
	time.sleep(1)
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

#-Master Test-
def topcat_test(browser_name):
    browser.get(icat_url)

    print('Root User Test:')
    test_login(root_mech, root_name, root_pass)
    test_users(True)

    print("") # New line to make output easier to read

    if (args.non_root != None):
        print('Non Root User Test:')
        test_login(non_root_mech, non_root_name, non_root_pass)
        test_users(False)

    time.sleep(3)
    print("Closing " + browser_name)
    browser.close()
#-end of topcat_test()-

#-List of tests to be run by each user-
def test_users(root):
    # Non-root User Tests
    if (root == False):
        test_data(False)
        test_emptycart()
        test_emptydownloads()
        logout()
        print ("Logging Out")
    # Root User Tests
    else:
        test_data(True)
        test_emptycart()
        test_emptydownloads()
        test_cart()
        test_download()
        logout()
        print ("Logging Out")
#-END OF test_users()

#-Check that user can login as specific user without error
def test_login(mechanism, username, password):

    login(mechanism, username, password)

    time.sleep(2)
    if (browser.current_url == icat_url + "/#/my-data/LILS"):
        print("Login Test: Success")
    else:
        print("Login Test: Failed (On page '" + browser.current_url + "')")
#-end of test_login()-

#-Check if Data exists within the datbase
def test_data(root):
    try:
	time.sleep(1)
        browser.find_element(By.CSS_SELECTOR, 'a[ng-click="grid.appScope.browse(row.entity)"]')
        if (root == True):
            print ("Data Existence Test: Success: Data elements exist")
        else:
            print ("Data Absence Test: Failed: Data elements exist")
    except NoSuchElementException:
        if (root == True):
            print ("Data Existence Test: Failed: Data elements do not exist")
        else:
            print ("Data Absence Test: Success: Data elements do not exist")
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
#-end of test_emptycart()-

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
#-end of test_downloads()-

#-Add Dataset and Datafile to cart then clear-
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
#-end of test_cart()-

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

            else:    # Cart has not been removed
                print("Download By Cart: Failed (Cart still exists)")

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
#-end of test_downloads()

#-------------------------------------------------------------------------------
# Runtime
#-------------------------------------------------------------------------------

# Print Info Output for debug
print("---Gathering Variables---")
# Virtual Display
if (args.virtual_display == True):
    w = 1920
    h = 1080
    display = Display(visible=0, size=(w, h))
    display.start()
    print("Virtual Display Used (" + str(w) + "x" + str(h) + ")")
else:
    print("Virtual Display Not Used")

print("URL: " + icat_url)

print("Directory: " + download_dir)
print("Root User: " + root_mech + "/" + root_name)
print("Root Password: " + root_pass)

if (args.non_root != None):
    print("Non Root User: " + non_root_mech + "/" + non_root_name)
    print("Non Root Password: " + non_root_pass)
else:
    print("Non Root User : NULL")

print("")
#---

# Firefox tests
if (firefox == True):
    print("---Firefox Test---")

    from selenium.webdriver import Firefox

    # Uncomment this and add 'firefox_options=ff' to arguments in webdriver.Firefox()
    # from selenium.webdriver.firefox.options import Options
    #
    # ff = webdriver.FirefoxOptions()
    # ff.log.level = 'trace'

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference('browser.download.dir', download_dir + "Firefox")
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

    # Start Tests
    browser = webdriver.Firefox(profile, executable_path=download_dir+exc_firefox)
    print("")
    topcat_test("Firefox")
    print("")

# Chrome tests
if (chrome == True):
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.log.level = log_level
    chrome_prefs = {"download.default_directory" : download_dir + "Chrome"}
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    #Start Tests
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=download_dir+exc_chrome)    # Chrome Test
    print("---Chrome Test---")
    print("")
    topcat_test("Chrome")
    print("")

print("Test Complete")
#---

