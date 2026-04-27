// Copyright (c) 2026, Adil KM and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airplane Ticket", {
	refresh(frm) {
        frm.add_custom_button("Assign Seat",()=>{
            frappe.prompt({
                label: 'Seat number',
                fieldname: 'seat_number',
                fieldtype: 'Data'
            }, (values) => {
                frm.set_value("seat", values.seat_number)
            })

        },"Actions")
	},
});


