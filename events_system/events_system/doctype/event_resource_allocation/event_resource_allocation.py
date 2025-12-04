# Copyright (c) 2025, prasath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EventResourceAllocation(Document):
    pass
	
	# def validate(self):
	# 	self.check_date_existence()

	# def check_date_existence(self):
	# 	print(1111111111)
		
	# 	date_list=frappe.get_list("Events Allocation",fields=["start_date","end_date"])

	# 	if self.start_date!= date_list[0]["start_date"] and self.end_date != date_list[0]["end_date"]:
	# 		frappe.throw("Error")

