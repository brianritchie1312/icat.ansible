# Notes
 # Selenium Must be installed via pip
 # webdriver executables must be in system PATH or specified in arguments
 # Geckodriver excutable should be bash script with '/path/to/executable "$@" --marionette-port 2828' INSIDE
 # Python2.7 must be withn system PATH
 # pyvirtualdisplay and xvfb are needed for virtual displays
 # If --user-admin is not included, --user-data will be assumed to be admin

# TODO
    # If possible, no reliance on ansible
      # Install chosen browser
      # Install webdrivers
      # Install selenium, pyvirtualdisplay, etc.
    # Replace time.sleep with reliable wait_until
    # Add tests for everything in checklist

#-------------------------------------------------------------------------------
# Imports
#-------------------------------------------------------------------------------

# Print, this has been imported to allow 'print("string", end="")'
from __future__ import print_function

# Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

# PyVirtualDisplay
from easyprocess import EasyProcess
from pyvirtualdisplay import Display

# OS
import os

# Delay
import time

# Argparse
import argparse

# Regexp
import re

# Firefox
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Chrome
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions


#-------------------------------------------------------------------------------
# Arguments, options
#-------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Gather variables from command line')
required = parser.add_argument_group('required arguments')

# ICAT URL
required.add_argument('--url',
                      action='store',
                      dest='icat_url',
                      help='The url of the icat build you wish to test, including port number.',
                      required=True)

# Priviillged user
required.add_argument('--user-data',
                      action='append',
                      nargs='+',
                      dest='user_data',
                      help='The user with rights to the testdata. syntax: "--user-data <mechanism> <username> <password>" eg. "--user-data simple root pass"',
                      required=True)

# Unprivillaged user
parser.add_argument('--user-nodata',
                    action='append',
                    nargs='+',
                    dest='user_nodata',
                    help='The user without rights to the testdata, used to ensure unprivileged users can not access data. (Syntax: "--user-nodata <mechanism> <username> <password>" eg. "--user-nodata simple user1 pass")',
                    required=False)

# Unprivillaged user
parser.add_argument('--user-admin',
                    action='append',
                    nargs='+',
                    dest='user_admin',
                    help='The admin user, only needed if --user-data is not admin. syntax: "--user-admin <mechanism> <username> <password>" eg. "--user-admin simple root pass"',
                    required=False)

# Create Virtual Display if GUI unavailiable
parser.add_argument('--virtual-display',
                     action='store_true',
                     dest='virtual_display',
                     help='Creates a pyvirtualdisplay, use if GUI is unavailiable',
                     required=False)

# Working directory if in alternative location
parser.add_argument('--path',
                    action='store',
                    dest='download_dir',
                    help='Absolute path to directory containing webdrivers and download folders (default: parent directory of this script)',
                    required=False)

# Browsers to test
parser.add_argument('--browsers',
                    action='append',
                    nargs='+',
                    dest='browsers',
                    help='List of browsers to test. eg. "--browsers firefox chrome" (default: firefox) (supported: firefox, chrome)',
                    required=False)

# Log level
parser.add_argument('--log-level',
                    action='store',
                    dest='log_level',
                    help='Log level of webdrivers (default: unchanged). Currently only firefox supported. eg. --log-level trace',
                    required=False)

# Gather all arguments

# Example arguments, meant for testing within IDE (eg. Atom Runner)
#args = parser.parse_args(['--url', 'http://vm8.nubes.stfc.ac.uk:8080',
#                          '--user-data', 'simple', 'root', 'pass',
#                          '--user-nodata', 'db', 'root', 'password',
#                          # '--user-admin', 'simple', 'root', 'pass',
#                          '--browsers', 'firefox', 'chrome',
#                          '--log-level', 'trace',
#                          # '--path', 'C:\Users\Uvn88637\Documents\AutoICAT2',
#                          # '--virtual-display',
#                          ])

# args = parser.parse_args(['--help'])

args = parser.parse_args()

#-------------------------------------------------------------------------------
# Variables
#-------------------------------------------------------------------------------

class txt:
    BASIC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    HEADING = YELLOW
    SUBHEADING = BOLD
    Success = GREEN + 'Success' + BASIC
    Failed = RED + 'Failed' + BASIC

