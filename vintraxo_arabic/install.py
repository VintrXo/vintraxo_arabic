"""Refresh translation caches without changing users, permissions or business data."""
def refresh_translations():
    import frappe
    from frappe.translate import clear_cache
    clear_cache()
    frappe.clear_cache()
