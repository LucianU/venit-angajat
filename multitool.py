import streamlit as st

def show_runway_calculator():
    st.header("🔁 Runway Calculator")
    cash = st.number_input("Cash disponibil (RON)", min_value=0.0, value=20000.0)
    burn = st.number_input("Cheltuieli lunare (RON)", min_value=0.0, value=5500.0)
    if burn > 0:
        runway = cash / burn
        st.success(f"🏁 Runway estimat: **{runway:.2f} luni**")
    else:
        st.info("💡 Runway nelimitat (cheltuieli lunare = 0)")

def show_survival_threshold():
    st.header("🛟 Prag de supraviețuire")
    expenses = st.number_input("Cheltuieli lunare fixe (RON)", min_value=0.0, value=8000.0)
    margin = st.slider("Marjă de siguranță (%)", min_value=0, max_value=100, value=10)
    threshold = expenses * (1 + margin / 100)
    st.success(f"🧾 Venit minim recomandat: **{threshold:.2f} RON/lună**")

def show_employee_break_even():
    st.header("👥 Venit necesar per angajat")

    salary = st.number_input("Salariu brut lunar (RON)", value=5000.0)
    tax_rate = st.slider("Taxe angajator (%)", 0, 100, 40)
    overhead = st.number_input("Costuri indirecte/lună (RON)", value=1000.0)
    margin = st.slider("Marjă profit (%)", 0, 100, 20)

    net_salary = calculate_net_salary(salary)

    st.info(f"💡 Salariu net estimat: **{net_salary:.2f} RON**")

    if margin < 100:
        total_cost = salary * (1 + tax_rate / 100) + overhead
        required_revenue = total_cost / (1 - margin / 100)
        st.success(f"👉 Venit necesar per angajat: **{required_revenue:.2f} RON/lună**")
    else:
        st.warning("⚠️ Marja de profit nu poate fi 100% sau mai mult.")

st.sidebar.title("🧰 Alege unealta")
tool = st.sidebar.radio("Ce vrei să calculezi?", [
    "Runway (autonomie financiară)",
    "Prag de supraviețuire",
    "Venit necesar per angajat"
])

if tool == "Runway (autonomie financiară)":
    show_runway_calculator()
elif tool == "Prag de supraviețuire":
    show_survival_threshold()
elif tool == "Venit necesar per angajat":
    show_employee_break_even()


def calculate_net_salary(brut_salary: float) -> float:
    """
    Approximate net salary in Romania (standard full-time contract),
    no tax exemptions, no deductions.
    """
    CAS = brut_salary * 0.25
    CASS = brut_salary * 0.10
    taxable_income = brut_salary - CAS - CASS
    income_tax = taxable_income * 0.10
    net_salary = brut_salary - CAS - CASS - income_tax
    return net_salary

