import streamlit as st
from openai import OpenAI

# Initialize OpenAI client with API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit app setup
st.title("FA Controls - Sales Advisor GPT")

# Initialize session state for model and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"  # Ensure correct model name
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": (
                "You are a professional sales director for FA Controls. Your role is to provide ideas, new strategies, "
                "and helpful information about creative ways to generate new sales leads for FA Controls' products. "
                "Follow these instructions carefully... "
                "You need to advise us what information you need us to enter into your product knowledge to improve your ability "
                "and knowledge to give the above-mentioned advice."
            ),
        }
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        st.markdown(f"**{message['role'].capitalize()}:** {message['content']}")

# Function to check if a prompt is about a specific product and provide a detailed response
def get_product_response(prompt):
    product_knowledge = {
        "collaborative robots": """To generate new sales leads for collaborative robots (cobots), consider implementing the following strategies:
        - **Targeted Marketing Campaigns:** Focus on industries such as manufacturing, logistics, food processing, and healthcare.
        - **Content Marketing:** Create case studies, whitepapers, and blog posts showcasing the benefits of cobots.
        - **Webinars and Workshops:** Host webinars to demonstrate the value of cobots in different industries.
        - **Partnerships and Collaborations:** Work with system integrators and automation consultants to expand reach.
        - **Trade Shows and Industry Events:** Attend relevant events to showcase cobots and engage potential clients.
        - **Lead Generation through Demos:** Offer free demonstrations to attract leads.
        - **Referral Programs:** Use existing customer referrals to gain new business.
        - **Social Media Marketing:** Leverage platforms like LinkedIn and Instagram to engage prospects.
        - **SEO and PPC Campaigns:** Use search engine optimization and paid ads to drive traffic to your offerings.
        - **Educational Content:** Create how-to videos and FAQs to educate potential clients about cobots."""
        "semiconductor equipments" """To generate new sales leads for semiconductor equipment, consider strategies such as:
        - **Industry-Specific Marketing:** Target industries requiring advanced semiconductor technology like electronics, automotive, and telecommunications.
        - **Trade Shows and Industry Conferences:** Attend events like SEMICON to network with key players in the semiconductor industry.
        - **Content Marketing:** Create educational materials, case studies, and whitepapers to inform prospects about your semiconductor solutions.
        - **Partnerships:** Collaborate with other tech companies or system integrators to expand your reach.
        - **Webinars and Demos:** Host webinars and virtual demos to educate potential customers on the advantages of your semiconductor products.
        - **SEO and Paid Campaigns:** Optimize your website for semiconductor-related keywords and run PPC campaigns targeting potential customers.
        - **Customer Case Studies:** Share success stories from current customers to build credibility and trust.
        - **Referral Programs:** Offer discounts or incentives for customers who refer new leads to your semiconductor solutions.
        - **Direct Outreach:** Use targeted email and phone outreach to connect with decision-makers in relevant industries."""
    }
    
    for product, description in product_knowledge.items():
        if product.lower() in prompt.lower():
            return description
    return None

# Handle user input
if prompt := st.text_input("What can I help you with?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"**You:** {prompt}")

    # Check if prompt relates to a specific product
    product_response = get_product_response(prompt)
    if product_response:
        response = product_response
    else:
        # Use OpenAI API if no specific product match found
        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=st.session_state["messages"],
                )
                response = completion.choices[0].message.content  # Access `content` attribute
            except Exception as e:
                st.error(f"An error occurred: {e}")
                response = "I'm sorry, but I couldn't process your request."

    # Save assistant's response and display it
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f"**Assistant:** {response}")
