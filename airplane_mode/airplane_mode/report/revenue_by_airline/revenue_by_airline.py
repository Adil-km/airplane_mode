# Copyright (c) 2026, Adil KM and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	chart = {
		"data":{
			"labels":[x[0] for x in data],
			"datasets":[{"values": [x[1] for x in data]}],
		},
		"type":"donut"
	}

	total_revenue = sum(chart["data"]["datasets"][0]["values"])
	report_summary = [
		{
		 	"value": total_revenue,
			"indicator": "Green",
			"label": _("Total Revenue"),
			"datatype": "Currency", 
			}
		]
	return columns, data, None, chart, report_summary


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options":"Airline"
		},
		{
			"label": _("Revenue"),
			"fieldname": "revenue",
			"fieldtype": "Currency",
		}
	]

def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	tickets = frappe.get_all(
		"Airplane Ticket",
		fields=["flight", {"SUM":"total_amount", "AS":"total_amount"}],
		filters={"docstatus":1},
		group_by="flight"
		)

	temp = {}
	res = []
	for t in tickets:
		flight = frappe.get_doc("Airplane Flight",t['flight']).airplane
		airplane = frappe.get_doc("Airplane", flight,).airline
		if airplane in temp:
			temp[airplane] += t['total_amount']
		else:
			temp[airplane] = t['total_amount']

	for i in frappe.get_all("Airline", fields=["name"]):
		if i.name not in temp:
			temp[i.name] = 0

	for t in temp:
		a = [t, temp[t]]
		res.append(a)

	return res
