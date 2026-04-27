// Copyright (c) 2026, Adil KM and contributors
// For license information, please see license.txt

frappe.ui.form.on("Airline", {
	refresh(frm) {
        let website_link = frm.doc.website
        if (website_link){
            frm.add_web_link(website_link, "Visit Website")
        }
	},
});
