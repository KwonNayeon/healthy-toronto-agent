from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from dotenv import load_dotenv
import os
import pandas as pd
import io

# Load .env file
load_dotenv()

# Define data directly as a string
data_str = """name,address,category,price_range,vegan,vegetarian,gluten_free,grab_and_go,open_status,notes
Kupfert & Kim,"140 Spadina Ave / 83 Critchley Ln",Plant-based,$$,Y,Y,Y,Y,Open,"Wheat-free, meat-free, bowls, toasts, smoothies"
imPerfect Fresh Eats,"1108 Bay St. Unit A","Healthy Bowls/Wraps",$,Y,Y,Y,Y,Open,"Customizable bowls, wraps, smoothies, locally-sourced"
Mad Radish,"120 Bloor St E","Healthy Bowls/Soups",$$,Y,Y,Y,Y,Open,"Bowls, sandwiches, soups, compostable packaging"
Copper Branch,"199 Bay St",Plant-based,$$,Y,Y,Y,Y,Open,"Quinoa bowls, plant-based, breakfast/lunch/dinner"
Planta,"60 Bloor St W",Vegan,$$$,Y,Y,Y,N,Open,"Trendy vegan, salads, wraps, higher price"
Impact Kitchen,"1222 Yonge St","Healthy Bowls/Soups",$$,Y,Y,Y,Y,Open,"Power bowls, soups, gluten-free bread, grab-and-go"
Basil Box,"351 Yonge St","Asian Fusion",$,Y,Y,Y,Y,Open,"Build-your-own box, Southeast Asian inspired, open 7 days"
The Goods,"279 Roncesvalles Ave","Vegan/Organic",$$,Y,Y,Y,Y,Open,"Organic, gluten-free, sugar-free, functional ingredients"
Tractor Everyday,"151 Yonge St","Healthy Cafe",$$,Y,Y,Y,Y,Open,"Salads, bowls, soups, whole grains, nuts, lean proteins"
Aamazing Salad,"82 Adelaide St E","Salads/Bowls",$,Y,Y,Y,Y,Open,"Salads, bowls, wraps, supports SickKids Foundation"
The Sushi Bowl | MSB,"1 King's College Circle","Sushi Bowls",$,Y,Y,Y,Y,Open,"Build-your-own sushi bowl, vegan/gluten-free options, TBucks"
Za'atar | MSB,"1 King's College Circle",Mediterranean,$,Y,Y,Y,Y,Open,"Greek/Turkish/Middle Eastern, vegan/vegetarian, TBucks"
Kung Fu Tea | Sid Smith,"100 St. George St","Bubble Tea/Cafe",$,Y,Y,?,Y,Open,"Milk teas, smoothies, snacks"
Fair Trade Café (Robarts),"130 St. George St","Café/Bakery",$,Y,Y,?,Y,Open,"Grab-and-go bakery, sandwiches, staff can warm food"
Veda,"Hart House","Vegetarian Indian",$,Y,Y,?,Y,Open,"Vegetarian/vegan Indian, highly recommended by students"
H Mart Dundas,"705 Dundas St W","Asian Market",$,?,?,?,Y,Open,"Ready meals: Dongpo pork rice bowl, food court style, discounts after 8pm"
Galleria Supermarket,"7040 Yonge St","Asian Market",$,?,?,?,Y,Open,"Poke, bulgogi rice bowl, kimbap, discounts after 8pm"
Banh Mi Nguyen Huong,"322 Spadina Ave","Vietnamese Sandwich",$,?,?,?,Y,Open,"Banh mi $5.50, very fast, cash only"
Yummy Korean Food Restaurant,"620 Bloor St W",Korean,$,?,?,?,Y,Open,"Bibimbap, bulgogi, tteokbokki, large portions, good value"
"""

# Create DataFrame from string
df = pd.read_csv(io.StringIO(data_str), quotechar='"', escapechar='\\')

# Convert each row into a string document
def row_to_text(row):
    return f""" {row['name']} is located at {row['address']}. Category: {row['category']}. Price: {row['price_range']}. Open status: {row['open_status']}. Healthy options - Vegan: {row['vegan']}, Vegetarian: {row['vegetarian']}, Gluten-Free: {row['gluten_free']}, Grab & Go: {row['grab_and_go']}. Notes: {row['notes']}. """

# Apply formatting
texts = df.apply(row_to_text, axis=1).tolist()

# Wrap into LangChain Documents
documents = [Document(page_content=text) for text in texts]

# STEP 3: Split if needed (can skip if docs are already short)
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = splitter.split_documents(documents)

# STEP 4: Embed & Store into Chroma (or FAISS if you prefer)
embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(split_docs, embedding, persist_directory="db")
vectorstore.persist()

print("Ingestion complete! Vector DB stored in ./db")
