#Act as Financial Advisor and Wealth Manager. Your client is interested in GOOG. 
#Please elaborate more on the history of company, latest growth of financial report, and give conclusion and recommendation.

import streamlit as st
import call_vertex_api as vapi
import time

st.set_page_config(page_icon="image/usd.ico")

vNoLabel = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(vNoLabel, unsafe_allow_html=True)

st.title("Discover the financial detail and latest information of a Company or Stock to invest")

def show_progress_bar():
    progress_bar = st.progress(0)  # Create a progress bar widget
    # Iterate through each iteration
    for iteration in range(10):  # Change the total_iterations as per your requirement
        progress = iteration / 10  # Update the progress value
        progress_bar.progress(progress)  # Update the progress bar widget
        time.sleep(0.5)  # Simulating some work being done
    progress_bar.empty()  # Clear the progress bar when done

def show_progress():
    with st.spinner('Please wait for my answer... it might take longer...'):
        time.sleep(5)

def article_outline(topic):
    # Prompt    
    prompt = f"Act as Financial Consultant and Wealth Advisor, please create a detail explanation article about a {vOpt} for {vText}. "
    prompt += "You are truthful and never lie. never make up facts if you are not 100 percent sure, reply with what you can not answer in a truthful way."
    prompt += "Please make it factual and remember to update the information regularly as news and events unfold to keep your audience informed with the most up-to-date information.  "
    prompt += """
                It's essential to consider both the fundamental aspects of the company and any recent news or updates. Here's a structured approach you can follow:

                Introduction:
                Start by providing a brief overview of the company and its stock symbol.

                Company Background:
                Explain key details about the company, such as its industry, products/services, and market presence. Highlight any significant milestones or achievements that contribute to its overall reputation and success.

                Financial Performance:
                Discuss the company's financial performance, including revenue, profit, and growth trends. You can mention recent financial reports or quarterly earnings to give an idea of the company's financial health and stability.

                Competitive Landscape:
                Analyze the company's position within its industry and discuss its main competitors. Assess how Alphabet Inc. stands out from its competitors and what advantages or challenges it faces in the market.

                Recent News and Updates:
                Provide the latest news or updates related to the company. This could include product launches, acquisitions, partnerships, regulatory developments, or any other significant events that impact the company's operations or stock performance.

                Stock Performance:
                Show the stock ticker code, then discuss the historical stock performance of the company, including key metrics such as the stock price, market capitalization, and trading volume. Explain any notable trends, fluctuations, or recent developments that have influenced the stock's performance.
                Provide historical price charts and graphs, showing how the stock has performed over different time periods (e.g., day, week, month, year). Highlight significant events or milestones that affected the stock price.

                Expensive or Cheap:
                Based on Price Earning Ratio of the stock, is it considered cheap or expensive? If so, explain the reasons.

                Analyst Opinions:
                Summarize the viewpoints of financial analysts or experts regarding the company's stock. Highlight any upgrades, downgrades, or target price revisions provided by reputable analysts. Mention consensus estimates and the overall sentiment in the investment community.

                Risks and Challenges:
                Identify potential risks and challenges that company may face. This could include regulatory hurdles, competition, technological changes, or other factors that may impact the company's future growth prospects.

                Conclusion:
                Summarize the key points discussed and provide an overall assessment of the company's stock. Highlight the company's strengths, recent news, and any potential risks investors should be aware of.

                Call to Action:
                Inform the latest price of the stock per-latest date (inform the actual date of that price) and Make a recommendation whether to buy or not to buy the stock right now.
                
             """

    # Show Progress Bar
    show_progress_bar()
    show_progress()
    # Run LLM model
    response = vapi.generate_text_from_genai_googlevertexapi(prompt)
    # Print results
    return st.info(response)

with st.form("myform1"):
    col1, col2 = st.columns(2)
    with col1:
        vOpt_options = ['Company Name', 'Stock Exchange Code/Symbol']
        vOpt = st.selectbox('Choose the type of information you want to extract:', vOpt_options)
    with col2:
        vText = st.text_input('Enter the name of the company or the company symbol:')
    submitted = st.form_submit_button("Submit", type="primary")
    if not vText:
        st.info("Please enter your company name or stock symbol.")
    elif submitted:
        article_outline(vText)
        # Show me more information (next improvement)