# Facilty
# TODO make these args
facilty_short_name = "LILS"
facilty_long_name = "Lorum Ipsum Light Source"

# --url
icat_url = args.icat_url
icat_home = icat_url + "/#/my-data/" + facilty_short_name

# --user-data
user_data_mech = args.user_data[0][0]
user_data_name = args.user_data[0][1]
user_data_pass = args.user_data[0][2]

# --user-nodata
if (args.user_nodata != None):
    user_nodata_mech = args.user_nodata[0][0]
    user_nodata_name = args.user_nodata[0][1]
    user_nodata_pass = args.user_nodata[0][2]

# --user-admin
if (args.user_admin != None):
    user_admin_mech = args.user_admin[0][0]
    user_admin_name = args.user_admin[0][1]
    user_admin_pass = args.user_admin[0][2]
    data_is_admin = False
else:
    data_is_admin = True

# --path
if (args.download_dir != None):
    download_dir = (args.download_dir + "/")
else:
    download_dir = (os.path.dirname(os.path.abspath(__file__)) + "/")

# --browsers
if (args.browsers != None):
    # Firefox
    if ('firefox' in args.browsers[0]) or ('Firefox' in args.browsers[0]):      # if --browser is used and firefox is in list
        firefox = True
    else:                   # if --browser is used and firefox is not in list
        firefox = False
    # Chrome
    if ('chrome' in args.browsers[0]) or ('Chrome' in args.browsers[0]):
        chrome = True
    else:
        chrome = False
else:                       # if --browser is not used
    firefox = True
    chrome = False

exc_firefox = 'gecko.sh'
exc_chrome = 'chromedriver'

# --log-level
if (args.log_level != None):
    log_level = args.log_level
else:
    log_level = 'default'

# CSS_SELECTOR of Frequently Used Elements
obj_cart_icon = '.glyphicon.glyphicon-shopping-cart'
obj_downloads_icon = '.glyphicon.glyphicon-download-alt'
obj_row_link = 'a[ng-click="grid.appScope.browse(row.entity)"]'


#-------------------------------------------------------------------------------
# Alliases/Shortcuts
#-------------------------------------------------------------------------------

# Login as specific user
  # mechanism = String, mnemonic of desired plugin
  # username = String, username of user
  # password = String, password of user
def login(mechanism, username, password):
    logout()

    # Fix case of plugins for drop down on login page
    if (mechanism == "simple"):
        mechanism = (mechanism[:1].upper() + mechanism[1:])
    else:
        mechanism = mechanism.upper()

    element_wait((By.ID, "plugin"))
    Select(browser.find_element(By.ID, 'plugin')).select_by_visible_text(mechanism)
    browser.find_element(By.ID, 'username').send_keys(username)
    browser.find_element(By.ID, 'password').send_keys(password)
    browser.find_element(By.ID, 'login').click()
#-END-

# Logout
def logout():
        browser.get(icat_url + "/#/")   # Return to Home, Topcat saves browse path across multiple users, this should reset it
        time.sleep(1)
        browser.get(icat_url + "/#/logout")
#-END-

# Find element by CSS_SELECTOR
  # element = String, CSS_SELECTOR of element
    # non CSS_SELECTOR need full command
def element_find(element):
    return browser.find_element(By.CSS_SELECTOR, (element))
#-END-

# Click element by CSS_SELECTOR
  # element = String, CSS_SELECTOR of element you wish to click on
    # non CSS_SELECTOR need full command
def element_click(element):
    element_find(element).click()
#-END-

# Wait until element exists
  # element = Two arguments, selector and string for selector
    # eg. element_wait((By.ID, 'plugin')) would wait until it found element with 'plugin' as it's id
    # eg. element_wait((By.CSS_SELECTOR, '.glyphicon.glyphicon-shopping-cart')) will wait until cart icon shows
def element_wait(element):
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(element))
#-END-

# Check if element exists, element found by CSS_SELECTOR
  # element = CSS_SELECTOR of element
    # non CSS_SELECTOR need full command
def element_exists(element):
    try:
        element_find(element)
        return True
    except NoSuchElementException:
        return False
#-END-

# Get no. of items in cart
def cart_items():
    return int(re.findall(r'\d+', element_find('span[ng-click="indexController.showCart()"]').text)[0])
