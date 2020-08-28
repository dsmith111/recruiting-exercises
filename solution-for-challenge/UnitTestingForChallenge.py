#!/usr/bin/env python

import unittest
import random
from InventoryAllocationRC import inventoryAllocation


class AllocationTesting(unittest.TestCase):

    # Tests below on varying order size and inventory distribution

    # Test 1: One order, valid shipment, one providing warehouse,
    # one listed warehouse
    def test_OneOrder_ValidShipment_OneProviding_OneWarehouse(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])

    # Test 2: One order, valid shipment, one providing warehouse,
    # multiple listed warehouses
    def test_OneOrder_ValidShipment_OneProviding_MultipleWarehouses(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1}},
                                 {'name': 'dm', 'inventory': {'apple': 3}}
                                 ]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])

    # Test 3: One order, valid shipment, multiple providing warehouses,
    # multiple listed warehouses
    def test_OneOrder_ValidShipment_MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 10}
        inventoryDistribution = [
                                    {'name': 'dm', 'inventory': {'apple': 5}},
                                    {'name': 'owd', 'inventory': {'apple': 5}}
                                 ]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [
                                    {'dm': {'apple': 5}},
                                    {'owd': {'apple': 5}}
                                    ])

    # Test 4: One order, no valid shipments, one listed warehouse
    def OneOrder_InvalidShipment__OneProviding_OneWarehouse(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 0}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [])

    # Test 5: One order, no valid shipments, multiple listed warehouses
    def test_OneOrder_InvalidShipment__OneProviding_MultipleWarehouses(self):
        order = {'apple': 2}
        inventoryDistribution = [
                                    {'name': 'dm', 'inventory': {'apple': 0}},
                                    {'name': 'owd', 'inventory': {'apple': 1}}
                                 ]

        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [])

    # Test 6: Multiple orders, valid shipment, one providing warehouse,
    # one listed warehouse
    def test_MultipleOrders_ValidShipment_OneProviding_OneWarehouse(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1, 'orange': 2}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1, 'orange': 2}}])

    # Test 7: Multiple orders, valid shipment, one providing warehouses,
    # multiple listed warehouses
    def test_MultipleOrders_ValidShipment_OneProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [
                                    {'name': 'dm', 'inventory': {'apple': 1, 'orange': 2}},
                                    {'name': 'owd', 'inventory': {'banana': 3}}
                                 ]

        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [{'dm': {'apple': 1, 'orange': 2}}])

    # Test 8: Multiple orders, valid shipment, multiple providing warehouses,
    # multiple listed warehouses
    def test_MultipleOrders_ValidShipment_MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [
                                    {'name': 'dm', 'inventory': {'apple': 1, 'orange': 1}},
                                    {'name': 'owd', 'inventory': {'orange': 1}}
                                 ]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [
                                    {'dm': {'apple': 1, 'orange': 1}},
                                    {'owd': {'orange': 1}}
                                    ])

    # Test 9: Multiple orders, no valid shipments, one listed warehouse
    def test_MultipleOrders_InvalidShipment__OneProviding_OneWarehouse(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [])

    # Test 10: Multiple orders, no valid shipments, multiple listed warehouses
    def test_MultipleOrders_InvalidShipment__MultipleProviding_MultipleWarehouses(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [
                                    {'name': 'dm', 'inventory': {'apple': 0, 'orange': 1}},
                                    {'name': 'owd', 'inventory': {'orange': 1}}
                                 ]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [])
        
    # Test 11: Orders are not present in warehouses
    def test_OrderIsNotPresent(self):
        order = {'apple': 1, 'orange': 2}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'Banana': 1}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [])
    
    # Test on surplus inventory
    def test_surplusInventory(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 10}}]
        shipment = inventoryAllocation.findShipment(order, inventoryDistribution)
        self.assertEqual(shipment, [{'owd': {'apple': 1}}])


class AllocationErrorTesting(unittest.TestCase):
    # Error Testing
    
    # Type Errors
    
    # Test 1: Amount of an order is not a number
    def test_OrderAmountIsString_TypeError(self):
        order = {'apple': '1'}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        with self.assertRaises(TypeError):
            inventoryAllocation.findShipment(order, inventoryDistribution)

    # Test 2: Amount of inventory in a warehouse is not a number
    def test_InventoryAmountIsString_TypeError(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': '1'}}]
        with self.assertRaises(TypeError):
            inventoryAllocation.findShipment(order, inventoryDistribution)

    # Test 3: Name of an order is not a string
    def test_OrderNameIsNonString_TypeError(self):
        order = {1: 1}
        inventoryDistribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        with self.assertRaises(TypeError):
            inventoryAllocation.findShipment(order, inventoryDistribution)
    
    # Test 4: Name of a company is not a string
    def test_NameInDistributionIsNonString_TypeError(self):
        order = {'apple': 1}
        inventoryDistribution = [{'name': 1, 'inventory': {'apple': 1}}]
        
        
            
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

input()
