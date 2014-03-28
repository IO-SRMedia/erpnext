# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
import unittest
from erpnext.accounts.doctype.shipping_rule.shipping_rule import FromGreaterThanToError, ManyBlankToValuesError, OverlappingConditionError

class TestShippingRule(unittest.TestCase):
	def test_from_greater_than_to(self):
		shipping_rule = frappe.get_doc(copy=test_records[0])
		shipping_rule.doclist[1].from_value = 101
		self.assertRaises(FromGreaterThanToError, shipping_rule.insert)
		
	def test_many_zero_to_values(self):
		shipping_rule = frappe.get_doc(copy=test_records[0])
		shipping_rule.doclist[1].to_value = 0
		self.assertRaises(ManyBlankToValuesError, shipping_rule.insert)
		
	def test_overlapping_conditions(self):
		for range_a, range_b in [
			((50, 150), (0, 100)),
			((50, 150), (100, 200)),
			((50, 150), (75, 125)),
			((50, 150), (25, 175)),
			((50, 150), (50, 150)),
		]:
			shipping_rule = frappe.get_doc(copy=test_records[0])
			shipping_rule.doclist[1].from_value = range_a[0]
			shipping_rule.doclist[1].to_value = range_a[1]
			shipping_rule.doclist[2].from_value = range_b[0]
			shipping_rule.doclist[2].to_value = range_b[1]
			self.assertRaises(OverlappingConditionError, shipping_rule.insert)

test_records = [
	[
		{
			"doctype": "Shipping Rule",
			"label": "_Test Shipping Rule",
			"name": "_Test Shipping Rule",
			"calculate_based_on": "Net Total",
			"company": "_Test Company",
			"account": "_Test Account Shipping Charges - _TC",
			"cost_center": "_Test Cost Center - _TC"
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 0,
			"to_value": 100,
			"shipping_amount": 50.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 101,
			"to_value": 200,
			"shipping_amount": 100.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 201,
			"shipping_amount": 0.0
		},
		{
			"doctype": "Applicable Territory",
			"parentfield": "valid_for_territories",
			"territory": "_Test Territory"
		}
	],
	[
		{
			"doctype": "Shipping Rule",
			"name": "_Test Shipping Rule - India",
			"label": "_Test Shipping Rule - India",
			"calculate_based_on": "Net Total",
			"company": "_Test Company",
			"account": "_Test Account Shipping Charges - _TC",
			"cost_center": "_Test Cost Center - _TC"
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 0,
			"to_value": 100,
			"shipping_amount": 50.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 101,
			"to_value": 200,
			"shipping_amount": 100.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 201,
			"shipping_amount": 0.0
		},
		{
			"doctype": "Applicable Territory",
			"parentfield": "valid_for_territories",
			"territory": "_Test Territory India"
		}
	],
	[
		{
			"doctype": "Shipping Rule",
			"name": "_Test Shipping Rule - Rest of the World",
			"label": "_Test Shipping Rule - Rest of the World",
			"calculate_based_on": "Net Total",
			"company": "_Test Company",
			"account": "_Test Account Shipping Charges - _TC",
			"cost_center": "_Test Cost Center - _TC"
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 0,
			"to_value": 1000,
			"shipping_amount": 500.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 1001,
			"to_value": 2000,
			"shipping_amount": 1000.0
		},
		{
			"doctype": "Shipping Rule Condition",
			"parentfield": "shipping_rule_conditions",
			"from_value": 2001,
			"shipping_amount": 1500.0
		},
		{
			"doctype": "Applicable Territory",
			"parentfield": "valid_for_territories",
			"territory": "_Test Territory Rest Of The World"
		}
	],
]