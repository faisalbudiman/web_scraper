from selenium import webdriver


import time
from bs4 import BeautifulSoup
import requests
import pandas as pd



# please put your cetegory  below in cetegory variable
cetegory = "handphone-tablet/handphone"


xx = 1
no = []
name_list = []
description_list = []
image_list = []
store_list = []
rating_list = []
price_list = []

headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        'origin': 'https://www.tokopedia.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'accept': 'application/json, text/plain, */*',
        'referer': 'https://www.tokopedia.com/p/laptop-aksesoris/laptop',
        'authority': 'ace.tokopedia.com'
    }
driver = webdriver.Chrome()

for y in range(1,3):
    listu = []
    main_url  = f'https://www.tokopedia.com/p/{cetegory}?page={y}'
    print(main_url)
    driver.get(main_url)
    time.sleep(2)


    country_list = driver.find_element_by_css_selector('.css-hdtg6a.e15j6tp62').find_element_by_xpath('./..')
    time.sleep(2)
    country_list.click()
    time.sleep(1)
    country_list.find_element_by_css_selector('.css-miy2s2.e15j6tp69').click()
    time.sleep(1)



    driver.execute_script('window.scrollBy(0,4500)','')
    time.sleep(2)


    for x in range(1,76):
        try:
            ave_su_nai = driver.find_element_by_xpath(f'//*[@id="zeus-root"]/div/div[2]/div/div[2]/div/div[2]/div[3]/div[2]/div[3]/div[{x}]/a')
            hh = ave_su_nai.get_attribute('href')                                                
            listu.append(hh)
        except:
            pass

    print("lenn:", len(listu))

    for x in listu:
        if x.find('https://www') == -1:
            
            url = str(x)
            # print(url)
            urld = url.split('r=')[1]
            urld = urld.split('%3F')[0]
            urld = urld.replace('%3A%2F%2F','://')
            urld = urld.replace('%2F','/')
            urld = urld+'?src=topads'
            
            driver.get(urld)
            time.sleep(3)
            driver.refresh()
            driver.implicitly_wait(5)
        
            r = requests.get(urld,headers=headers)
            # print(r.status_code)
            soup  = BeautifulSoup(r.text,'html.parser')
            name = soup.find('h1',class_='css-1wtrxts').text
            price = soup.find('div',{'data-testid':'lblPDPDetailProductPrice'}).text

           
            try:
                reting = driver.find_element_by_xpath('//*[@id="pdp_comp-product_content"]/div/div[1]/div/div[2]/span[1]/span[2]').text
                # print(reting)
            except:
                try:
                    driver.refresh()
                    driver.implicitly_wait(5)
                    reting = driver.find_element_by_xpath('//*[@id="pdp_comp-product_content"]/div/div[1]/div/div[2]/span[1]/span[2]').text
                except:
                    reting = '4'
  
   

            try:
                image = soup.find('img',class_="fade")['src']
              
            except:
                image = 'Not Found'
            # print(image)
        
            try:
                shop_name = soup.find('a',{'data-testid':'llbPDPFooterShopName'}).text
            except:
                try:
                    shop_name = driver.find_element_by_xpath('//*[@id="pdp_comp-shop_credibility"]/div[2]/div[1]/div/a/h2').text                      
                   
                except:
                    shop_name =  'Not Found'
            
            # print(shop_name)

            try:
                description = soup.find('div',class_="css-1k1relq").text
                description = description.strip()
                description = description.replace('\n',',')
                description = description.split("-word;}")[1]
            except:
                description = 'Gudang-HP'
      

        else:
            xxs = x+'?src=topads'
           
            driver.get(xxs)
            driver.implicitly_wait(5)
            driver.refresh()
            driver.implicitly_wait(4)
            r = requests.get(x,headers=headers)
            # print(r.status_code)
            soup  = BeautifulSoup(r.text,'html.parser')
            name = soup.find('h1',class_='css-1wtrxts').text
            price = soup.find('div',{'data-testid':'lblPDPDetailProductPrice'}).text
            try:
                reting = driver.find_element_by_xpath('//*[@id="pdp_comp-product_content"]/div/div[1]/div/div[2]/span[1]/span[2]').text
            except:
                try:
                    driver.refresh()
                    driver.implicitly_wait(5)
                    reting = driver.find_element_by_xpath('//*[@id="pdp_comp-product_content"]/div/div[1]/div/div[2]/span[1]/span[2]').text
                except:
                    try:              
                        reting = soup.find('span',{'data-testid':'lblPDPDetailProductRatingNumber'}).text
                    except:
                        reting = 'Nan'

            try:
                image = soup.find('img',class_="fade")['src']
            
            except:
                image = 'Not Found'
      

            try:
                shop_name = soup.find('a',{'data-testid':'llbPDPFooterShopName'}).text
            except:
                try:
                    shop_name = driver.find_element_by_xpath('//*[@id="pdp_comp-shop_credibility"]/div[2]/div[1]/div/a/h2').text                      
                    # print(shop_name)
                except:
                    shop_name =  'Not given'
            try:

                description = soup.find('div',class_="css-1k1relq").text
                description = description.strip()
                description = description.replace('\n',',')
                description = description.split("-word;}")[1]
            except:
                description = 'Not Found'



        name_list.append(name)
        description_list.append(description)
        image_list.append(image)
        store_list.append(shop_name)
        rating_list.append(reting)
        price_list.append(price)
        no.append(xx)
        xx = xx  + 1
        if(xx==101):
            break
    if(xx==101):
            break

main_dir = {
    'No': no,
    'Title': name_list,
    'Description': description_list,
    'image': image_list,
    'Store': store_list,
    'rating of product': rating_list,
    'Price': price_list,

}

df = pd.DataFrame(main_dir, columns=("No", "Title", "Description", "image", "Store", "rating of product", "Price"))
df.style.format(precision=0,
                formatter={('Decision Tree', 'Tumour'): "{:.2f}",
                           ('Regression', 'Non-Tumour'): lambda x: "$ {:,.1f}".format(x*-1e6)
                          })
df.to_csv('tokopedia.csv', index=False, header=True, encoding='utf-8')


print("script run successfully")


driver.quit()





