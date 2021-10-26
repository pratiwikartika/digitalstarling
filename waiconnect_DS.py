import math
import re
from collections import Counter

def cosinesimilarity(text1, text2):
    WORD = re.compile(r"\w+")
    def get_cosine(vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
        sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)
    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)
    cosine = get_cosine(vector1, vector2)
    return cosine
print(cosinesimilarity(text1 = "This is a foo bar sentence .",text2 = "This sentence is similar to a foo bar sentence ."))

import streamlit as st
import pandas as pd


def name(Name):
    return "Hey "+Name+"! Fill other details to get Connected!"

df = pd.read_csv(r'upwork.csv')

df["Combined_Skills"] = df["Skill_1"] + ' ' +\
                        df["Skill_2"] + ' ' +\
                        df["Skill_3"] + ' ' +\
                        df["Skill_4"] + ' ' +\
                        df["Skill_5"] + ' ' +\
                        df["Skill_6"] + ' ' +\
                        df["Skill_7"] + ' ' +\
                        df["Skill_8"] + ' ' +\
                        df["Skill_9"] + ' ' +\
                        df["Skill_10"]

df_new = df[["Name", "Hourly_Rate", "Expertise_Level", "Combined_Skills", "Job Title"]]
List1 = list(df_new.Hourly_Rate)
List1_modified = []
for i in range(len(List1)):
    x = float(List1[i].strip().strip('$'))
    List1_modified.append(x)

df_new["Hourly_Rate1"] = List1_modified

st.sidebar.title("Let me know you")
template = """
    <div style = "background-color : grey; padding : 7.9px;">
    </div>
    """
st.markdown(template, unsafe_allow_html=True)
st.image("female workers_2.png",width=698)

Name = st.sidebar.text_input("Your Name")
if len(Name)>2:
        st.success(name(Name))

st.sidebar.text_input("Enter your company")
lookingfor = st.sidebar.text_input("What skills you are looking for")

level_of_expertise = st.sidebar.selectbox('Select level of expertise', ["Beginner", "Intermediate", "Expert"])
pricing_per_hour = st.sidebar.text_input("Enter your pricing per hour")
if st.sidebar.button("Find Freelancers"):
    st.write("Here are your recommended freelancers")

    List2 = list(df_new.Combined_Skills)
    List2_modified = []
    import itertools as itrt
    for i in range(len(List2)):
        print(lookingfor, "--->", List2[i])
        Count = len(lookingfor.split(' '))
        List3 = list(itrt.combinations(List2[i].lower().split(' '), Count))
        List4 = []
        for j in range(len(List3)):
            x = cosinesimilarity(lookingfor.lower(), str(List3[j]))
            List4.append(x)

        List2_modified.append(float(max(List4)))

    df_new["Similarity"] = List2_modified

    df_new1 = df_new.query("Hourly_Rate1 == " + str(pricing_per_hour))
    df_new2 = df_new.query("Similarity > 0.9")
    df_new3 = df_new2.query("Expertise_Level == @level_of_expertise")
    df_display = df_new3[["Name", "Job Title","Combined_Skills", "Expertise_Level","Hourly_Rate","Similarity"]]

    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #000066; color: white;'
    }
    df_display.style.set_table_styles([cell_hover, index_names, headers])
    df_display.style.highlight_max(axis=0)
    st.dataframe(df_display.style.highlight_max(axis=0))
    st.success("Table: List of matches")
