
import streamlit as st

st.set_page_config(page_title="Venit per angajat", page_icon="💼", layout="centered")
st.title("💼 Venit necesar per angajat — ghid estimativ")

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
    }
}

# Initialize session state for edit mode
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

business_type = st.selectbox("Alege tipul de angajat / afacere:", list(presets.keys()))
preset = presets[business_type]

if st.button("🔧 Vreau să modific valorile pentru acest rol"):
    st.session_state.edit_mode = True

if st.session_state.edit_mode:
    st.subheader("✏️ Editare valori preset")
    salary = st.number_input("Salariu brut lunar (RON)", min_value=0.0, value=preset["salary"])
    tax_rate = st.slider("Taxe angajator (%)", min_value=0, max_value=100, value=preset["tax_rate"])
    overhead = st.number_input("Costuri indirecte/lună (RON)", min_value=0.0, value=preset["overhead"])
    margin = st.slider("Marjă profit (%)", min_value=0, max_value=100, value=preset["margin"])
else:
    salary = preset["salary"]
    tax_rate = preset["tax_rate"]
    overhead = preset["overhead"]
    margin = preset["margin"]

# Display preset values
st.markdown(f"### Valori prestabilite pentru {business_type}:")
st.markdown(f"- Salariu brut: {salary:.1f} RON")
st.markdown(f"- Taxe angajator: {tax_rate}%")
st.markdown(f"- Costuri indirecte: {overhead:.1f} RON")
st.markdown(f"- Marjă profit: {margin}%")

# Salariu net estimat
CAS = salary * 0.25
CASS = salary * 0.10
taxable = salary - CAS - CASS
tax = taxable * 0.10
net_salary = salary - CAS - CASS - tax

st.info(f"💡 **Salariu net estimat:** {net_salary:.2f} RON _(estimare simplificată pentru contract full-time, fără deduceri speciale)_")

# Calcul venit necesar
if margin < 100:
    total_cost = salary * (1 + tax_rate / 100) + overhead
    required_revenue = total_cost / (1 - margin / 100)
    st.success(f"✅ **Venit necesar per angajat: {required_revenue:.2f} RON/lună**")
else:
    st.warning("⚠️ Marja de profit nu poate fi 100% sau mai mult.")

# Surse
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

st.caption("© 2025 Lucian Ursu")