#-END-

# Add first element to cart and check it has been added
def cart_add():
    # Get number of items in cart
    if (element_exists(obj_cart_icon)):
        pre_items = cart_items()
    else:
        pre_items = 0

    element_wait((By.CSS_SELECTOR, 'div[ng-click="selectButtonClick(row, $event)"]'))
    element_click('div[ng-click="selectButtonClick(row, $event)"]')

    # Compare no. of items in cart to previous
    try:
        element_wait((By.CSS_SELECTOR, obj_cart_icon))
        time.sleep(1)
        post_items = cart_items()
        if (post_items == (pre_items + 1)):
            return post_items           # If 1 item has been added to cart)
        else:
            return pre_items            # If 1 item has not been added to cart
    except NoSuchElementException as ex:
        print(ex)
#-END-

# Delete first entry in cart
  # Will fail if cart is empty
def cart_rm():
    try:
        pre_items = cart_items()

        if (element_exists('div[class="modal-dialog modal-lg"]') == False):
            element_click(obj_cart_icon)

        element_wait((By.CSS_SELECTOR, 'a[translate="CART.ACTIONS.LINK.REMOVE.TEXT"]'))
        element_click('a[translate="CART.ACTIONS.LINK.REMOVE.TEXT"]')

        time.sleep(1)
        post_items = cart_items()

        if (post_items == pre_items - 1):
            return post_items
        else:
            return pre_items

    except NoSuchElementException as ex:
        print(ex)
#-END-

# Empty Cart
def cart_clear():
    try:
        if (element_exists('div[class="modal-dialog modal-lg"]') == False):
            element_click(obj_cart_icon)

        element_wait((By.CSS_SELECTOR, 'button[translate="CART.REMOVE_ALL_BUTTON.TEXT"]'))
        time.sleep(1)
        element_click('button[translate="CART.REMOVE_ALL_BUTTON.TEXT"]')
        time.sleep(1)
    except NoSuchElementException as ex:
        print("Cart already non-existent")
        print(ex)
#-END-

# Clear downloads
def downloads_clear():
    try:
        # If downloads not already open click downloads icon
        if (element_exists('div[class="modal-content ng-scope"]') == False):
            element_click(obj_downloads_icon)
        time.sleep(1)

        while (element_exists('a[translate="DOWNLOAD.ACTIONS.LINK.REMOVE.TEXT"]') == True):
            element_click('a[translate="DOWNLOAD.ACTIONS.LINK.REMOVE.TEXT"]')
            time.sleep(1)

    except NoSuchElementException as ex:
        print("Downloads already non-existent")
        print(ex)
#-END-

# Click a link and check if directed to correct url
  # element = String, CSS_SELECTOR of element to click
  # target = String, Url the element should take user to (appended after baseurl, eg. '/#/my-data' not 'http://localhost:8080/#/my-data')
def link_check(element, target):
    try:
        element_wait((By.CSS_SELECTOR, element))
        element_click(element)
        time.sleep(1)

        if (browser.current_url == icat_url + target):
            return (txt.Success)
        else:
            return (txt.Failed + " (current url: " + browser.current_url + ")")

    except NoSuchElementException as ex:
        return (txt.Failed + " (link element does not exist)")
        print(ex)
#-END-

# Search for string and check each tab
  # search = String to search for
  # visit = Bool, should the item have results in Visit
  # dataset = Bool, should the item have results in Dataset
  # datafile = Bool, should the item have results in Datafile
def search_test(search, visit, dataset, datafile):

    element_wait((By.ID, "searchText"))
    browser.find_element(By.ID, 'searchText').send_keys(Keys.CONTROL + "a")
    browser.find_element(By.ID, 'searchText').send_keys(search)
    element_click('button[type="submit"]')
    time.sleep(2)

    search_results(search, "Visit", visit)
    time.sleep(1)
    search_results(search, "Dataset", dataset)
    time.sleep(1)
    search_results(search, "Datafile", datafile)
    time.sleep(1)
#-END-

# Check results of search and output results
  # search = String, sting to be searched
  # tab = String, which tabs are you looking in (eg. Visit, Dataset, Datafile)
  # target = Bool,should there be results in the respective tab?
