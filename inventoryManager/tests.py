from django.test import TestCase
from django.contrib.auth.models import User
from inventoryManager.models import *
from datetime import *
from inventoryManager import views

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

import time

# This is the unit tests for creating and deleting organizations, orders and orderitems
# baseline unit tests
class InventoryManagerTester(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='tester',
											password='password',
											email = 'test@nsysdev.com',
											first_name='Test',
											last_name='Tester')
											
		login = self.client.login(username='testuser', password='12345')
		
	# test if you can create an organization
	def testCreateOrg(self):
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		# verify the organization exists, with the right name
		self.assertTrue(Organization.objects.filter(name = "TestOrg").exists())
		
		# verify the organization data
		testOrg = Organization.objects.get(name = "TestOrg")
		self.assertEqual(testOrg.associatedUser, self.user)
		self.assertEqual(testOrg.about, "Test description")
		
	# test delete organization
	def testDeleteOrg(self):
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		# verify the organization exists, with the right name
		self.assertTrue(Organization.objects.filter(name = "TestOrg").exists())
		
		# verify the organization data
		testOrg = Organization.objects.get(name = "TestOrg")
		orgId = testOrg.id
		
		# delete and verify
		testOrg.delete()
		self.assertFalse(Organization.objects.filter(id=orgId).exists())
		
	
	# Test to create an order
	def testCreateOrder(self):
		testName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		Order.objects.create(title = testName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
							
		# test that the order was made and has the data given
		# get an order by the title. if this fails the order wasn't made.
		testOrder = Order.objects.get(title = testName)
		self.assertTrue(Order.objects.filter(title=testName).exists())
		
		# test the values
		self.assertEqual(testOrder.organization, Organization.objects.get(name = "TestOrg"))
		self.assertEqual(testOrder.title, testName)
		self.assertEqual(testOrder.description, testDescr)
		self.assertEqual(testOrder.posted, date(year, month, day))
		
	# test that you can delete an order
	def testDeleteOrder(self):
		testName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		Order.objects.create(title = testName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
							
		# test that the order was made and has the data given
		# get an order by the title. if this fails the order wasn't made.
		testOrder = Order.objects.get(title = testName)
		id = testOrder.id
		testOrder.delete()
		self.assertFalse(Order.objects.filter(id=id).exists())
		
	# Test to create an order item
	def testCreateOrderItem(self):
		testOrderName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		testItemName = "TestOrderItem"
		testNsn = "129FJ9R8ERG9832"
		testQuantity = int(4)
		testCost = float(12.36)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		Order.objects.create(title = testOrderName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
		testOrder = Order.objects.get(title=testOrderName)
							
		# create the orderitem
		OrderItem.objects.create(itemName=testItemName, itemNsn = testNsn,
								itemQuantity=testQuantity, itemCost = testCost, order = testOrder)
								
		# make sure the order item exists
		self.assertTrue(OrderItem.objects.filter(itemName=testItemName).exists())
		
	# Test to delete an order item
	def testDeleteOrderItem(self):
		testOrderName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		testItemName = "TestOrderItem"
		testNsn = "129FJ9R8ERG9832"
		testQuantity = int(4)
		testCost = float(12.36)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		Order.objects.create(title = testOrderName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
		testOrder = Order.objects.get(title=testOrderName)
							
		# create the orderitem
		OrderItem.objects.create(itemName=testItemName, itemNsn = testNsn,
								itemQuantity=testQuantity, itemCost = testCost, order = testOrder)
		
		testItem = OrderItem.objects.get(itemName=testItemName)
		
		# delete the item
		testItem.delete()
		
		# verify it's deleted
		self.assertFalse(OrderItem.objects.filter(itemName=testItemName).exists())
		
	# Test to delete an order with items. everything should be gone
	def testDeleteOrderWithItems(self):
		testOrderName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		testItemName = "TestOrderItem"
		testNsn = "129FJ9R8ERG9832"
		testQuantity = int(4)
		testCost = float(12.36)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		Order.objects.create(title = testOrderName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
		testOrder = Order.objects.get(title=testOrderName)
							
		# create the orderitem
		OrderItem.objects.create(itemName=testItemName, itemNsn = testNsn,
								itemQuantity=testQuantity, itemCost = testCost, order = testOrder)
		
		testItem = OrderItem.objects.get(itemName=testItemName)
		
		# delete the order, but save the ids
		orderId = testOrder.id
		itemId = testItem.id
		testOrder.delete()
		
		# verify the order's deleted
		self.assertFalse(Order.objects.filter(id=orderId).exists())
		
		# verify item's deleted
		self.assertFalse(OrderItem.objects.filter(id=itemId).exists())

	# Test to delete an organization with orders. everything should be gone
	def testOrgWithOrders(self):
		testOrderName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		testItemName = "TestOrderItem"
		testNsn = "129FJ9R8ERG9832"
		testQuantity = int(4)
		testCost = float(12.36)
		
		# create the organization and order
		Organization.objects.create(name = "TestOrg", about = "Test description", associatedUser = self.user)
		testOrg = Organization.objects.get(name = "TestOrg")
		
		Order.objects.create(title = testOrderName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
		testOrder = Order.objects.get(title=testOrderName)
							
		# create the orderitem
		OrderItem.objects.create(itemName=testItemName, itemNsn = testNsn,
								itemQuantity=testQuantity, itemCost = testCost, order = testOrder)
		
		testItem = OrderItem.objects.get(itemName=testItemName)
		
		# delete the organization, but save the ids
		orgId = testOrg.id
		orderId = testOrder.id
		itemId = testItem.id
		testOrg.delete()
		
		#verify the organization's deleted
		self.assertFalse(Organization.objects.filter(id=orgId).exists())
		
		# verify the order's deleted
		self.assertFalse(Order.objects.filter(id=orderId).exists())
		
		# verify item's deleted
		self.assertFalse(OrderItem.objects.filter(id=itemId).exists())
		

# Selenium tests
class SeleniumTester(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.selenium = WebDriver()
		cls.selenium.implicitly_wait(10)
		
	@classmethod
	def tearDownClass(cls):
		crap = 1 + 1
		cls.selenium.quit()
		super().tearDownClass()
	
	# selenium test to create a user and login	
	def testCreateLoginUser(self):
		userName = "TestUser"
		password = "password"
		email = "test@nsysdev.com"
		firstName = "Test"
		lastName = "Tester"
		
		self.selenium.get(f"{self.live_server_url}")
		
		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
		else:
			# we have to click the hamburger toggler first, then click the account button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
			
		# hit register
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Register")]').click()
		
		# verify on register page
		self.assertTrue(self.selenium.find_element(By.XPATH, "//*[text() = 'Create User']"))
		
		# populate user creation form
		usernameInput = self.selenium.find_element(By.ID, "id_username")
		usernameInput.send_keys(userName)
		
		passwordInput = self.selenium.find_element(By.ID, "id_password")
		passwordInput.send_keys(password)
		
		emailInput = self.selenium.find_element(By.ID, "id_email")
		emailInput.send_keys(email)
		
		firstNameInput = self.selenium.find_element(By.ID, "id_first_name")
		firstNameInput.send_keys(firstName)
		
		lastNameInput = self.selenium.find_element(By.ID, "id_last_name")
		lastNameInput.send_keys(lastName)
		
		# hit submit
		self.selenium.find_element(By.NAME, 'submit').click()
		
		# now login
		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
		else:
			# we have to click the hamburger toggler first, then click the account button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
			
		# hit login
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()
		
		# verify on login page
		self.assertTrue(self.selenium.find_element(By.XPATH, "//*[text() = 'User Login']"))
		
		# populate user login form
		usernameInput = self.selenium.find_element(By.ID, "id_username")
		usernameInput.send_keys(userName)
		
		passwordInput = self.selenium.find_element(By.ID, "id_password")
		passwordInput.send_keys(password)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()

		get_url = self.selenium.current_url
		print("The current url is:"+str(get_url))
		
		# by this point we should be logged in. the way to check is the welcome text
		self.assertTrue(self.selenium.find_element(By.XPATH, '//*[contains(text(), "Welcome")]'))
		
		
	# selenium test to login and create an organization	
	def testCreateOrg(self):
		orgName = "TestOrg"
		orgDscr = "TestOrg description"
		userName = "TestUser"
		password = "password"
		
		
		# we do need to create a user, since database data is rolled back after each test
		# we'll use the old fashioned way in this case since testing creating a user "the right way"
		# is handled elsewhere
		User.objects.create_user(username= userName,
											password= password,
											email = 'test@nsysdev.com',
											first_name='Test',
											last_name='Tester')
		
		# first login from homepage
		self.selenium.get(f"{self.live_server_url}")
		
		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
		else:
			# we have to click the hamburger toggler first, then click the account button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
			
		# hit login
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()
		
		# verify on login page
		self.assertTrue(self.selenium.find_element(By.XPATH, "//*[text() = 'User Login']"))
		
		# populate user login form
		usernameInput = self.selenium.find_element(By.ID, "id_username")
		usernameInput.send_keys(userName)
		
		passwordInput = self.selenium.find_element(By.ID, "id_password")
		passwordInput.send_keys(password)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()
		
		# now go to the organizations page
		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Manager")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Manager")]').click()
		else:
			# we have to click the hamburger toggler first, then click the manage button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Manager")]').click()
			
		# hit organizations
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Organizations")]').click()
		
		# now hit create organization
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Create Organization")]').click()
		
		# assert that we are on the right page
		self.assertTrue("Create: Organization" in self.selenium.page_source)
		
		# now populate the form
		orgNameInput = self.selenium.find_element(By.ID, "id_name")
		orgNameInput.send_keys(orgName)
		
		orgDescInput = self.selenium.find_element(By.ID, "id_about")
		orgDescInput.send_keys(orgDscr)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()

		print("From testCreateOrg")
		get_url = self.selenium.current_url
		print("The current url is:"+str(get_url))
		
		# we should be redirected to org list page. verify that the org name is there
		self.assertTrue(orgName in self.selenium.page_source)
		
	# selenium test to create an order	
	def testCreateOrder(self):
		orgName = "TestOrg"
		orgDscr = "TestOrg description"
		
		testName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		userName = "TestUser"
		password = "password"
		
		# create a user
		User.objects.create_user(username= userName,
											password= password,
											email = 'test@nsysdev.com',
											first_name='Test',
											last_name='Tester')
		
		# create the org the old fashioned way
		Organization.objects.create(name = "TestOrg", about = "Test description",
									associatedUser = User.objects.get(username = userName))
		
		# verify organization exists
		testOrg = Organization.objects.get(name = orgName)
		orgId = testOrg.id
		self.assertTrue(Organization.objects.filter(id=orgId).exists())
		
		# now we get to actually making the order
		# first login from homepage
		self.selenium.get(f"{self.live_server_url}")

		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
		else:
			# we have to click the hamburger toggler first, then click the account button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
			
		# hit login
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()
		
		# verify on login page
		self.assertTrue(self.selenium.find_element(By.XPATH, "//*[text() = 'User Login']"))
		
		# populate user login form
		usernameInput = self.selenium.find_element(By.ID, "id_username")
		usernameInput.send_keys(userName)
		
		passwordInput = self.selenium.find_element(By.ID, "id_password")
		passwordInput.send_keys(password)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()
		
		# we'll go through the chain starting from homepage
		self.selenium.get(f"{self.live_server_url}")
		self.selenium.find_element(By.XPATH, '//*[text()="View"]').click()
		
		# verify we're at the org page
		self.assertTrue(orgName in self.selenium.page_source)
		
		# click new order
		self.selenium.find_element(By.XPATH, '//*[text()="New"]').click()
		
		# make sure we're at the order create page
		self.assertTrue("Create: Order" in self.selenium.page_source)
		
		# populate fields
		postedInput = self.selenium.find_element(By.ID, "id_posted")
		postedInput.send_keys(str(month) + str(day) + str(year))
		
		titleInput = self.selenium.find_element(By.ID, "id_title")
		titleInput.send_keys(testName)
		
		descrInput = self.selenium.find_element(By.ID, "id_description")
		descrInput.send_keys(testDescr)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()
		
		# make sure order was created
		testOrder = Order.objects.get(title = testName)
		id = testOrder.id
		self.assertTrue(Order.objects.filter(id=id).exists())

		print("From testCreateOrder")
		get_url = self.selenium.current_url
		print("The current url is:"+str(get_url))
		
		# we should also be at the org page now. verify the order's on the page
		self.assertTrue(orgName in self.selenium.page_source)
		self.assertTrue(testName in self.selenium.page_source)
		self.assertTrue(testDescr in self.selenium.page_source)
		
	# selenium test to create an order item
	def testCreateOrderItem(self):
		orgName = "TestOrg"
		orgDscr = "TestOrg description"
		
		testOrderName = "TestOrder"
		testDescr = "Test Order"
		year = int(2023)
		month = int(1)
		day = int(1)
		testPosted = str(year) + '-' + str(month) + '-' + str(day)
		
		testItemName = "TestOrderItem"
		testNsn = "129FJ9R8ERG9832"
		testQuantity = int(4)
		testCost = float(12.36)
		
		userName = "TestUser"
		password = "password"
		
		# create a user
		User.objects.create_user(username= userName,
											password= password,
											email = 'test@nsysdev.com',
											first_name='Test',
											last_name='Tester')
		
		# create the org and order the old fashioned way
		Organization.objects.create(name = "TestOrg", about = "Test description",
									associatedUser = User.objects.get(username = userName))
		Order.objects.create(title = testOrderName, organization = Organization.objects.get(name = "TestOrg"),
							description = testDescr, posted = testPosted)
		
		# verify organization and order exists
		testOrg = Organization.objects.get(name = orgName)
		orgId = testOrg.id
		self.assertTrue(Organization.objects.filter(id=orgId).exists())
		
		testOrder = Order.objects.get(title=testOrderName)
		orderId = testOrder.id
		self.assertTrue(Order.objects.filter(id=orderId).exists())
		
		self.selenium.get(f"{self.live_server_url}")
		
		# now we login
		# we need to check if the navbar was converted to a hamburger menu
		if (self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').is_displayed()):
			# the account thing is shown, and not collapsed in so we can click it
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
		else:
			# we have to click the hamburger toggler first, then click the account button
			self.selenium.find_element(By.ID, "nav_toggler").click()
			self.selenium.find_element(By.XPATH, '//*[contains(text(), "Account")]').click()
			
		# hit login
		self.selenium.find_element(By.XPATH, '//*[contains(text(), "Log in")]').click()
		
		# verify on login page
		self.assertTrue(self.selenium.find_element(By.XPATH, "//*[text() = 'User Login']"))
		
		# populate user login form
		usernameInput = self.selenium.find_element(By.ID, "id_username")
		usernameInput.send_keys(userName)
		
		passwordInput = self.selenium.find_element(By.ID, "id_password")
		passwordInput.send_keys(password)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()
		
		# go to org page from home
		self.selenium.find_element(By.XPATH, '//*[text()="View"]').click()
		
		# go to order page from org
		self.selenium.find_element(By.XPATH, '//*[text()="View"]').click()
		
		# go to add item page
		self.selenium.find_element(By.XPATH, '//*[text()="Add an item"]').click()
		
		# populate the form
		itemNameInput = self.selenium.find_element(By.ID, "id_itemName")
		itemNameInput.send_keys(testItemName)
		
		itemNsnInput = self.selenium.find_element(By.ID, "id_itemNsn")
		itemNsnInput.send_keys(testNsn)
		
		itemQuantityInput = self.selenium.find_element(By.ID, "id_itemQuantity")
		itemQuantityInput.send_keys(testQuantity)
		
		itemCostInput = self.selenium.find_element(By.ID, "id_itemCost")
		itemCostInput.send_keys(testCost)
		
		# hit submit
		self.selenium.find_element(By.NAME, "submit").click()
		
		# we should also be at the order page now. verify the item's on the page
		self.assertTrue(testItemName in self.selenium.page_source)
		self.assertTrue(testNsn in self.selenium.page_source)
		
