import streamlit as st
import pandas as pd

@st.cache_data
def fetch_exam_data():
    # Fetch and return exam data from data source
    return pd.read_csv('path_to_exam_data.csv')

@st.cache_data
def fetch_questions():
    # Fetch and return questions from data source
    return pd.read_csv('path_to_questions.csv')

# Initialize state
if 'questions' not in st.session_state:
    st.session_state.questions = fetch_questions()

if 'exam_data' not in st.session_state:
    st.session_state.exam_data = fetch_exam_data()

# Function to display questions
def display_questions():
    for question in st.session_state.questions:
        st.write(question)

# Main execution
if __name__ == '__main__':
    st.title('CBT Exam Portal')
    display_questions()