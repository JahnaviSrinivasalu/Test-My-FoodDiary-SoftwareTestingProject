import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class TestFoodDiary(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://127.0.0.1:5000/home') 
        self.wait = WebDriverWait(self.driver, 10)
        print("Browser opened")

        self.driver.maximize_window()

        with open('config.json') as f:
            self.config = json.load(f)

        self.base_url = self.config['base_url']
        self.food_name = self.config['addfood']['food_name']
        self.carbo = self.config['addfood']['carbo']
        self.protein = self.config['addfood']['protein']
        self.fat = self.config['addfood']['fat']

    def test_FoodDiary(self):
        
        #home
        driver = self.driver
        config = self.config
        wait = self.wait
        expected_title = 'Food Diary'
        actual_title = driver.title
        print(f"Expected title: {expected_title}")
        print(f"Actual title: {actual_title}")
        self.assertEqual(actual_title, expected_title, "The page title does not match the expected title.")
        print("Home page is verified.")
        time.sleep(2)

        #listview
        driver.get(f'{self.base_url}/listview')
        time.sleep(4)
        expected_title_listview = 'Food Diary'
        actual_title_listview = driver.title
        self.assertEqual(actual_title_listview, expected_title_listview, "The list view page title does not match the expected title.")
        food_items = driver.find_elements(By.CSS_SELECTOR, 'ol li')
        self.assertGreater(len(food_items), 0, "No food items found in the list.")

        #addfood to listview
        driver.get(f'{self.base_url}/newfood')
        time.sleep(2)
        driver.find_element(By.ID, 'food_name').send_keys(self.food_name)
        driver.find_element(By.ID, 'carbo').send_keys(self.carbo)
        driver.find_element(By.ID, 'protein').send_keys(self.protein)
        driver.find_element(By.ID, 'fat').send_keys(self.fat)
        time.sleep(2)
        driver.find_element(By.NAME, 'button').click()
        time.sleep(2)
        success_message = driver.find_element(By.TAG_NAME, 'p').text
        print(f"Message displayed: {success_message}")
        self.assertIn('Success', success_message, "Food item was not added successfully.")

        #back to listview to check the added food item
        driver.get(f'{self.base_url}/listview')
        time.sleep(4)
        
        # Navigate to Food Tracker page
        driver.get(f'{self.base_url}/tracker')
        time.sleep(2) 

        # Check the title of the page
        expected_title = 'Food Diary'
        actual_title = driver.title
        print(f"Expected title: {expected_title}")
        print(f"Actual title: {actual_title}")
        self.assertEqual(actual_title, expected_title, "The page title does not match the expected title.")
        print("Food Tracker page is verified.")

        # Verify the values for 'This Day'
        day_carbo = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='leftdiv']//p[contains(text(), 'Carbo:')]/span"))).text
        day_protein = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='leftdiv']//p[contains(text(), 'Protein:')]/span"))).text
        day_fat = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='leftdiv']//p[contains(text(), 'Fat:')]/span"))).text
        print(f"This Day - Carbo: {day_carbo}, Protein: {day_protein}, Fat: {day_fat}")

        # Verify links to Bar Graphs
        bar_graph_day_link = driver.find_element(By.XPATH, "//div[@id='leftdiv']//a").get_attribute('href')
        
        self.assertIn('/bargraph', bar_graph_day_link, "Day bar graph link is incorrect.")
        print("Bar graph links are verified.")

        #about
        driver.get(f'{self.base_url}/about')
        expected_title_listview = 'Food Diary'
        actual_title_listview = driver.title
        self.assertEqual(actual_title_listview, expected_title_listview, "The about page title does not match the expected title.")
        print("About page is verified.")
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()

if __name__=="__main__":
    unittest.main()