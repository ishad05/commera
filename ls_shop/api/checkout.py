import frappe

from ls_shop.api.payments import set_charges, system_user_session
from ls_shop.core import _get_cart_quotation
from ls_shop.utils import get_delivery_configuration


@frappe.whitelist()
def apply_shipping_rule():
	cart_quotation = _get_cart_quotation()
	# Saving a Quotation runs ERPNext's get_item_details, which calls Item.check_permission()
	# directly - ignore_permissions never reaches it, only the session user does, and a shopper
	# holds just the Customer role, which carries no read on Item.
	with system_user_session():
		set_charges(cart_quotation)
		cart_quotation.save(ignore_permissions=True)
	return get_delivery_configuration()
