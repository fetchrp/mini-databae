# all langchain functionality
# lc = langchain, not leetcode

from typing import Annotated
from typing_extensions import TypedDict, Literal
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from sql_helper import execute_query_in_db, get_schema_in_db
from prompts import GENERATOR_SYSTEM_PROMPT, ANALYZE_DATA_SET_PROMPT, REMOVE_DEEPSEEK_THINKING_SQL_PROMPT, REMOVE_DEEPSEEK_THINKING_EXPLANATION_PROMPT
import json
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings

load_dotenv()

class State(TypedDict):
    # needed for logging into db
    host: str
    port: int
    username: str
    password: str
    database: str
    # to get the results
    message: str # what is the user's request?
    sql_query: str
    result_set: str
    analysis: str

# the 2 llms needed
llm = ChatGroq(temperature=0, model_name="deepseek-r1-distill-llama-70b")
llm2 = ChatGroq(temperature=0, model_name="llama-3.1-8b-instant")

def get_vector_store(jsonDict: dict):
    # intialize vector store
    vector_store = InMemoryVectorStore(OpenAIEmbeddings())

    # split the json into chunks    
    splitter = RecursiveJsonSplitter(max_chunk_size=100)

    # put these documents into a vector store    
    vector_store.add_texts([json.dumps(chunk) for chunk in jsonDict])

    return vector_store

    
    
# checks whether the query executed properly or not
def execution_checker(state: State) -> Literal["generator", "analysis"]: # parameter should be the sql query
    if state["result_set"] == "":
        return "generator"
    else:
        return "analysis"

# store in vector store
# generates the sql query based off of the schema
def generate_query(state: State) -> str:
    schema_result = get_schema_in_db(state["host"], state["port"], state["username"], state["password"], state["database"])

    vector_store = get_vector_store(schema_result)
    needed_schemas = vector_store.similarity_search(state["message"], k=3)

    # because langchain does not like the fact that theres {} and it wants you to put {{ }} :)
    needed_schemas_text = "\n".join([doc.page_content.replace("{", "{{").replace("}", "}}") for doc in needed_schemas])

    template_preparsed = ChatPromptTemplate.from_messages([
        ("system", GENERATOR_SYSTEM_PROMPT),
        ("human", f"""
        Here is a part of the schema that can be used to generate the SQL query:
        {needed_schemas_text}

        Here is the user's request:
        {state["message"]}"""
        )
    ])
    prompt_value_preparsed = template_preparsed.invoke({})
    response_preparsed = llm.invoke(prompt_value_preparsed)

    template_postparsed = ChatPromptTemplate.from_messages([
        ("system", REMOVE_DEEPSEEK_THINKING_SQL_PROMPT),
        ("human", f"""
        Here is the response you are to clean:
        {response_preparsed.content}
        """
        )
    ])
    prompt_value_postparsed = template_postparsed.invoke({})
    response_postparsed = llm2.invoke(prompt_value_postparsed)

    state["sql_query"] = response_postparsed.content
    return state

# executes the query
def execute_query(state: State) -> str:
    result = execute_query_in_db(state["host"], state["port"], state["username"], state["password"], state["database"], state["sql_query"])
    state["result_set"] = result
    return state

# analysis of result set
def analyze_result_set(state: State) -> str:
    result_set_postprocessed = state["result_set"].replace("{", "{{").replace("}", "}}")
    template_preparsed = ChatPromptTemplate.from_messages([
        ("system", ANALYZE_DATA_SET_PROMPT),
        ("human", f"""
        Here is the data set you should analyze:
        {result_set_postprocessed}"""
        )
    ])
    prompt_value_preparsed = template_preparsed.invoke({})
    response_preparsed = llm.invoke(prompt_value_preparsed)

    template_postparsed = ChatPromptTemplate.from_messages([
        ("system", REMOVE_DEEPSEEK_THINKING_EXPLANATION_PROMPT),
        ("human", f"""
        Here is the response you are to clean:
        {response_preparsed.content}
        """
        )
    ])
    prompt_value_postparsed = template_postparsed.invoke({})
    response_postparsed = llm2.invoke(prompt_value_postparsed)

    state["analysis"] = response_postparsed.content
    return state


graph_builder = StateGraph(State)

# add nodes and callback functions
graph_builder.add_node("generator", generate_query)
graph_builder.add_node("executor", execute_query)
graph_builder.add_node("analyzer", analyze_result_set)

# setup edges
graph_builder.add_edge(START, "generator")
graph_builder.add_edge("generator", "executor")
graph_builder.add_conditional_edges(
    "executor", 
    execution_checker, 
    {"generator": "generator", "analysis": "analyzer"}
)
graph_builder.add_edge("analyzer", END)
graph = graph_builder.compile()
