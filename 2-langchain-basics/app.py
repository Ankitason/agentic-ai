import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

st.title("Product price prediction")
class Product(BaseModel):
    name:str=Field(description="Provide actual name of the product")
    details: str = Field(max_length=200,description="A small summary of the product")
    price: int = Field(description="provide tentative price of the product in USD with doller sign")
    
llm=ChatGroq(model="qwen-qwq-32b")

output_parser=JsonOutputParser(pydantic_object=Product)

promt=ChatPromptTemplate(
    [
        ("system", "You are a sales helpful assistant. provide details for asked products in json{format_instruction}"),
        ("human","{product}")
    ]
).partial(format_instruction=output_parser.get_format_instructions())

chain=promt|llm|output_parser
st.markdown("**Write down your product name here.**")
product_name=st.text_input("Give me the product name", value="Macbook Pro 2017 model",placeholder="Macbook Pro 2017 model", max_chars=50)
# product_name = st.text_area(
#     "Give me the product name", placeholder="Macbook Pro 2017 model", max_chars=50
# )
result=chain.invoke({"product":product_name})
st.subheader("Product Info")
st.write(result)
# st.markdown(f"**Name:** {result['name']}")
# st.markdown(f"**Details:** {result['details']}")
st.markdown(f"**Price (INR):** ${result['price']}")
