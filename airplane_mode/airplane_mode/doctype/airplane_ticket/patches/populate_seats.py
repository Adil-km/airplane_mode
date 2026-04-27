import frappe

def execute():
    tickets = frappe.get_all("Airplane Ticket", pluck="name")
    for t in tickets:
        ticket = frappe.get_doc("Airplane Ticket", t)
        if not ticket.seat:
            ticket.set_seat()
            ticket.save()

    frappe.db.commit()