#!/usr/bin/env python

class inventoryAllocation:

    # Define shipment validation method
    def findShipment(orders,warehouses):
        inventoryKey = 'inventory'
        nameKey = 'name'
        shipment = []

        for order in orders:
            if type(order) != str:
                raise TypeError
                
            orderLimit = orders[order]
            allListedInventory = map(lambda warehouse: warehouse[inventoryKey], warehouses)
            productDist = []
            
            for products in allListedInventory:
                productDist+=list(products)
                
            if order in productDist:

                # Filter out warehouses which do not store the order
                # by checking for name and amount in stock 
                validWarehouses = filter(lambda warehouse: order
                                         in str(warehouse), warehouses)
                stockedWarehouses = filter(lambda warehouse:
                                           warehouse[inventoryKey][order] != 0,
                                           validWarehouses)
                stockedWarehouses = list(stockedWarehouses)

                totalOrder = sum(map(lambda inventory:
                                 inventory[inventoryKey][order],
                                 stockedWarehouses.copy()))
                countedStock = 0
               
                # If not enough inventory for current order, shipment is invalid
                if totalOrder < orderLimit or len(stockedWarehouses) == 0:
                    return []

		# Add potential warehouses and amount of inventory they can
		# provide to shipment list
                for warehouse in stockedWarehouses:
                    
                    if warehouse[nameKey] not in str(shipment):
                        shipment.append({warehouse[nameKey]: {}})
                        indexLocation = -1
                    
                    else:
                        
                        for currentCount in range(len(shipment)):
                            
                            if next(iter(shipment[currentCount])) == warehouse[nameKey]:
                                indexLocation = currentCount

                    inStockAmount = warehouse[inventoryKey][order]
							
		    # If is order fulfilled, stop iterating
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