def search_results(search, tab, target):
    print("Search Results for '" + search + "' in " + tab + ": ", end='')

    # element clicked below is not named visit but is named investigation, despite visible text saying visit, so quick name change is declared here
    if (tab == "Visit"):
        tab = "investigation"

    element_click('a[ng-click="searchResultsController.currentTab = \'' + tab.lower() + '\'"]')
    time.sleep(1)

    if (target == True): # If results should exist
        if (element_exists('div[class="ui-grid-cell-contents ng-scope"]') == True): # IF results DO exist
            print(txt.Success + " (Results Exist)")
        else:
            print(txt.Failed + " (Results Do Not Exist)")

    else:        # If results shouldn't exist
        if (element_exists('div[class="ui-grid-cell-contents ng-scope"]') == False):
            print(txt.Success + " (No Results)")
        else:
            print(txt.Failed + " (Results Exist)")
#-END-

# Click on first item and check if naviagate to correct location
  # level = String, current level of browsing (eg. proposal, investigation, dataset, datafile)
  # target = String, level to navigate to
  # element = String, CSS_SELECTOR of element to click
def browse_click(level, target, element):
    print("Browse " + level + " to " + target + ": ", end='')

    element_wait((By.CSS_SELECTOR, obj_row_link))
    element_click(obj_row_link)
    time.sleep(1)

    if (element_exists('i[translate="ENTITIES.' + target.upper() + '.NAME"]') == True):
        print(txt.Success)
    else:
        print(txt.Failed + " (on page:" + browser.current_url + ")")
#-END-

# Click non-active section of row and check if info tab appears
  # level = String, current level (eg. Visit, Dataset, Datafile)
  # url = String, url to naviagte to before checking for infotab
def datanav_infotab(level, url):
    print("Info Tab " + level + " Level: ", end='')
    browser.get(url)
    time.sleep(1)

    # Click empty space on row, not link text
        # WARNING this does not guarantee child element (hyperlink) will not be clicked, especially on smaller resolutions
    element_click('div[class="ui-grid-cell-contents ng-binding ng-scope"]')
    time.sleep(1)

    if (element_exists('div[class="ui-grid-row ng-scope"]') == True):
        print(txt.Success)
    else:
        print(txt.Failed + " (Info Tab Not Present)")
#-END-


#-------------------------------------------------------------------------------
# Tests
#-------------------------------------------------------------------------------

# Test Modules
  # These modules are mainly for organisation and do not affect the code itself, except in naming conventions
    #--Browser--
        # Open browser and navigate to url
    #--Login--
        # Attempt to login as specific user
    #--Navigation--
        # Check Interface elements exist and work (eg. browse, search etc.)
    #--Data--
        # Check Data Exists and environment is as expected (eg. url, details popup works)
    #--Data Navigation--
        # Check all data links redirect correctly (eg. clicking visit directs to correct path)
    #--Cart--
        # Check adding to, removing from and clearing cart works as expected
    #--Download--
        # Download via action, https cart and globus. Check everything works as expected (eg. zip rename, download method)
    #--Other--
        # Other tests that may need to be added, check silvia's checklist
    #--Master--
        # The function that calls all the others

#---Browser---------------------------------------------------------------------

#-Navigate to Topcat home page and check if redirected to login
def test_url():
    print("Load Login Page: ", end='')
    try:
        browser.get(icat_url)
        time.sleep(2)
        if (browser.current_url == icat_url + '/#/login'):
            print(txt.Success + " (" + browser.current_url + ")")
        else:
            print(txt.Failed + " (" + browser.current_url + ")")
    except NoSuchElementException as ex:
        print(txt.Failed)
        print(ex)
#-END-

#---Login-----------------------------------------------------------------------

#-Check that user can login as specific user without error
  # mechanism = String, mnemonic of plugin (lowercase)
  # username = String, username
  # password = String, password
def test_login(mechanism, username, password):
    print("Login Test: ", end='')
    login(mechanism, username, password)

    time.sleep(2)
    if (browser.current_url == icat_home):
        print(txt.Success)
    else:
        print(txt.Failed + " (On page '" + browser.current_url + "')")
#-END-

#---Navigation------------------------------------------------------------------

