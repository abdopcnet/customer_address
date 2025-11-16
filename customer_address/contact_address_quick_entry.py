import frappe
from frappe import _


def customer_address_link(doc, method):
    """Handle customer operations after insert/update (الكود الأصلي)."""
    try:
        # المنطق الأصلي لعنوان الشركة (بدون تغيير)
        if getattr(doc, "is_company_address", None):
            link_customer_to_company_address(doc)
        else:
            unlink_customer_from_company_address(doc)
    except Exception:
        frappe.log_error(
            title=_("customer_address_link failed for Customer {0}").format(doc.name))
        frappe.throw(_("Error in customer_address_link"))


# الدوال الأصلية بدون تغيير
def link_customer_to_company_address(doc):
    try:
        address = frappe.get_all(
            "Address", filters={"is_your_company_address": 1}, fields=["name"])
        if not address:
            frappe.logger().error(
                "[[contact_address_quick_entry.py]] link_customer_to_company_address: No company address found")
            return
        address_doc = frappe.get_doc("Address", address[0].name)
        if not any(l.link_doctype == "Customer" and l.link_name == doc.name for l in address_doc.links):
            address_doc.append("links", {
                "link_doctype": "Customer",
                "link_name": doc.name
            })
            address_doc.save(ignore_permissions=True)
            frappe.logger().error(
                f"[[contact_address_quick_entry.py]] link_customer_to_company_address: Linked customer {doc.name} to address {address_doc.name}")
    except Exception:
        frappe.log_error(title=_(
            "link_customer_to_company_address failed for Customer {0}").format(doc.name))
        frappe.throw(_("Error linking customer to company address"))


def unlink_customer_from_company_address(doc):
    try:
        address = frappe.get_all(
            "Address", filters={"is_your_company_address": 1}, fields=["name"])
        if not address:
            frappe.logger().error(
                "[[contact_address_quick_entry.py]] unlink_customer_from_company_address: No company address found")
            return
        address_doc = frappe.get_doc("Address", address[0].name)
        new_links = [l for l in address_doc.links if not (
            l.link_doctype == "Customer" and l.link_name == doc.name)]
        if len(new_links) != len(address_doc.links):
            address_doc.links = new_links
            address_doc.save(ignore_permissions=True)
            frappe.logger().error(
                f"[[contact_address_quick_entry.py]] unlink_customer_from_company_address: Unlinked customer {doc.name} from address {address_doc.name}")
    except Exception:
        frappe.log_error(title=_(
            "unlink_customer_from_company_address failed for Customer {0}").format(doc.name))
        frappe.throw(_("Error unlinking customer from company address"))
