import streamlit as st

st.title("Venit necesar per angajat — ghid estimativ")

# Define presets
presets = {
    "Cafenea mică (ospătar/barista)": {
        "salary": 3000.0,
        "tax_rate": 35,
        "overhead": 500.0,
        "margin": 15
    },
    "Freelancer / Consultant solo": {
        "salary": 7000.0,
        "tax_rate": 0,
        "overhead": 1500.0,
        "margin": 30
    },
    "Agenție creativă": {
        "salary": 5000.0,
        "tax_rate": 40,
        "overhead": 1000.0,
        "margin": 20
    },
    "Startup tech (developer)": {
        "salary": 8000.0,
        "tax_rate": 45,
        "overhead": 1500.0,
        "margin": 20
    },
    "Personalizat": {
        "salary": 5000.0,
        "tax_rate": 40,
        "overhead": 1000.0,
        "margin": 20
    }
}

business_type = st.selectbox("Alege tipul de angajat / afacere:", list(presets.keys()))
preset = presets[business_type]

# Input handling
if business_type == "Personalizat":
    salary = st.number_input(
        "Salariu brut lunar (RON)",
        min_value=0.0,
        value=preset["salary"],
        help="Salariul brut lunar al angajatului, fără deduceri. Se folosește pentru a calcula costul total pentru angajator."
    )
    tax_rate = st.slider(
        "Taxe angajator (%)",
        min_value=0, max_value=100,
        value=preset["tax_rate"],
        help="Procentul de contribuții sociale și impozite plătite de angajator pentru fiecare angajat."
    )
    overhead = st.number_input(
        "Costuri indirecte per angajat (RON)",
        min_value=0.0,
        value=preset["overhead"],
        help="Cheltuieli asociate cu un angajat, altele decât salariul și taxele: chirie, echipamente, training etc."
    )
    margin = st.slider(
        "Marjă de profit țintă (%)",
        min_value=0, max_value=100,
        value=preset["margin"],
        help="Profitul pe care dorești să îl obții peste costurile totale. Afectează venitul minim necesar."
    )
else:
    salary = preset["salary"]
    tax_rate = preset["tax_rate"]
    overhead = preset["overhead"]
    margin = preset["margin"]

    st.markdown(f"""
    **Valori prestabilite pentru {business_type}:**
    - Salariu brut: {salary} RON
    - Taxe angajator: {tax_rate}%
    - Costuri indirecte: {overhead} RON
    - Marjă profit: {margin}%
    """)

# Calculate net salary (approximation)
net_salary = salary * 0.55
st.info(f"💡 *Salariu net estimat:* **{net_salary:.2f} RON** *(estimare simplificată pentru contract full-time, fără deduceri speciale)*")

# Result
if margin < 100:
    total_cost = salary * (1 + tax_rate / 100) + overhead
    required_revenue = total_cost / (1 - margin / 100)
    st.success(f"👉 Venit necesar per angajat: **{required_revenue:.2f} RON/lună**")
else:
    st.warning("Marja de profit nu poate fi 100% sau mai mult.")

# Surse și estimări
with st.expander("📎 Surse și estimări pentru valorile implicite"):
    st.markdown("""
    - **Salarii medii**: bazate pe datele publicate de Institutul Național de Statistică (INS):
        - [Câștigul salarial mediu brut în ianuarie 2025: 8.910 lei](https://insse.ro/cms/sites/default/files/com_presa/com_pdf/cs01r25.pdf)
        - [Câștigul salarial mediu brut în decembrie 2024: 9.251 lei](https://insse.ro/cms/sites/default/files/com_presa/com_pdf/cs12r24.pdf)
    - **Taxe angajator**: conform Codului Fiscal actualizat prin Ordonanța de Urgență nr. 11/2025:
        - [Legea nr. 227/2015 privind Codul Fiscal, actualizată](https://static.anaf.ro/static/10/Anaf/legislatie/Cod_fiscal_norme_2023.htm)
    - **Costuri indirecte**: estimări proprii pentru cheltuieli precum echipamente, chirie, software, training, contabilitate etc.
    - **Marjă de profit**: între 10% și 30%, în funcție de industrie, conform analizei firmelor active din România:
        - [Analiza indicatorilor economico-financiari ai unei firme](https://termene.ro/articole/indicatori-financiari)
    ---
    *Ultima actualizare: aprilie 2025*
    """)


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