# Check Nav buttons in top toolbar
def test_nav_toolbar():
    browser.get(icat_home)
    time.sleep(1)

    print("Toolbar About Page Link Test: ", end='')
    print(link_check('a[ui-sref="about"]', '/#/about'))

    print("Toolbar Contact Page Link Test: ", end='')
    print(link_check('a[ui-sref="contact"]', '/#/contact'))

    print("Toolbar Help Page Link Test: ", end='')
    print(link_check('a[ui-sref="help"]', '/#/help'))

    print("Toolbar Home Page Link Test: ", end='')
    print(link_check('a[ui-sref="homeRoute"]', '/#/my-data/' + facilty_short_name))
#-END-

# Check if admin link is present for admin user and is hidden for non-admin user(s)
  # admin = Boolean, is current user admin?
def test_nav_toolbar_admin(admin):
    browser.get(icat_home)
    time.sleep(1)

    if (admin == True):
        print("Toolbar Admin Page Link: ", end='')
        print(link_check('a[ui-sref="admin.downloads"]', '/#/admin/downloads/' + facilty_short_name))
    else:
        print("Toolbar Admin Page Link Hidden: ", end='')
        if (element_find('li[ng-show="indexController.adminFacilities.length > 0"]').get_attribute("class") == "ng-hide"):
            print(txt.Success)
        else:
            print(txt.Failed)
#-END-

# Check footer elements exist
def test_nav_footer():
    print("Footer Existence: ", end='')
    if (element_exists('footer[class="footer"]') == True):
        print(txt.Success)
    else:
        print(txt.Failed)

    # TODO see if it can specified that these must be children of footer element

    print("Footer Facility Link Existence: ", end='')
    try:
        browser.find_element(By.LINK_TEXT, facilty_long_name)
        print(txt.Success)
    except NoSuchElementException:
        print(txt.Failed + " (trying to find: " + facilty_long_name + ")")

    print("Footer Privacy Policy Link Existence: ", end='')
    try:
        browser.find_element(By.LINK_TEXT, 'Privacy Policy')
        print(txt.Success)
    except NoSuchElementException:
        print(txt.Failed)

    print("Footer Cookie Policy Link Existence: ", end='')
    try:
        browser.find_element(By.LINK_TEXT, 'Cookie Policy')
        print(txt.Success)
    except NoSuchElementException:
        print(txt.Failed)

    print("Footer About Us Link Existence: ", end='')
    try:
        browser.find_element(By.LINK_TEXT, 'About Us')
        print(txt.Success)
    except NoSuchElementException:
        print(txt.Failed)
#-END-

# Find and click 'My Data', 'Browse' and 'Search' tabs
def test_nav_tabs():
    browser.get(icat_home)
    time.sleep(1)

    print("Tabs Browse Link Test: ", end='')
    print(link_check('a[translate="MAIN_NAVIGATION.MAIN_TAB.BROWSE"]', '/#/browse/facility/' + facilty_short_name +'/proposal'))

    print("Tabs Search Link Test: ", end='')
    print(link_check('a[translate="MAIN_NAVIGATION.MAIN_TAB.SEARCH"]', '/#/search/start'))

    print("Tabs My Data Link Test: ", end='')
    print(link_check('a[translate="MAIN_NAVIGATION.MAIN_TAB.MY_DATA"]', '/#/my-data/' + facilty_short_name))
#-END-

def test_nav_search():
    browser.get(icat_url + "/#/search/start")
    search_visit = "Proposal"
    search_dataset = "Dataset"
    search_datafile = "Datafile"

    # Search that should only have results in Visit
    search_test(search_visit, True, False, False)

    # Search that should only have results in Dataset
    search_test(search_dataset, False, True, False)

    # Search that should only have results in Datafile
    search_test(search_datafile, False, False, True)
#-END-

#---Data------------------------------------------------------------------------

#-Check if Data exists within the datbase
  # data = Boolean, true if user is supposed to have access to testdata
def test_data_exists(data):
    browser.get(icat_home)
    time.sleep(1)

    if (data == True):
        print("Data Existence Test: ", end='')
        if (element_exists(obj_row_link) == True):
            print(txt.Success)
        else:
            print(txt.Failed)
    else:
        print("Data Absence Test: ", end='')
        if (element_exists(obj_row_link) == True):
            print(txt.Failed)
        else:
            print(txt.Success)
#-END-

