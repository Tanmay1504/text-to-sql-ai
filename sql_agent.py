import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

load_dotenv()

# Step 1 — Connect to the database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.db")
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

# Step 2 — Create the LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

# Step 3 — Create the SQL agent
agent = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="tool-calling",
    verbose=False
)

# Step 4 — Test it with a few questions
if __name__ == "__main__":
    questions = [
        "How many customers are there?",
        "Which city has the most customers?",
        "What is the total revenue across all orders?",
        "Who is the top customer by total order amount?",
        "Which brand has the highest average rating?"
    ]
    
    for q in questions:
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print(f"{'='*70}")
        result = agent.invoke({"input": q})
        print(f"\nFINAL ANSWER: {result['output']}")