from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from inventoryManager.models import *
from datetime import *
from inventoryManager import views

# This is the unit tests for creating and deleting organizations, orders and orderitems
# Editing order items will be tested with the selenium thingy

# first test, create a user
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