#-Check that cart does not exist when first logging in
def test_data_cart():
    print("Initial Cart Empty Test: ", end='')
    if (element_exists(obj_cart_icon) == True):
        print(txt.Failed + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")", end='')

        while (element_exists(obj_cart_icon) == True):
            cart_clear()
            time.sleep(1)

        if (element_exists(obj_cart_icon) == False):
            print(" - Cart Now Empty")
        else:
            print(" - Cart Still Exists")
    else:
        print(txt.Success)
#-END-

#-Check that downloads does not exist when first logging in
def test_data_downloads():
    print("Initial Downloads Empty Test: ", end='')
    if (element_exists(obj_downloads_icon) == True):
        print(txt.Failed, end='')
        downloads_clear()
        time.sleep(1)
        if (element_exists(obj_downloads_icon) == False):
            print(" - Downloads Now Empty")
        else:
            print(" - Downloads still exist")
    else:
        print(txt.Success)
#-END-

#---Data Navigation-------------------------------------------------------------

def test_datanav_browse():
    browser.get(icat_url + '/#/browse/facility/' + facilty_short_name + '/proposal')
    time.sleep(1)

    # Down
    browse_click("Proposal", "Investigation", obj_row_link)
    # global visit_url
    # visit_url = browser.current_url

    browse_click("Investigation", "Dataset", obj_row_link)
    global dataset_url
    dataset_url = browser.current_url

    browse_click("Dataset", "Datafile", obj_row_link)
    global datafile_url
    datafile_url = browser.current_url

    # TODO - Add upwards browsing (eg. click breadcrumb links)

#-END-

# Check if info tab show when clicking non active area of items
def test_datanav_infotab():
    datanav_infotab("Visit", icat_home)

    datanav_infotab("Dataset", dataset_url)

    datanav_infotab("Datafile", datafile_url)
#-END-

#---Cart------------------------------------------------------------------------

# Add Dataset and Datafile to cart then clear-
def test_cart_add():

    browser.get(dataset_url)
    time.sleep(2)

    print("Add Dataset to Cart: ", end='')
    if (cart_add() == 1):
        print (txt.Success + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")" )
    else:
        print (txt.Failed + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")" )

    time.sleep(3)
    # Click 2nd Dataset, Entire Dataset 1 is already in cart
    browser.find_element(By.LINK_TEXT, 'Dataset 2').click()
    time.sleep(1)

    print("Add Datafile to Cart: ", end='')
    if (cart_add() == 2):
        print (txt.Success + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")" )
    else:
        print (txt.Failed + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")" )
#-END-

# Remove 1 item from cart
def test_cart_rm():
    print("Remove Single Item from Cart: ", end='')
    cart_rm()
    time.sleep(1)
    if (cart_items() == 1):
        print(txt.Success + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")")
    else:
        print(txt.Failed + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")")
#-END-

# CLear the cart
def test_cart_clear():
    print("Clear Cart: ", end='')
    cart_clear()
    time.sleep(1)

    if (element_exists(obj_cart_icon) == False):
        print(txt.Success)
    else:
        print(txt.Failed + " (" + element_find('span[ng-click="indexController.showCart()"]').text + ")")
#-END-

#---Download--------------------------------------------------------------------

# Download Datafile via action button
# TODO check if file exists
def test_download_action():
    print("Download By Action: ", end='')
    browser.get(datafile_url)
    time.sleep(1)
    try:
        element_wait((By.CSS_SELECTOR, 'a[translate="DOWNLOAD_ENTITY_ACTION_BUTTON.TEXT"]'))
        element_click('a[translate="DOWNLOAD_ENTITY_ACTION_BUTTON.TEXT"]')

        print(txt.Success + " (NOTE: file existence not checked)")

    except NoSuchElementException as ex:
        print(txt.Failed)
        print(ex)
#-END-

