# Copyright (c) 2025, prasath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.model.workflow import apply_workflow

class EventsAllocation(Document):

	def validate(self):
		if self.start_date > self.end_date:
			frappe.throw("Start Date must be lesser than End Date")	
		self.check_date_existence()

	def check_date_existence(self):		
		date_list=frappe.get_all("Events Allocation",
				  filters={"resource_id":self.resource_id,"name": ["!=", self.name]},
				  fields=["start_date","end_date","name","workflow_state"]
				  )
		for value in date_list:
			if value["workflow_state"]!="Completed":
				if self.start_date < value["end_date"] and self.end_date > value["start_date"]:
					frappe.throw(f"Resource {self.resource_id} is already booked for {value['name']}")			
			
		self.check_available_resource(self.resource_id,self.name1)
		self.update_available_resource(self.resource_id,self.name1)
	
	def update_available_resource(self,resource_id,event_id):
		event_count = frappe.get_value("Events",event_id,"event_count")
		resource_data= frappe.get_doc("Resource",resource_id)
		needs = event_count//50

		if event_count >= 1 and event_count<=50:
			for val in resource_data.resource_table:
				val.room_strength-=event_count
				val.instructors_available-=1
				val.equipment_available-=1

		else:
			for val in resource_data.resource_table:
				val.room_strength-=event_count	
				val.instructors_available-=needs
				val.equipment_available-=needs

		resource_data.save()

                
	def check_available_resource(self,resource_id,event_id):
		event_count = frappe.get_value("Events",event_id,"event_count")
		resource_data = frappe.get_all("Available Resource",
						filters={"parent":resource_id},
						fields=["room_strength","instructors_available","equipment_available"]
					)

		needs = event_count//50
		for resource in resource_data:
			if event_count > resource["room_strength"] or resource["instructors_available"] < needs or resource["equipment_available"]<needs:
				frappe.throw(f"The Resource id {self.resource_id} not have sufficient resource to the selected event")
	

	
def auto_update():
	now = datetime.now()
	allocations= frappe.get_all("Events Allocation",fields=["name1","resource_id","end_date","start_date","name"])
	
	for value in allocations:
		event_count= frappe.get_value("Events",value["name1"],"event_count")
		resource_data= frappe.get_doc("Resource",value["resource_id"])
		allocation_list= frappe.get_doc("Events Allocation",value["name"])

		state = False
		if allocation_list.workflow_state =="Upcomming" and value["start_date"] <= now:
			apply_workflow(allocation_list,"Live")
			state =True

		if allocation_list.workflow_state =="Live" and value["end_date"] <= now :	
			apply_workflow(allocation_list,"Completed")
			state = True
			needs=event_count//50
			if event_count<=50:
				for val in resource_data.resource_table:
					val.room_strength+=event_count
					val.instructors_available+=1
					val.equipment_available+=1

			else:
				for val in resource_data.resource_table:
					val.room_strength+=event_count
					val.instructors_available+=needs
					val.equipment_available+=needs
			
			resource_data.reload()
			resource_data.save()

		if state:
			allocation_list.save()