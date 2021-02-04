import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from functools import reduce

COMPANY_URL = "http://127.0.0.1:5000/companies/company_overview/search"
SUB_INDUSTRY_URL = "http://127.0.0.1:5000/sub_industries/search"
SECTOR_URL = "http://127.0.0.1:5000/sectors/sector/search"

def sub_industry_avg_performance_history(sub_industry_name):
    """
    returns a sub_industry's average performance numbers in each quarter, over the most recent 4 quarters
    in which SEC filings contaiing these numbers have been made by the companies in the sub_industry.  

    The result contains revenue, cost, net_earnings, stock price, price/earnings ratio, which 
    can be selected by the web client/end user.
    """
    response = requests.get(SUB_INDUSTRY_URL, params= {'sub_industry': sub_industry_name})
    return response.json()

def avg_performance_by_sub_industries(sub_industries):
    avg_performances = dict()
    for sub_industry_name in sub_industries:
        sub_industry_avg_performance_hist = sub_industry_avg_performance_history(sub_industry_name)
        sub_industry_name = sub_industry_avg_performance_hist[0]['sub_industry_name']
        avg_performances[sub_industry_name] = sub_industry_avg_performance_hist
    return avg_performances

def sub_industry_single_measure_avg_performance(sub_industry_name:str, 
                                                performance_measurement:str,
                                                avg_performance_by_sub_industries):
    """
    Ruturns a sub_industry's a single performance measure's historical values over 4 quarters,
    in the right format for a steamlit trace.  
    """
    quarterly_results = [quarter[performance_measurement] for quarter 
                                            in avg_performance_by_sub_industries[
                                                                                sub_industry_name]]
    quarterly_report_dates = [quarter['date'] for quarter 
                                            in avg_performance_by_sub_industries[
                                                                                sub_industry_name]]
    return quarterly_results, quarterly_report_dates


