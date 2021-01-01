#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 05:19:32 2021

@author: silasjimmy
"""

# Part C: Finding the right amount to save away

num_of_months = 36
semi_annual_raise = .07
r = 0.04
portion_down_payment = 0.25
total_cost = 1000000
down_payment = total_cost * portion_down_payment

starting_salary = int(input("Enter the starting salary: "))

high = 10000
low = 0
guess = (high + low) / 2
num_of_searches = 0
current_savings = 0

while abs(down_payment - current_savings) >= 100:
    current_savings = 0
    portion_saved = guess / 100
    annual_salary = starting_salary
    
    for i in range(num_of_months):
        monthly_salary = annual_salary / 12
        monthly_savings = monthly_salary * portion_saved
        investment_returns = current_savings * (r / 12)
        current_savings += monthly_savings + investment_returns
        if num_of_months % 6 == 0:
            annual_salary *= (1 + semi_annual_raise)
    
    if current_savings > down_payment:
        high = guess
    else:
        low = guess
        
    guess = (high + low) / 2
    
    num_of_searches += 1

if portion_saved > 1:
    print("It is not possible to pay the down payment in three years.")
else:
    print("Best savings rate:", portion_saved)
    print("Steps in bisection search:", num_of_searches)