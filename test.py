from selenium import webdriver 

# Configure browser to test download
download_dir = "/home/ec2-user/"
options = webdriver.ChromeOptions()
preferences = {
        "download.default_directory": download_dir,
        "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", preferences)
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

# Sample PDF download test
driver.get("http://www.africau.edu/images/default/sample.pdf")
