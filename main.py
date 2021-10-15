import bz2
import pickle
import _pickle as cPickle
import streamlit as st 
import pandas as pd


df = pd.read_csv('data.csv', index_col=0)

# Load any compressed pickle file
def decompress_pickle(file):
 data = bz2.BZ2File(file, 'rb')
 data = cPickle.load(data)
 return data


titles = df['make'].drop_duplicates()


cosine_sim_mat = decompress_pickle('cosine_sim_mat.pbz2') 

def get_recommendation(title,cosine_sim_mat,df,num_of_rec=10):
	# indices of the course
	course_indices = pd.Series(df.index,index=df['old']).drop_duplicates()
	# Index of course
	idx = course_indices[title]

	# Look into the cosine matr for that index
	sim_scores =list(enumerate(cosine_sim_mat[idx]))
	sim_scores = sorted(sim_scores,key=lambda x: x[1],reverse=True)
	selected_course_indices = [i[0] for i in sim_scores[1:]]
	selected_course_scores = [i[0] for i in sim_scores[1:]]

	# Get the dataframe & title
	result_df = df.iloc[selected_course_indices]
	result_df['similarity_score'] = selected_course_scores
	final_recommended_courses = result_df[['old']]
	return final_recommended_courses.head(num_of_rec)

st.markdown("<h2 style='text-align: center;'>مقترح المنتجات العلمية الآلي </h2>", unsafe_allow_html=True)
  

st.markdown("<h4 style='text-align: center; color: orange;'>اختر أحد المنتجات العلمية التي تعجبك وسوف نقترح عليك بعض المنتجات ذات العلاقةا</h4>", unsafe_allow_html=True)


with st.form(key='mlform'):

    #st.markdown("<h6 style='text-align: center;'>ادخل النص المراد تصنيفه</h6>", unsafe_allow_html=True)

    #message = st.text_area("")
    message = st.sidebar.selectbox('اختر أحد المنتجات العلمية', titles)

    submit_message = st.form_submit_button(label='اقترح المزيد')
    
if submit_message:
    results = get_recommendation(message,cosine_sim_mat,df,10)
    st.write(results)
    #st.markdown("<h3 style='text-align: center;color:red'>"+  pred +"</h3>", unsafe_allow_html=True)

    