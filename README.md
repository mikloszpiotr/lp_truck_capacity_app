# 🚚 LP Truck Capacity App (Pyomo + Streamlit)

Interactive **Streamlit** application demonstrating a simple **Linear Programming (LP)** model built with **Pyomo** for a classic supply chain problem.

The app analyzes how **truck capacity limitations** impact:
- Shipped volume
- Unmet demand
- Service level
- Total cost (shipping + penalty)

---

## 🔍 Problem Description

A company needs to deliver apples to customers.

- **Demand**: total customer demand  
- **Capacity**: maximum apples the truck can carry  
- **Shipping cost**: cost per shipped apple  
- **Penalty cost**: cost per unmet apple  

When capacity is insufficient, part of the demand remains unmet.

---

## 🧮 Optimization Model

### Decision Variables
- `shipped` ≥ 0 — apples delivered
- `unmet` ≥ 0 — apples not delivered

### Constraints
- `shipped ≤ capacity`
- `shipped + unmet = demand`

### Objective
Minimize total cost:

