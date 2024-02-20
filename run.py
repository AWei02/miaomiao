import json
import requests
import streamlit as st
import numpy as np
import pandas as pd


def work(latitude, longitude, date1, date2, keywords):
    # latitude纬度, longitude经度
    # 温度（T2M）、露点温度（T2MDEW）、湿度（T2MWET）、地表温度（TS）
    base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={keywords}&community=RE&longitude={longitude}&latitude={latitude}&start={date1}&end={date2}&format=JSON"
    api_request_url = base_url.format(longitude=longitude,
                                      latitude=latitude,
                                      keywords=keywords,
                                      date1=date1,
                                      date2=date2)
    response = requests.get(url=api_request_url, verify=True, timeout=30.00)
    content = json.loads(response.content.decode('utf-8'))
    df = pd.DataFrame(content["properties"]['parameter'])

    return df


st.set_page_config(
    page_title="NASA数据获取",
    page_icon="	:milky_way:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.header('NASA数据获取')
tab1, tab2 = st.tabs(["输入", "输出"])

with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(":globe_with_meridians:坐标")
        number1 = st.number_input("纬度", format="%s", value=24.3406606)
        number2 = st.number_input("经度", format="%s", value=124.1555804)

    with col2:
        st.write(":date:日期")
        string1 = st.text_input("开始日期", value='20220101')
        string2 = st.text_input("截止日期", value='20221231')

    with col3:
        st.write(":pushpin:关注点")
        T2M = st.checkbox("T2M")
        T2M_MAX = st.checkbox("T2M_MAX")
        T2M_MIN = st.checkbox("T2M_MIN")
        T2M_RANGE = st.checkbox("T2M_RANGE")
        T2MDEW = st.checkbox("T2MDEW")
        T2MWET = st.checkbox("T2MWET")
        TS = st.checkbox("TS")
        ALLSKY_SFC_SW_DWN = st.checkbox("ALLSKY_SFC_SW_DWN")
        ALLSKY_SFC_SW_DNI = st.checkbox("ALLSKY_SFC_SW_DNI")
        WS2M = st.checkbox("WS2M")
        PRECTOTCORR = st.checkbox("PRECTOTCORR")

        # 获取选中的复选框的值
        selected_checkboxes = [T2M, T2M_MAX, T2M_MIN, T2M_RANGE, T2MDEW,
                               T2MWET, TS, ALLSKY_SFC_SW_DWN, ALLSKY_SFC_SW_DNI, WS2M, PRECTOTCORR]
        selected_checkboxes_names = ['T2M', 'T2M_MAX', 'T2M_MIN', 'T2M_RANGE', 'T2MDEW',
                                     'T2MWET', 'TS', 'ALLSKY_SFC_SW_DWN', 'ALLSKY_SFC_SW_DNI', 'WS2M', 'PRECTOTCORR']
        # 打印选中的复选框的项目
        selected_items = [f"{selected_checkboxes_names[i]}" for i, checkbox in enumerate(selected_checkboxes) if
                          checkbox]

    if st.button('查找', type="primary"):
        # 判断输入框是否全部填写
        if not number1 or not number2 or not string1 or not string2 or not selected_items:
            st.warning("有数据空缺，请补充完整再查询")
            with tab2:
                st.write("有数据空缺，请补充完整再查询")
        else:
            st.success("输入完整，去看看查询结果吧!")
            with tab2:
                st.write("纬度:", number1, "经度:", number2)
                st.write("日期：", string1, "-", string2)
                key = ",".join(selected_items)
                st.write("关注点：", key)

                # df = work(number1, number2, string1, string2, key)
                df = pd.DataFrame(np.random.randn(8, 8))

                csv = df.to_csv().encode('utf-8')
                st.download_button(
                    label="导出",
                    data=csv,
                    file_name='output.csv',
                    mime='text/csv',
                )

                st.table(df.head(10))
    else:
        with tab2:
            st.write("请先点击查找")
