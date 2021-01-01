#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 05:19:18 2021

@author: silasjimmy
"""

# Party B: Saving, with a raise

portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = int(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost = int(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-­annual raise, as a decimal:​ "))

down_payment = total_cost * portion_down_payment
num_of_months = 0

while current_savings < down_payment:
    monthly_salary = annual_salary / 12
    monthly_savings = monthly_salary * portion_saved
    investment_returns = current_savings * (r / 12)
    current_savings += monthly_savings + investment_returns
    num_of_months += 1
    if num_of_months % 6 == 0:
        annual_salary *= (1 + semi_annual_raise)

print()
print("Number of months:", num_of_months)