# the complete sql agent , text to sql project this one 



import os
import streamlit as st
import pandas as pd
import sqlite3
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

# ===== Page setup =====
st.set_page_config(
    page_title="Text-to-SQL AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Text-to-SQL AI Agent")
st.caption("Ask questions about the QSR database in plain English — powered by Llama 3.1 70B")

# ===== Database setup =====
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.db")
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# ===== Cache the agent =====
@st.cache_resource
def get_agent():
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
        temperature=0
    )
    return create_sql_agent(
        llm=llm,
        db=db,
        agent_type="tool-calling",
        verbose=False,
        return_intermediate_steps=True   # NEW — gives us the SQL queries
    )

agent = get_agent()

# ===== Helper to extract SQL from agent's intermediate steps =====
def extract_sql_and_results(intermediate_steps):
    sql_queries = []
    for action, observation in intermediate_steps:
        if action.tool == "sql_db_query":
            query = action.tool_input.get("query", "") if isinstance(action.tool_input, dict) else str(action.tool_input)
            sql_queries.append({"query": query, "result": observation})
    return sql_queries

# ===== Helper to run SQL and return as DataFrame =====
def run_query_as_df(query):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception:
        return None

# ===== Sidebar =====
with st.sidebar:
    st.header("📊 Database Schema")
    
    tables = db.get_usable_table_names()
    for table in tables:
        with st.expander(f"📁 {table}"):
            schema = db.get_table_info_no_throw([table])
            st.code(schema, language="sql")
    
    st.divider()
    
    st.markdown("**💡 Example Questions:**")
    examples = [
    "How many orders are there in total?",
    "What's the most popular menu item across all brands?",
    "Top 5 customers by lifetime spending",
    "Which restaurant has the highest average rating?",
    "Show me orders that used the 'Diwali Special' promotion",
    "Average order value per brand",
    "Which employee role earns the most on average?",
    "Show me the 3 lowest-rated feedback comments",
    "How many vegetarian menu items does each brand have?",
]
    for ex in examples:
        st.markdown(f"- {ex}")
    
    st.divider()
    
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

# ===== Main chat interface =====
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Show SQL if available
        if "sql_queries" in msg:
            for i, sql_item in enumerate(msg["sql_queries"]):
                with st.expander(f"🔍 SQL Query {i+1}"):
                    st.code(sql_item["query"], language="sql")
                    df = run_query_as_df(sql_item["query"])
                    if df is not None and not df.empty:
                        st.dataframe(df, use_container_width=True)

# User input
if user_question := st.chat_input("Ask a question about the database..."):
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = agent.invoke({"input": user_question})
                answer = result["output"]
                sql_queries = extract_sql_and_results(result.get("intermediate_steps", []))
            except Exception as e:
                answer = f"⚠️ Sorry, I ran into an issue: {str(e)[:200]}"
                sql_queries = []
        
        st.markdown(answer)
        
        # Show SQL queries used
        for i, sql_item in enumerate(sql_queries):
            with st.expander(f"🔍 SQL Query {i+1}"):
                st.code(sql_item["query"], language="sql")
                df = run_query_as_df(sql_item["query"])
                if df is not None and not df.empty:
                    st.dataframe(df, use_container_width=True)
        
        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sql_queries": sql_queries
        }) 