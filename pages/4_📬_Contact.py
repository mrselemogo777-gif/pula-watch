import streamlit as st

st.set_page_config(
    page_title="Contact · Pula Watch",
    page_icon="📬",
    layout="wide",
)

st.title("📬 Contact")
st.caption("Questions, collaboration, or feedback on Pula Watch.")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("Author")
    st.markdown("""
**Legakwa Selemogo**

Independent ML researcher · Botswana

-  GitHub: [@mrselemogo777-gif](https://github.com/mrselemogo777-gif)
- 📦 Project repo: [pula-watch](https://github.com/mrselemogo777-gif/pula-watch)
- 📧 Email: mrselemogo777@gmail.com
""")

with col2:
    st.header("Quick links")
    st.markdown("""
- [Open an issue](https://github.com/mrselemogo777-gif/pula-watch/issues)
- [View source](https://github.com/mrselemogo777-gif/pula-watch)
- [Model & Data](1_📊_Model_and_Data.py)
- [About](2_ℹ️_About.py)
""")

st.markdown("---")

st.header("Get in touch")

with st.form("contact_form", clear_on_submit=True):
    name = st.text_input("Your name", placeholder="Jane Doe")
    email = st.text_input("Your email", placeholder="jane@example.org")
    org = st.text_input("Organisation (optional)", placeholder="University / NGO / Government")
    topic = st.selectbox(
        "Topic",
        [
            "General question",
            "Data / methodology",
            "Collaboration proposal",
            "Bug report",
            "Feature request",
            "Media / press",
        ],
    )
    message = st.text_area(
        "Message",
        placeholder="Briefly describe your question or proposal...",
        height=150,
    )

    submitted = st.form_submit_button("📨 Send message")

    if submitted:
        if not name or not email or not message:
            st.error("Please fill in name, email, and message.")
        else:
            st.success(
                f"Thanks, **{name}**. Your message about *{topic}* has been noted. "
                "For the fastest response, please also open an issue on the GitHub repo."
            )
            st.info(
                "Note: this demo form does not send email. To enable delivery, "
                "connect it to a backend (e.g., Formspree, Resend) in the source."
            )

st.markdown("---")

st.header("Collaboration")

st.markdown("""
I'm open to:

- **Research collaborations** on drought monitoring, climate ML, or spatial analysis in southern Africa.
- **Data partnerships** with meteorological services, NGOs, or agricultural extension programmes.
- **Methodology feedback** — especially from climate scientists and ML practitioners.
- **Field deployments** where the tool could be tested with extension officers.

If you work in any of these areas, please reach out via GitHub or the form above.
""")

st.markdown("---")
st.caption("Pula Watch · MIT License · 2026")
