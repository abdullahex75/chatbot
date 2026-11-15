# ==============================================================================
# JAZZCASH PAYMENT SECTION
# ==============================================================================

def render_payment_section():

    st.markdown("---")
    st.markdown("## 💳 JazzCash Payment")

    st.info(
        "Choose your plan and contact the administrator "
        "for manual payment verification."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Weekly Plan")
        st.subheader("PKR 200")
        st.caption("7 Days Access")

    with col2:
        st.markdown("### Monthly Plan")
        st.subheader("PKR 500")
        st.caption("30 Days Access")

    st.divider()

    st.markdown("### 📱 Payment Details")

    # Replace these placeholders only with guardian-approved details.
    payment_number = "YOUR_APPROVED_JAZZCASH_NUMBER"
    account_name = "YOUR_ACCOUNT_NAME"

    st.write("**JazzCash Number:**", payment_number)
    st.write("**Account Name:**", account_name)

    st.warning(
        "Payment ke baad administrator se contact karein. "
        "Premium access sirf payment verify hone ke baad activate hoga."
    )

    st.caption(
        "Automatic payment gateway abhi connected nahi hai. "
        "Is app mein payment automatically process nahi hoti."
    )
