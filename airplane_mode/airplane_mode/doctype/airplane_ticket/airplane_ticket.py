# Copyright (c) 2026, Adil KM and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from airplane_mode.airplane_mode.doctype.airplane_ticket_add_on_item.airplane_ticket_add_on_item import AirplaneTicketAddonItem
		from frappe.types import DF

		add_ons: DF.Table[AirplaneTicketAddonItem]
		amended_from: DF.Link | None
		departure_date: DF.Date
		departure_time: DF.Time
		destination_airport_code: DF.Data | None
		duration_of_flight: DF.Duration
		flight: DF.Link
		flight_price: DF.Currency
		passenger: DF.Link
		seat: DF.Data | None
		source_airport_code: DF.Data | None
		status: DF.Literal["Booked", "Checked-In", "Boarded"]
		total_amount: DF.Currency
	# end: auto-generated types

	def on_refresh():
		
		total_airplane_tickets = frappe.db.count("Airplane Ticket")

		frappe.throw(total_airplane_tickets)


	def before_save(self):
		amount = 0 

		for item in self.add_ons:
			amount += item.amount 
		
		if self.flight_price: 
			self.total_amount = amount + self.flight_price 
		else: 
			frappe.throw("Flight amount is not set!")


	def before_insert(self):
		airplane = frappe.get_doc("Airplane Flight", self.flight).airplane
		airplane_capacity = frappe.get_doc("Airplane", airplane).capacity

		total_airplane_tickets = frappe.db.count(
			"Airplane Ticket",
			{"flight": self.flight}
		)

		if total_airplane_tickets >= airplane_capacity:
			frappe.throw(f"Flight {self.flight} is fully booked.")

		
	def set_seat(self):
		self.seat = str(random.randint(10, 99)) + random.choice("ABCDEF")


	def before_submit(self):
		if self.status != "Boarded":
			frappe.throw("Not Boarded")
		if not self.seat:
			self.set_seat()

	def validate(self):
		seen = set()
		u_addons = []

		for addon in self.add_ons:
			if addon.item not in seen:
				seen.add(addon.item)
				u_addons.append(addon)
		self.add_ons = u_addons
