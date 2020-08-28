#!/usr/bin/env python

class inventoryAllocation:

#     def __init__(self, orders, warehouses):
#         self.orders = orders
#         self.warehouses = warehouses

    # Define shipment validation method
    def findShipment(orders,warehouses):
        inventoryKey = 'inventory'
        nameKey = 'name'
        shipment = []

        for order in orders:
            if type(order) != str:
                raise TypeError
                
            orderLimit = orders[order]
            inventoryAcrossAll = map(lambda x: x[inventoryKey], warehouses)
            productDist = []
            
            for products in inventoryAcrossAll:
                productDist+=list(products)
                
            if order in productDist:
                # Filter out warehouses which do not store the order,
                # then filter out those which do hold the product,
                # but have zero in stock
                validWarehouses = filter(lambda warehouse: order
                                         in str(warehouse), warehouses)
                stockedWarehouses = filter(lambda warehouse:
                                           warehouse[inventoryKey][order] != 0,
                                           validWarehouses)
                stockedWarehouses = list(stockedWarehouses)
                # Create variable summing up quantity of
                # order across all warehouses

                totalOrder = sum(map(lambda inventory:
                                 inventory[inventoryKey][order],
                                 stockedWarehouses.copy()))
                countedStock = 0
                if totalOrder < orderLimit or len(stockedWarehouses) == 0:
                    return []

                # Iterate through warehouses and add the company name &
                # amount of the order they can provide
                for warehouse in stockedWarehouses:
                    
                    # If company not already present, then add them
                    # Otherwise find their indexed location
                    if warehouse[nameKey] not in str(shipment):
                        shipment.append({warehouse[nameKey]: {}})
                        indexLocation = -1
                    
                    else:
                        
                        for currentCount in range(len(shipment)):
                            
                            if next(iter(shipment[currentCount])) == warehouse[nameKey]:
                                indexLocation = currentCount

                    # Set variable for the amount of the order
                    # the current warehouse has in stock
                    inStockAmount = warehouse[inventoryKey][order]

                    # If the current order is fulfilled,
                    # break loop and move to next,
                    # otherwise continue calculating amount of product left to
                    # ship while adding its warehouse
                    if inStockAmount + countedStock >= orderLimit:
                        amountNeeded = orderLimit - countedStock
                        shipment[indexLocation][warehouse[nameKey]].update({order: amountNeeded})
                        break
                    
                    else:
                        countedStock += inStockAmount
                        shipment[indexLocation][warehouse[nameKey]].update({order: inStockAmount})
            
            else:
                return []
        
        return shipment
