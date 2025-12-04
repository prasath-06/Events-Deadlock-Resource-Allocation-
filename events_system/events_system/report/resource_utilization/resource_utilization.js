// Copyright (c) 2025, prasath and contributors
// For license information, please see license.txt

frappe.query_reports["Resource Utilization"] = {
	"filters": [
		{
			"label":"From Date",
			"fieldname":"from_date",
			"fieldtype":"Datetime"
		},
		{
			"label":"To Date",
			"fieldname":"to_date",
			"fieldtype":"Datetime"
		},
		{
			"lable":"Event Status",
			"fieldname":"event_status",
			"fieldtype":"Select",
			"options":"\nLive\nUpcomming\nCompleted"
		}
	]
};

