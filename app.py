
import streamlit as st
import httpx

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PayPilot AI",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ PayPilot AI")
st.subheader("Your AI-powered commerce and payment copilot")

st.write(
    "Describe what you need. PayPilot AI will help you "
    "clarify your shopping requirements."
)

if st.button("Check Backend Connection"):
    try:
        response = httpx.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        st.success("Backend connection successful!")
    except httpx.HTTPError:
        st.error("Backend unavailable. Check the first terminal.")

st.divider()
st.header("AI Shopping Assistant")

prompt = st.text_area(
    "What are you looking for?",
    placeholder="Example: Recommend headphones for online classes under $100.",
)

if st.button("Ask PayPilot AI", type="primary"):
    if not prompt.strip():
        st.warning("Please describe what you need.")
    else:
        try:
            with st.spinner("PayPilot AI is thinking..."):
                response = httpx.post(
                    f"{API_URL}/ai/assist",
                    json={"prompt": prompt},
                    timeout=70,
                )
                response.raise_for_status()
                result = response.json()

            st.markdown("### AI Response")
            st.write(result["answer"])
            st.caption(f"Model used: {result['model']}")

        except httpx.HTTPStatusError as exc:
            st.error(
                f"Request failed ({exc.response.status_code}): "
                f"{exc.response.text[:500]}"
            )
        except httpx.RequestError as exc:
            st.error(f"Could not reach the backend: {exc}")
