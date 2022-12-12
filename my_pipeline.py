from selenium import webdriver
import time
import os
import datetime
from collections import defaultdict
import pandas as pd
import networkx as nx
from pyvis.network import Network
pd.set_option('display.max_columns', 500)


def get_page_info(browser):
    url = 'https://firststop.sos.nd.gov/search/business'
    print(f"getting page info from {url}...")
    browser.get(url)  # visit the page
    browser.find_element_by_class_name('search-input').send_keys("X")  # search for 'X'
    browser.find_element_by_class_name('advanced-search-toggle').click()  # find div with class='advanced-search-toggle'
    browser.find_element_by_xpath("//*[text()='Starts with']").click()  # find div that has text='Starts with'
    browser.find_element_by_xpath("//*[text()='Active entities only']").click()  # find div that has text='Active ...'
    browser.find_element_by_class_name('center').click()  # find div that has class='center'
    form_info = browser.find_elements_by_class_name('interactive-cell-button')  # get the list of all business buttons
    df_res = []
    for info in form_info:
        storage = defaultdict()
        storage['datadate'] = today_date
        storage['biz_name'] = info.text.split("\n")[0]
        storage['Owner Name'] = ""
        storage['Registered Agent'] = ""
        storage['Commercial Registered Agent'] = ""
        time.sleep(1.5)
        browser.execute_script("arguments[0].click();", info)  # something blocked the element so that use script here.
        ls = browser.find_elements_by_class_name('detail ')  # get list of detailed information from side window
        for item in ls:
            label = item.find_element_by_class_name('label').text
            if 'Registered Agent' in label or 'Owner Name' in label:
                storage[label] = item.find_element_by_class_name('value').text
        temp_df = pd.DataFrame(data=storage, index=[0])
        df_res.append(temp_df)
    df_res = pd.concat(df_res, axis=0, ignore_index=True)
    df_res = df_res.astype({'biz_name': str, 'Owner Name': str,
                            'Registered Agent': str, 'Commercial Registered Agent': str})  # make sure the data types
    return df_res


def save_data(df, outdir=None):
    if outdir:
        godir = outdir
    else:
        godir = DEFAULT_DATA_HOME
    df.to_csv(godir, index=False)
    print(f'Data saved at {godir}')
    return True


def pop_graph(df):
    print("Forming graph...")
    my_gp = nx.Graph()
    for index, row in df.iterrows():
        my_gp.add_node(row['biz_name'], group=1)
        col1, col2, col3 = 'Owner Name', 'Registered Agent', 'Commercial Registered Agent'
        # we don't want to show nan in the graph, so we only keep non-NaN values
        if not pd.isnull(row[col1]):
            my_gp.add_node(row[col1], group=2)
            my_gp.add_edge(row['biz_name'], row[col1])
        if not pd.isnull(row[col2]):
            my_gp.add_node(row[col2], group=3)
            my_gp.add_edge(row['biz_name'], row[col2])
        if not pd.isnull(row[col3]):
            my_gp.add_node(row[col3], group=3)
            my_gp.add_edge(row['biz_name'], row[col3])
    return my_gp


def save_plot(graph):
    nt = Network('500px', '1000px')
    nt.from_nx(graph)
    file_name = os.path.join(BASE_PATH, 'plot', 'business_graph.html')
    nt.show(os.path.join('plot', 'business_graph.html'))
    print(f"graph shown in {os.path.abspath(file_name)}, copy the path and open in your browser")


if __name__ == '__main__':
    today_date = datetime.datetime.today().date()
    BASE_PATH = "./"
    DEFAULT_DATA_HOME = os.path.join(BASE_PATH, "data", f"nd_business_X_{today_date:%Y%m%d}.csv")
    CHROME_SIMULATOR = os.path.join(BASE_PATH, "chromedriver_mac_20221211")
    # # xattr -d com.apple.quarantine chromedriver_mac_20221211
    brows = webdriver.Chrome(CHROME_SIMULATOR)
    brows.implicitly_wait(10)  # makes sure browser is fully loaded
    df_info = get_page_info(brows)
    save_data(df_info)
    df_info = pd.read_csv(DEFAULT_DATA_HOME)  # can be commented
    G = pop_graph(df_info)
    save_plot(G)
