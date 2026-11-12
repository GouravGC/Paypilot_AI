
import streamlit as st
import httpx

API_URL = "https://paypilot-ai-latest.onrender.com"

st.set_page_config(
    page_title="PayPilot AI",
    page_icon="🛍️",
    layout="wide",
)

st.title("🛍️ PayPilot AI")
st.subheader("Your AI-powered commerce and payment copilot")

st.write("Discover products, compare real offers and get AI-powered shopping assistance.")

# Backend connection
if st.button("Check Backend Connection"):
    try:
        response = httpx.get(f"{API_URL}/health", timeout=30)
        response.raise_for_status()
        st.success("Backend connection successful!")
    except httpx.HTTPError as exc:
        st.error(f"Backend connection failed: {exc}")

st.divider()

# Live Channel3 product discovery
st.header("🔎 Live Product Discovery")
query = st.text_input(
    "Search products",
    placeholder="e.g. Adidas running shoes under $100",
)

if st.button("Search Products", type="primary"):
    if not query.strip():
        st.warning("Enter a product search.")
    else:
        try:
            with st.spinner("Searching live product listings..."):
                response = httpx.post(
                    f"{API_URL}/products/search",
                    json={"query": query, "limit": 5},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

            products = data.get("products", [])
            st.success(f"Found {len(products)} products")

            if not products:
                st.info("No products found. Try another search.")

            for product in products:
                with st.container(border=True):
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if product.get("image"):
                            st.image(product["image"], use_container_width=True)

                    with col2:
                        st.subheader(product.get("title", "Product"))
                        if product.get("brand"):
                            st.caption(f"Brand: {product['brand']}")

                        price = product.get("price")
                        currency = product.get("currency", "")
                        if price is not None:
                            st.markdown(f"### {currency} {price}")

                        st.write(product.get("description", "")[:350])

                        if product.get("rating") is not None:
                            st.write(
                                f"⭐ {product['rating']} "
                                f"({product.get('rating_count', 0)} ratings)"
                            )

                        st.caption(
                            f"Retailer: {product.get('retailer', 'Not specified')} "
                            f"· Availability: {product.get('availability', 'Unknown')}"
                        )

                        if product.get("features"):
                            st.write("Features: " + ", ".join(product["features"][:4]))

                        if product.get("buy_url"):
                            st.link_button("View / Buy Product", product["buy_url"])

        except httpx.HTTPStatusError as exc:
            st.error(
                f"Product search failed ({exc.response.status_code}): "
                f"{exc.response.text[:500]}"
            )
        except httpx.RequestError as exc:
            st.error(f"Could not reach backend: {exc}")

st.divider()

# Existing AI assistant
st.header("🤖 AI Shopping Assistant")

prompt = st.text_area(
    "What are you looking for?",
    placeholder="Recommend headphones for online classes under $100.",
)

if st.button("Ask PayPilot AI"):
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
            st.error(f"Could not reach backend: {exc}")
