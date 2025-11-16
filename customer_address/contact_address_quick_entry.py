import frappe

def customer_address_link(doc, method):
    """Handle customer operations after insert/update (الكود الأصلي)."""
    
    # المنطق الأصلي لعنوان الشركة (بدون تغيير)
    if getattr(doc, "is_company_address", None):
        link_customer_to_company_address(doc)
    else:
        unlink_customer_from_company_address(doc)


# الدوال الأصلية بدون تغيير
def link_customer_to_company_address(doc):
    address = frappe.get_all("Address", filters={"is_your_company_address": 1}, fields=["name"])
    if not address:
        return
    address_doc = frappe.get_doc("Address", address[0].name)
    if not any(l.link_doctype == "Customer" and l.link_name == doc.name for l in address_doc.links):
        address_doc.append("links", {
            "link_doctype": "Customer",
            "link_name": doc.name
        })
        address_doc.save(ignore_permissions=True)

def unlink_customer_from_company_address(doc):
    address = frappe.get_all("Address", filters={"is_your_company_address": 1}, fields=["name"])
    if not address:
        return
    address_doc = frappe.get_doc("Address", address[0].name)
    new_links = [l for l in address_doc.links if not (l.link_doctype == "Customer" and l.link_name == doc.name)]
    if len(new_links) != len(address_doc.links):
        address_doc.links = new_links
        address_doc.save(ignore_permissions=True)