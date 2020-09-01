#!/usr/bin/env python

class InventoryAllocation:

    # Define shipment validation method
    def find_shipment(orders,warehouses):
        inventory_key = 'inventory'
        name_key = 'name'
        shipment = []

        for order in orders:
            if type(order) != str:
                raise TypeError
                
            order_limit = orders[order]
            all_listed_inventory = map(lambda warehouse: warehouse[inventory_key], warehouses)
            product_dist = []
            
            for products in all_listed_inventory:
                product_dist+=list(products)
                
            if order in product_dist:

                # Filter out warehouses which do not store the order
                # by checking for name and amount in stock 
                valid_warehouses = filter(lambda warehouse: order
                                         in str(warehouse), warehouses)
                stocked_warehouses = filter(lambda warehouse:
                                           warehouse[inventory_key][order] != 0,
                                           valid_warehouses)
                stocked_warehouses = list(stocked_warehouses)

                total_order = sum(map(lambda inventory:
                                 inventory[inventory_key][order],
                                 stocked_warehouses.copy()))
                counted_stock = 0
               
                # If not enough inventory for current order, shipment is invalid
                if total_order < order_limit or len(stocked_warehouses) == 0:
                    return []

                # Add potential warehouses and amount of inventory they can
                # provide to shipment list
                for warehouse in stocked_warehouses:
                    
                    if warehouse[name_key] not in str(shipment):
                        shipment.append({warehouse[name_key]: {}})
                        index_location = -1
                    
                    else:
                        
                        for current_count in range(len(shipment)):
                            
                            if next(iter(shipment[current_count])) == warehouse[name_key]:
                                index_location = current_count

                    amount_in_stock = warehouse[inventory_key][order]
                            
                    # If is order fulfilled, stop iterating
                    if amount_in_stock + counted_stock >= order_limit:
                        amount_needed = order_limit - counted_stock
                        shipment[index_location][warehouse[name_key]].update({order: amount_needed})
                        break
                    
                    else:
                        counted_stock += amount_in_stock
                        shipment[index_location][warehouse[name_key]].update({order: amount_in_stock})
            
            else:
                return []
        
        return shipment