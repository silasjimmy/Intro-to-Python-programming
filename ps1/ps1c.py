#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 05:19:32 2021

@author: silasjimmy
"""

num_of_months = 36
semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
down_payment = total_cost * portion_down_payment

annual_salary = 100000 #int(input("Enter the starting salary: "))

high = 10000
low = 0
guess = (high + low) / 2
num_of_searches = 0

current_savings = 0

print("Down payment:", down_payment)

#while abs(current_savings - down_payment) >= 100:
#    # Set current savings to 0
#    current_savings = 0
#    # Calculate the portion saved in percentage
#    portion_saved = guess / 100
#    # Calculate the current savings
portion_saved = guess / 100
for i in range(num_of_months):
    monthly_salary = annual_salary / 12
    
    monthly_savings = monthly_salary * portion_saved
    investment_returns = current_savings * (r / 12)
    current_savings += monthly_savings + investment_returns
    if num_of_months % 6 == 0:
        annual_salary = annual_salary * (1 + semi_annual_raise)
print(current_savings)
#    # Calculate the low and high values
#    if current_savings > down_payment:
#        high = guess
#    else:
#        low = guess
#    # Set the guess value
#    guess = (high + low) / 2
##    print(low, high)
#    # Increment the number of searches
#    num_of_searches += 1
#    if num_of_searches == 10:
#        break

#print(portion_saved)
#print("Best savings rate:")
#print("Steps in bisection search:")