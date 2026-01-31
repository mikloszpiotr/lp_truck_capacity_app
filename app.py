import streamlit as st
from pyomo.environ import (
    ConcreteModel, Var, Constraint, Objective,
    NonNegativeReals, minimize, SolverFactory, value
)

# ============================
# Pyomo LP model (cost-based)
# ============================
def solve_lp(demand, capacity, ship_cost, penalty_cost):
    m = ConcreteModel()

    # Decision variables
    m.shipped = Var(domain=NonNegativeReals)
    m.unmet = Var(domain=NonNegativeReals)

    # Constraints
    m.capacity_con = Constraint(expr=m.shipped <= capacity)
    m.demand_con = Constraint(expr=m.shipped + m.unmet == demand)

    # Objective: minimize total cost
    m.obj = Objective(
        expr=ship_cost * m.shipped + penalty_cost * m.unmet,
        sense=minimize
    )

    # Solve
    solver = SolverFactory("highs")
    if not solver.available():
        raise RuntimeError(
            "HiGHS solver not available. Install with: pip install highspy"
        )

    solver.solve(m)

    shipped = value(m.shipped)
    unmet = value(m.unmet)
    total_cost = value(m.obj)
    service_level = shipped / demand if demand > 0 else 0

    return shipped, unmet, total_cost, service_level


# ============================
# Streamlit App
# ============================
st.set_page_config(page_title="LP Truck Capacity – Cost Model", layout="centered")

st.title("🚚 LP Truck Capacity — Cost Minimization")
st.write(
    """
    Simple **Linear Programming** example using **Pyomo**.

    You decide:
    - Demand
    - Truck capacity
    - Shipping cost
    - Penalty cost for unmet demand

    The model **minimizes total cost**.
    """
)

with st.sidebar:
    st.header("Inputs")

    demand = st.number_input("Demand (apples)", min_value=0.0, value=100.0, step=1.0)
    capacity = st.number_input("Truck capacity (apples)", min_value=0.0, value=80.0, step=1.0)

    st.divider()

    ship_cost = st.number_input("Shipping cost per apple", min_value=0.0, value=1.0, step=0.1)
    penalty_cost = st.number_input("Penalty cost per unmet apple", min_value=0.0, value=10.0, step=0.5)

    solve = st.button("Solve LP")

if solve or True:
    try:
        shipped, unmet, total_cost, service_level = solve_lp(
            demand, capacity, ship_cost, penalty_cost
        )

        st.subheader("Results")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("✅ Shipped", f"{shipped:.0f}")
        c2.metric("❌ Unmet", f"{unmet:.0f}")
        c3.metric("⚠️ Service Level", f"{service_level*100:.1f}%")
        c4.metric("💰 Total Cost", f"{total_cost:.2f}")

        st.markdown("---")
        st.subheader("Planner Interpretation")

        if unmet > 0:
            st.warning(
                f"Capacity is limiting. You can ship only **{shipped:.0f}** "
                f"out of **{demand:.0f}**. "
                f"Unmet demand = **{unmet:.0f}**."
            )
        else:
            st.success("All demand is fulfilled within capacity.")

        st.markdown("---")
        st.subheader("LP Model (what Pyomo solved)")

        st.markdown(
            f"""
**Decision variables**
- shipped ≥ 0  
- unmet ≥ 0  

**Constraints**
- shipped ≤ {capacity} (truck capacity)  
- shipped + unmet = {demand} (demand balance)  

**Objective**
- Minimize:  
  `{ship_cost} × shipped + {penalty_cost} × unmet`
            """
        )

        st.caption(
            "Note: In this formulation, shipped = min(demand, capacity). "
            "Costs affect total cost, not shipped quantity. "
            "Next step would be adding expediting or backup supply."
        )

    except Exception as e:
        st.error(str(e))
