# %%
from pydantic import Field, BaseModel
import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

## Langsmith Tracking And Tracing
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"


# %%
class Product(BaseModel):
    name:str=Field(description="Provide actual name of the product")
    price: int = Field(description="provide price of the product in USD")
    

# %%
from langchain_groq import ChatGroq
model=ChatGroq(model="qwen-qwq-32b")
model

# %%
from langchain_core.prompts import ChatPromptTemplate
prompt=ChatPromptTemplate(
    [
    ("system", "You are a helpful assistant. When asked about any product, respond in JSON with product name, details, and a tentative price in USD (integer)."),
    ("human","{product}")
    ]
)
prompt

# %%
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
output_parser=JsonOutputParser(pydantic_object=Product)


# %%
chain=prompt|model|output_parser

# %%
print(chain.invoke({"product":"tell me about iPhone 15"}))




