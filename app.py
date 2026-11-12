
import streamlit as st
import httpx

# Render-hosted FastAPI backend
API_URL = "https://paypilot-ai-latest.onrender.com"

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

# Backend health check
if st.button("Check Backend Connection"):
    try:
        response = httpx.get(
            f"{API_URL}/health",
            timeout=30,
        )
        response.raise_for_status()
        st.success("Backend connection successful!")
    except httpx.HTTPError as exc:
        st.error(f"Backend connection failed: {exc}")

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
        except (KeyError, ValueError) as exc:
            st.error(f"Unexpected backend response: {exc}")
