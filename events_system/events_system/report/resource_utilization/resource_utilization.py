# Copyright (c) 2025, prasath and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns =[
		{
			"label":"Resource",
			"fieldname":"resource",
			"fieldtype":"Data",
		},
		{
			"label":"Hours Utilized",
			"fieldname":"count",
			"fieldtype":"Float",
		},

	]
	
	data=[]
	from_date=filters.get("from_date")
	to_date=filters.get("to_date")
	status = filters.get("event_status")

	allocation = frappe.get_all("Events Allocation",
	 	filters=[
				["start_date",">=",from_date],
				["end_date","<=",to_date],
				["workflow_state","=",status]
			],
		fields=["start_date","end_date","resource_id"]
	)

	resource_map={}
	for date in allocation:
		time_limit = (date["end_date"]-date["start_date"]).total_seconds()
		total_hours=time_limit/3600

		if date["resource_id"] in resource_map:
			resource_map[date["resource_id"]]+=total_hours
		else:
			resource_map[date["resource_id"]]=total_hours

	for res,count in resource_map.items():
		data.append(
			{
				"resource":res,
				"count":count,
			}
		)

	
	return columns,data
