from selenium import webdriver	# (1)
import unittest
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException #
import time
class NewVisitorTest(LiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
	
	def tearDown(self):
		self.browser.quit()
	
	def wait_for_row_in_list_table(self, row_text):
		MAX_WAIT = 10 #
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text, [row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		browser = webdriver.Firefox()	# (2)
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get(self.live_server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)	# (4)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# She is invited to enter a to-do item sreight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# Edith wonders whether the site will remember her list. Then she sees
		# that the site has generated a unique URL for her --- there is some
		# explanatory text to that effect
		# self.fail('Finish the test!')
		
		# She visits that URL - her to-do list is still there
		# Satisfied, she goes back to sleep
		
#	def test_can_start_a_list_for_one_user(self):
#		self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
#		self.wait_for_row_in_list_table('1: Buy peacock feathers')
	
	def test_multiple_users_can_start_lists_at_different_urls(self):
		self.browser.get(self.live_server_url)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy peacock feathers')
		
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
	
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		
	def test_layout_and_styling(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('testing')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: testing')
		
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
			)
		
		