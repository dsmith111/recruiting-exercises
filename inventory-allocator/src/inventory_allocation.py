
class InventoryAllocation:

    def __init__(self, order, inventory):

        self.order = order
        self.inventory = inventory
        self.amount_needed = order
        self.shipment = []
        self.name_key = "name"
        self.inventory_key = "inventory"

    def valid_inventory(self, local_inventory_names):

        matching_order = map(lambda order: order in local_inventory_names,
                             self.order.keys())
        matching_order = any(matching_order)
        return matching_order


    def compare_amount(self, local_inventory, local_inventory_products, company_name):
        first = True
        for order in self.order.keys():

            if order in local_inventory_products:
                if first:
                    self.shipment.append({company_name: {}})
                    first = False

                difference =  self.amount_needed[order] - local_inventory[order]

                if local_inventory[order] == 0 or self.amount_needed[order] == 0:
                    continue

                if difference >= 0:
                    amount_provided = local_inventory[order]
                else:
                    amount_provided = self.amount_needed[order]

                self.shipment[-1][company_name].update({order: amount_provided})
                self.amount_needed[order] -= amount_provided


    def check_type(self):

        logic_array = map(lambda order: type(order) != str, self.order.keys())
        logic_array2 = map(lambda name: type(name[self.name_key]) != str, self.inventory)
        if any(logic_array) or any(logic_array2):
            raise TypeError

    def shipment_validation(self):

        # Raise error if wrong data type
        self.check_type()

        for warehouse in self.inventory:

            if sum(self.amount_needed.values()) == 0:
                break

            local_inventory = warehouse[self.inventory_key]
            local_inventory_products = local_inventory.keys()
            company_name = warehouse[self.name_key]
            matching = self.valid_inventory(local_inventory_products)

            if matching:
                self.compare_amount(local_inventory, local_inventory_products, company_name)
            else:
                continue

        if sum(self.amount_needed.values()) == 0:
            return self.shipment

        return []
