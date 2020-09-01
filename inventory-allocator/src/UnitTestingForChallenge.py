#!/usr/bin/env python

import unittest
from inventory_allocation import InventoryAllocation


class AllocationTesting(unittest.TestCase):

    # Tests below on varying order size and inventory distribution

    # Test 1: One order, valid shipment, one providing warehouse,
    # one listed warehouse
    def test_OneOrder_ValidShipment_OneProviding_OneWarehouse(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])

    # Test 2: One order, valid shipment, one providing warehouse,
    # multiple listed warehouses
    def test_OneOrder_ValidShipment_OneProviding_MultipleWarehouses(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}},
                                 {'name': 'dm', 'inventory': {'apple': 3}}
                                 ]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])

    # Test 3: One order, valid shipment, multiple providing warehouses,
    # multiple listed warehouses
    def test_OneOrder_ValidShipment_MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 10}
        inventory_distribution = [
                                    {'name': 'dm', 'inventory': {'apple': 5}},
                                    {'name': 'owd', 'inventory': {'apple': 5}}
                                 ]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [
                                    {'dm': {'apple': 5}},
                                    {'owd': {'apple': 5}}
                                    ])

    # Test 4: One order, no valid shipments, one listed warehouse
    def test_OneOrder_InvalidShipment__OneProviding_OneWarehouse(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 0}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [])

    # Test 5: One order, no valid shipments, multiple listed warehouses
    def test_OneOrder_InvalidShipment__OneProviding_MultipleWarehouses(self):
        order = {'apple': 2}
        inventory_distribution = [
                                    {'name': 'dm', 'inventory': {'apple': 0}},
                                    {'name': 'owd', 'inventory': {'apple': 1}}
                                 ]

        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [])

    # Test 6: Multiple orders, valid shipment, one providing warehouse,
    # one listed warehouse
    def test_MultipleOrders_ValidShipment_OneProviding_OneWarehouse(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1, 'orange': 2}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1, 'orange': 2}}])

    # Test 7: Multiple orders, valid shipment, one providing warehouses,
    # multiple listed warehouses
    def test_MultipleOrders_ValidShipment_OneProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [
                                    {'name': 'dm', 'inventory': {'apple': 1, 'orange': 2}},
                                    {'name': 'owd', 'inventory': {'banana': 3}}
                                 ]

        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [{'dm': {'apple': 1, 'orange': 2}}])

    # Test 8: Multiple orders, valid shipment, multiple providing warehouses,
    # multiple listed warehouses
    def test_MultipleOrders_ValidShipment_MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [
                                    {'name': 'dm', 'inventory': {'apple': 1, 'orange': 1}},
                                    {'name': 'owd', 'inventory': {'orange': 1}}
                                 ]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [
                                    {'dm': {'apple': 1, 'orange': 1}},
                                    {'owd': {'orange': 1}}
                                    ])

    # Test 9: Multiple orders, no valid shipments, one listed warehouse
    def test_MultipleOrders_InvalidShipment__OneProviding_OneWarehouse(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [])

    # Test 10: Multiple orders, no valid shipments, multiple listed warehouses
    def test_MultipleOrders_InvalidShipment__MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [
                                    {'name': 'dm', 'inventory': {'apple': 0, 'orange': 1}},
                                    {'name': 'owd', 'inventory': {'orange': 1}}
                                 ]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [])
        
    # Test 11: Orders are not present in warehouses
    def test_OrderIsNotPresent(self):
        order = {'apple': 1, 'orange': 2}
        inventory_distribution = [{'name': 'owd', 'inventory': {'Banana': 1}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [])
    
    # Test on surplus inventory
    def test_surplusInventory(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 10}}]
        shipment = InventoryAllocation.find_shipment(order, inventory_distribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])


class AllocationErrorTesting(unittest.TestCase):
    # Error Testing
    
    # Type Errors
    
    # Test 1: Amount of an order is not a number
    def test_OrderAmountIsString_TypeError(self):
        order = {'apple': '1'}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        with self.assertRaises(TypeError):
            InventoryAllocation.find_shipment(order, inventory_distribution)

    # Test 2: Amount of inventory in a warehouse is not a number
    def test_InventoryAmountIsString_TypeError(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': '1'}}]
        with self.assertRaises(TypeError):
            InventoryAllocation.find_shipment(order, inventory_distribution)

    # Test 3: Name of an order is not a string
    def test_OrderNameIsNonString_TypeError(self):
        order = {1: 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        with self.assertRaises(TypeError):
            InventoryAllocation.find_shipment(order, inventory_distribution)
    
    # Test 4: Name of a company is not a string
    def test_NameInDistributionIsNonString_TypeError(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 1, 'inventory': {'apple': 1}}]
        
        
            
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

input()