# Download via cart
# TODO check if file exists
# TODO check if download properly added to downloads (eg. download action exists)
def test_download_cart():
    print("Download by Cart: ", end='')
    cart_add()
    time.sleep(1)

    try:
        element_wait((By.CSS_SELECTOR, obj_cart_icon))
        element_click(obj_cart_icon)

        element_wait((By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD_CART_BUTTON.TEXT"]'))
        time.sleep(1)
        element_click('button[translate="CART.DOWNLOAD_CART_BUTTON.TEXT"]')

        element_wait((By.CSS_SELECTOR, 'button[translate="CART.DOWNLOAD.MODAL.BUTTON.OK.TEXT"]'))
        time.sleep(1)
        element_click('button[translate="CART.DOWNLOAD.MODAL.BUTTON.OK.TEXT"]')
        time.sleep(1)

        # Check if cart hidden
        if (element_exists(obj_cart_icon) == False):
            # Check if downloads has appeared
            if (element_exists(obj_downloads_icon) == True):
                print(txt.Success + " (NOTE: File existence not checked)")
            else:    # Downloads has not appeared
                print(txt.Failed + " (Download icon does not exist)")

        else:    # Cart has not been removed
            print(txt.Failed + " (Cart still exists)")

    except NoSuchElementException as ex:
        print(ex)
#-END-

def test_download_avaliable():
    print("Download Is Available in Downloads: ", end='')
    if (element_exists(obj_downloads_icon)):

        # If downloads not already open
        if (element_exists('div[class="modal-content ng-scope"]') == False):
            element_click(obj_downloads_icon)

        time.sleep(1)

        # If Status text Says Availiable
        if (element_find('span[class="ng-binding ng-scope"]').text == "Available"):
            print(txt.Success)
        else:
            print(txt.Failed + "(Download is '" + element_find('span[class="ng-binding ng-scope"]').text + "')")

        # If Download Button exists
        print("Download Button Exists in Downloads: ", end='')
        if (element_exists('a[translate="DOWNLOAD.ACTIONS.LINK.HTTP_DOWNLOAD.TEXT"]') == True) or (element_exists('a[translate="DOWNLOAD.ACTIONS.LINK.GLOBUS_DOWNLOAD.TEXT"]') == True):
            print(txt.Success)
        else:
            print(txt.Failed + " (Download button does not exist)")

    else:
        print(txt.Failed + " (Downloads does not exist)")

# Rename zip file to be downloaded by cart
def test_download_rename():
    print("Downloading Rename Test Not Yet Written")
#-END-

# Remove all items from downloads
def test_download_clear():
    print("Clear Downloads: ", end='')
    downloads_clear()
    if (element_exists(obj_downloads_icon) == True):
        print(txt.Failed + " (Downloads still exists)")
    else:
        print(txt.Success)
#-END-

#---Browsers--------------------------------------------------------------------

# Setup and run tests fo Firefox
def test_firefox():
    print("")
    print(txt.HEADING + "[ Firefox Test ]" + txt.BASIC)

    # Force Firefox to download without prompting user
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference('browser.download.dir', download_dir + "Firefox")
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')

    ff_options = FirefoxOptions()
    if (log_level != 'default'):
        ff_options.log.level = log_level
        ff_options.log.path = download_dir + 'geckodriver.log'

    # Start Tests
    global browser
    browser = webdriver.Firefox(profile, firefox_options=ff_options, executable_path=download_dir+exc_firefox)
    test_browser()
    print("Closing Firefox")
    browser.close()
    print(txt.BOLD + "[ Firefox Test Complete ]" + txt.BASIC)
#-END-

# Setup and run tests for Chrome
def test_chrome():
    print("")
    print(txt.HEADING + "[ Chrome Test ]" + txt.BASIC)

    chrome_options = ChromeOptions()
    # if (log_level != 'default'):
    #     chrome_options.log.level = log_level

    chrome_prefs = {"download.default_directory" : download_dir + "Chrome"}
    chrome_options.add_experimental_option("prefs", chrome_prefs)

    #Start Tests
    global browser
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=download_dir+exc_chrome)
    test_browser()
    print("Closing Chrome")
    browser.close()
    print(txt.BOLD + "[ Chrome Test Complete ]" + txt.BASIC)
#-END-

# TODO - Add support for more browsers (eg. Chromium, Edge, Safari)

#---Other-----------------------------------------------------------------------

# Output useful variables for debuging
def print_variables():
    print("")
    print(txt.HEADING + "[ Gathering Variables ]" + txt.BASIC)

    # Virtual Display
    if (args.virtual_display == True):
        w = 1920
        h = 1080
        display = Display(visible=0, size=(w, h))
        display.start()
        print("Virtual Display Used (" + str(w) + "x" + str(h) + ")")
    else:
        print("Virtual Display Not Used")

    # Browsers
    print("Browsers: ", end="")
    if (firefox == True):
        print("Firefox, ", end="")
    if (chrome == True):
        print("Chrome, ", end="")
    print("")

    # URL
    print("URL: " + icat_url)

    # Facilty
    print("Facility: " + facilty_short_name + "(" + facilty_long_name + ")")

    # Directory
    print("Directory: " + download_dir)

    # Log Level
    print("Log Level: " + log_level)

    # Root User
    print("Data User: " + user_data_mech + "/" + user_data_name)
    print("Data User Password: " + user_data_pass)

    # Non Root User
    print("No Data User: ", end='')
    if (args.user_nodata != None):
        print(user_nodata_mech + "/" + user_nodata_name)
        print("No Data User Password: " + user_nodata_pass)
    else:
        print("NULL")

    print("Admin User: ", end='')
    if (args.user_admin != None):
        print(user_admin_mech + "/" + user_admin_name)
        print("Admin Password: " + user_admin_pass)
    else:
        print("Same as Data User")

    # Newline
        print(txt.BOLD + "[ Gathering Variables Complete ]" + txt.BASIC)
    #---
#-END-

#---Master----------------------------------------------------------------------

# List of tests to run for each user
def test_browser():
    #--Browser--
    test_url()
    print("")

    # User with access to testdata
    print(txt.SUBHEADING + '[ Data User Test ]' + txt.BASIC)
    #---Login--
    test_login(user_data_mech, user_data_name, user_data_pass)
    #--Navigation--
    test_nav_toolbar()
    test_nav_toolbar_admin(data_is_admin)   # data_is_admin = Boolean defined in arguments above
    test_nav_footer()
    test_nav_tabs()
    test_nav_search()
    #--Data--
    test_data_exists(True)
    test_data_cart()
    test_data_downloads()
    #--Data Navigation--
    test_datanav_browse()
    test_datanav_infotab()
    #--Cart--
    test_cart_add()
    test_cart_rm()
    test_cart_clear()
    #--Download--
    test_download_action()
    test_download_cart()
    test_download_avaliable()
    # test_download_rename()
    test_download_clear()
    #--Other--
    #--Finish--
    logout()
    print("Logging Out")

    # User without access to test date (if included in CLI args)
    if (args.user_nodata != None):
        print("")
        print(txt.SUBHEADING + '[ No Data User Test ]' + txt.BASIC)
        test_login(user_nodata_mech, user_nodata_name, user_nodata_pass)
        #---Nav---
        test_nav_toolbar_admin(False)
        #--Data--
        test_data_exists(False)
        test_data_cart()
        test_data_downloads()
        #--Finish--
        logout()
        print ("Logging Out")
        print("")

    # User with admin access (if not same as User with data)
    if (args.user_admin != None):
        print("")
        print(txt.SUBHEADING + '[ Admin User Test ]' + txt.BASIC)
        test_login(user_admin_mech, user_admin_name, user_admin_pass)
        test_nav_toolbar_admin(True)
        logout()
        print ("Logging Out")
        print("")
#-END-

# Master function
def test_master():
    print_variables()

    if (firefox == True):
        test_firefox()

    if (chrome == True):
        test_chrome()

    print("")
    print( txt.GREEN + "Test Complete" + txt.BASIC)
#-END-

#-------------------------------------------------------------------------------
# Runtime
#-------------------------------------------------------------------------------

# Made with (http://patorjk.com/software/taag/#p=display&f=Big&t=TopCat%20Test)
print("  _______           _____      _     _______        _    ")
print(" |__   __|         / ____|    | |   |__   __|      | |   ")
print("    | | ___  _ __ | |     __ _| |_     | | ___  ___| |_  ")
print("    | |/ _ \| '_ \| |    / _` | __|    | |/ _ \/ __| __| ")
print("    | | (_) | |_) | |___| (_| | |_     | |  __/\__ \ |_  ")
print("    |_|\___/| .__/ \_____\__,_|\__|    |_|\___||___/\__| ")
print("            | |                                          ")
print("            |_|                                          ")
print("---------------------------------------------------------")
print("                                                         ")

test_master()

