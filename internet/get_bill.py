import os
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
print(os.environ)

# Configure logging
logging.basicConfig(filename='/var/log/quebec-bills.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Configure browser to enable file downloading and headless Chrome option.
# This is very important for running on cloud
logging.info("Setting up browser")
download_dir = "/home/ec2-user"
options = webdriver.ChromeOptions()
profile = {"download.default_directory": download_dir,
           "plugins.always_open_pdf_externally": True}
options.add_experimental_option("prefs", profile)
options.add_argument('headless')
driver = webdriver.Chrome(options=options)
logging.info("Browser setup done")

# Getting credentials from environment
email = os.getenv('VIVO_EMAIL')
password = os.getenv('VIVO_PASSWORD')

# Check if environment variables are set
if email is None or password is None:
    logging.warning("Environment variables for email or password are not set")
    exit()

# Access main website
driver.get("https://www.vivo.com.br/portalweb/appmanager/env/web")

# Insert email field
logging.info("Logging in to Vivo portal")
login = driver.find_element_by_name('cpfOuEmail')
login.send_keys(email)

# Insert password field (using js hack)
js = "document.getElementById('senhaHeader').value = '"+password+"'"
driver.execute_script(js)

# Submit login
submit_button = driver.find_element_by_id('btnEntrar')
submit_button.click()

# Wait until dashboard page has loaded
WebDriverWait(driver, 60).until(EC.url_contains("meuvivo.vivo.com.br"))
logging.info("Login successful")

# Move to page that has link to the pdf
driver.get("https://legado.vivo.com.br/portal/site/meuvivo/segundaViaConta?segundaViaConta=sVConta")

# Wait to page load
try:
    btn = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, 'botao-segunda-via')))
    btn.click()
except TimeoutException:
    # Latest bill is already paid or page timed out
    logging.info("Latest bill was already paid")
    pass
else:
    logging.info("Latest bill is ready to be paid")
