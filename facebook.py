import sys, getopt, time, os
import getpass
import pickle
from selenium import webdriver

def login(driver):
    email = input("Email:")
    password = getpass.getpass("Password:")
    print("Login...")
    times = 0
    while(1):
    	try:
    		login_box = driver.find_element_by_xpath('//*[@id="email"]')
    		login_box.send_keys(email)
    		login_box = driver.find_element_by_xpath('//*[@id="pass"]')
    		login_box.send_keys(password)
    		chbox = driver.find_element_by_xpath('//*[@id="persist_box"]')
    		chbox.click()
    		login_box.submit()
    		break
    	except():
    		time.sleep(0.5)
    		times += 1
    		if(times > 100):
    			print("Time Out")
    			exit()
    try:
        driver.find_element_by_tag_name('textarea')
        pickle.dump(driver.get_cookies(), open("{}/cookies.pkl".format(os.path.split(os.path.realpath(__file__))[0]),"wb"))
    except:
        print("LogIn Failed")
        driver.quit()
        exit()

def post(driver, content):
    print("Posting...")
    times = 0
    while(1):
    	try:
    		msgbox = driver.find_element_by_tag_name('textarea')
    		time.sleep(0.5)
    		msgbox.send_keys(content)
    		msgbox.submit()
    		break
    	except():
    		time.sleep(0.5)
    		times += 1
    		if(times > 100):
    			print("Time Out")
    			exit()

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h",[])
        # opts, args = getopt.getopt(argv,"hp:",["picture="])
    except getopt.GetoptError:
        print('facebook.py <content>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('facebook.py <content>')
            sys.exit()
        # elif opt in ("-p", "--picture"):
        #     picture = arg

    service_args = ['--cookies-file=./cookies.txt']
    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS(executable_path=os.path.split(os.path.realpath(__file__))[0]+'/phantomjs', service_args=service_args)
    try:
        cookies = pickle.load(open("{}/cookies.pkl".format(os.path.split(os.path.realpath(__file__))[0]), "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://www.facebook.com/');
    except:
        driver.get('https://www.facebook.com/');
        login(driver)

    try:
        driver.find_element_by_tag_name('textarea')

    except:
        login(driver)

    try:
        content= "\n".join(args)
    except:
        content = ''

    post(driver, content)
    print(content)
    driver.close()

if __name__ == "__main__":
   main(sys.argv[1:])