def plot_sub_industries_avg_performance_history(sub_industries:list, performance_measurement):
    sub_industries_avg_performance = avg_performance_by_sub_industries(sub_industries)
    fig = go.Figure()
    for sub_industry in sub_industries:
        quarterly_results, quarterly_report_dates = sub_industry_single_measure_avg_performance(
                                                                            sub_industry, 
                                                                            performance_measurement,
                                                                            sub_industries_avg_performance)
          
        fig.add_trace(go.Scatter(x= quarterly_report_dates,
                                y= quarterly_results,
                                name = f"{sub_industry}"))

    fig.update_layout(
        title=f"""Quarterly {performance_measurement} by sub-industry""",
        xaxis_title="Month-Year",
        yaxis_title= f"{performance_measurement}",
        legend_title= "Sub-industries:",
        legend=dict(
                x=0,
                y=1,
                traceorder='normal',
                font=dict(
                    size=12,),
                    ),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    st.plotly_chart(fig)

def find_companies_by_sub_industry(sub_industry_name):
    response = requests.get(SUB_INDUSTRY_URL, params={'sub_industry': sub_industry_name})
    return response.json()

def find_company_by_ticker(ticker):
    '''returns the company ticker from the web interface'''
    response = requests.get(COMPANY_URL, params = {'ticker': ticker})
    return response.json()

def find_companies_by_sector(sector):
    selected_sector = requests.get(SECTOR_URL, params = {'sector': sector})
    return selected_sector.json()

def avg_element_wise_list(list_of_tuples: list):
    """
    Turns a list of tuples into a list of element-wise average numbers.
    """
    sum_element_wise_list = (reduce(lambda x, y: [tup[0] + tup[1] for tup in zip(x,y)], list_of_tuples) 
                                if type(list_of_tuples[0]) == tuple 
                                else list_of_tuples)
    if type(list_of_tuples[0]) == tuple:
        number_companies = len(list_of_tuples)
        return list(map(lambda sum_element_wise: sum_element_wise/ number_companies,
                            sum_element_wise_list))
    else:
        return list_of_tuples

#####
# Various plots
#####

sub_industries_selected = st.multiselect('Sub_industries:',
                        ['Hypermarkets & Super Centers', 'Pharmaceuticals', 'Technology Hardware, Storage & Peripherals'],
                        ['Hypermarkets & Super Centers', 'Pharmaceuticals', 'Technology Hardware, Storage & Peripherals'])

# show one performance measurement, 'avg_pe_ratio', for demo purpose, to be followed by a menu choice of # all the performance measurments

# plot_sub_industries_avg_performance_history(sub_industries_selected, 'avg_closing_price')


performance_measurement_selected = st.multiselect('Performance measurements:',
                            ['avg_pe_ratio', 'avg_closing_price', 'avg_revenue', 'avg_cost', 'avg_net_income'],
                            ['avg_pe_ratio'])[0]

plot_sub_industries_avg_performance_history(sub_industries_selected, 
                                            performance_measurement_selected)
breakpoint()

# earlier scripts - need reviewing and pruning. 

# plot each sector's average price/quarter-earnings ratio over 4 quarters
fig = go.Figure()
for sector in selected_sectors:
    companies_by_sector = find_companies_by_sector(sector)
    pe_list = []
    for company in companies_by_sector:
        ticker = company['ticker']
        company_info = find_company_by_ticker(ticker)
        pe_history = [quarter['price_earnings_ratio'] for quarter in company_info[
                                                'Quarterly Closing Price and P/E ratio']]
        date_history = [datetime.strptime(quarter['date'], "%Y-%m-%d") for quarter in company_info[
                                                'Quarterly Closing Price and P/E ratio']]
        pe_list.append(dict(zip(date_history, pe_history)))

    companies_pe_history_list = [company_quarterly_pe
                                        for company_pe_history_dict in pe_list 
                                                for company_quarterly_pe in company_pe_history_dict.values()]
    quarterly_average_pe_history = avg_element_wise_list(companies_pe_history_list)
    quarter_ending_dates_history = [key for key in pe_list[0].keys()] 
    

    # y, x axis, respectively, above
    # average quarterly p/e ratio trace for each sector    
    fig.add_trace(go.Scatter(x= quarter_ending_dates_history,
                            y= quarterly_average_pe_history,
                            name = f"{sector}"))

fig.update_layout(
    title=f"""Average Price/Earnings ratio by sector""",
    xaxis_title="Month-Year",
    yaxis_title="Average P/E ratio",
    legend_title="Average quarterly P/E ratio",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

st.plotly_chart(fig)

selected_sectors = st.multiselect(
                    'Which sector are you interested in? (Select only one, please.)',
                    ['Health Care', 'Information Technology', 'Consumer Staples'],
                    ['Health Care', 'Information Technology', 'Consumer Staples'])

selected_sector = selected_sectors[0]
st.write(f'You selected: {selected_sector}')

companies_by_sector = find_companies_by_sector(selected_sector)
st.text(f"Companies in the {selected_sector} sector:")
st.text("=" * 30)
for company in companies_by_sector:
    st.text(f"{company['name']}   Ticker: {company['ticker']}")
    st.text(f"Year founded: {company['year_founded']}")
    st.text(f"Number of employees: {company['number_of_employees']}")
    st.text('_' * 30)


fig = go.Figure()
for company in companies_by_sector:
    ticker = company['ticker']
    company_info = find_company_by_ticker(ticker)

    revenue_history = [report['revenue'] for report in company_info['History of quarterly financials']]
    date_history = [datetime.strptime(report['date'], "%Y-%m-%d") for report in company_info['History of quarterly financials']]
    
    # https://plotly.com/python/figure-labels/
    
    fig.add_trace(go.Scatter(x=date_history,
                            y=revenue_history,
                            name = f"{company_info['name']}"))

fig.update_layout(
    title=f"""Companies in {selected_sector}:""",
    xaxis_title="Month-Year",
    yaxis_title="Quarterly Revenue",
    legend_title="Companies",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

st.plotly_chart(fig)
# fig.show() -> plotly implementation, not streamlit

# Next-level choice menu

# develop a companies_by_sector method, pass in selected_sector, obtains a list of companies
# in a chosen sector, then pass it to the st.multiselect below:


# should be done in the backend, through the Flask app, not the frontend.  
companies_in_sector = [company['name'] for company in companies_by_sector]
company_response = st.multiselect(
                    f'Which company in the {selected_sector} sector are you interested in? (Select only one, please.)',
                    companies_in_sector,
                    companies_in_sector)
company_name = company_response[0]
st.write('You selected:', company_name)

def find_company_by_name(name):
    response = requests.get(COMPANY_URL, params = {'name': name})
    return response.json()

companies_by_sector = find_company_by_name(company_response)
ticker = companies_by_sector['ticker']

company_info = find_company_by_ticker(ticker)
st.text(f"Name: {company_info['name']}")
st.text(f"Ticker: {company_info['ticker']}")

revenue_history = [report['revenue'] for report in company_info['History of quarterly financials']]
date_history = [datetime.strptime(report['date'], "%Y-%m-%d") for report in company_info['History of quarterly financials']]
#fig = plt.plot(date_history, revenue_history)
#st.pyplot
#st.plotly_chart

fig = go.Figure(data=go.Scatter(x=date_history,
                             y=revenue_history))
st.plotly_chart(fig)
#plt.savefig(fig)



