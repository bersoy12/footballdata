import os
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


# os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

db = SQLDatabase.from_uri(conn_string)
llm = ChatOpenAI(model="gpt-4o", temperature=0)



custom_prompt = '''
You are a PostgreSQL expert. Given an input question, first create a syntactically correct PostgreSQL query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per PostgreSQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
Pay attention to key names in stat_types table. You must use only `key` values from stat_types table listed below.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

Only use the following tables:
{table_info}

Question: {input}
'''

prompt = PromptTemplate(input_variables=["input", "top_k", "table_info"], template=custom_prompt)

def response_generator(conn: str, question: str, top_k: int = 5):
    """
    Soruyu SQL sorgusuna çevirip veritabanında çalıştırır
    
    Args:
        conn (str): connection URI to database
        question (str): Kullanıcının sorusu
        top_k (int): Maksimum sonuç sayısı
        
    Returns:
        tuple: (sql_query, result)
    """
    db = SQLDatabase.from_uri(conn)
    chain = create_sql_query_chain(llm, db, prompt)
    sql_query = chain.invoke({
        "question": question,
        "top_k": top_k,
        "table_info": db.get_table_info()
    })

    cleaned_query = sql_query
    if "```sql" in sql_query:
        cleaned_query = sql_query.split("```sql")[1].split("```")[0].strip()
    elif "---sql" in sql_query:
        cleaned_query = sql_query.split("---sql")[1].split("---")[0].strip()
    elif "SQLQuery" in sql_query:
        cleaned_query = sql_query.replace("SQLQuery","").strip()
    elif ":" in sql_query:
        cleaned_query = sql_query.replace(":").strip()

    # result = db.run(cleaned_query)
    return sql_query
