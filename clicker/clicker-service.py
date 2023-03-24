# Service to support vulnerable by design web applications.
# Flask server receives POST requests and "clicks" malicious
# links with headless chrome browser
# Probably shouldn't expose this app to public networks

# Form data for POST requests:
# url: required. URL encoded url to be visited
# cookie_name: optional. Cookie name to be set for visiting (simulate user)
# cookie_value: optional. Value for cookie_name. 

# Both cookie_name and cookie_value must be received to set the cookie.
# Otherwise the malicious link will be visited without a cookie set.

# import flask relevant libraries
from urllib.parse import unquote_plus
from flask import Flask
from flask import request

# import selenium relevant libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# initialize flask app
app = Flask(__name__)

# initialize headless chrome browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

# Route set to "/clicker" to avoid scanners randomly tripping service
@app.route('/clicker', strict_slashes=False, methods = ['POST'])
def clicker():
    """Receive URL to click, and make request"""
    # only accept POST
    if request.method == 'POST':
        data = request.form
        # url var is minimum required to "click" malicious link
        if "url" in data.keys():
            # url decode incoming url
            target_url = unquote_plus(data['url'])
            # if cookie values are provided, set cookie for malicious "click"
            if "cookie_name" in data.keys() and "cookie_value" in data.keys():
                
                driver.set_page_load_timeout(1)
                
                # selenium can't set a cookie without being "at" the domain
                # so we hit a known 404 address, then add the cookie to the session
                driver.get(f"{target_url}/thisaddressshouldntexist")
                driver.add_cookie({'name': unquote_plus(data['cookie_name']), 'value': unquote_plus(data['cookie_value'])})
            try:
                # "Click" malicious link
                driver.set_page_load_timeout(1)
                driver.get(target_url)
            except TimeoutException as ex:
                isrunning = 0
                return f"Exception has been thrown. {str(ex)}"

            return "Done"
        else:
            return "This endpoint requires a url parameter."

    else:
        return "STATUS 405 - Method Not Allowed"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
