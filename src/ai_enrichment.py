# src/ai_enrichment.py
from transformers import pipeline

def enrich_data(content, query):
    if not content or not query:
        return "No"
    
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    
    result = qa_pipeline({
        "question": query,
        "context": content
    })
    
    print(f"Query: {query}, Answer: {result['answer']}, Score: {result['score']}")
    
    score = result["score"]
    answer = result["answer"].lower()
    
    query_keywords = query.lower().split()
    content_lower = content.lower()
    relevant_keywords = [kw for kw in query_keywords if kw in content_lower]
    
    if score > 0.3 and len(relevant_keywords) > 0:
        print(f"Determined 'Yes' for query '{query}' based on score {score} and keywords {relevant_keywords}")
        return "Yes"
    else:
        print(f"Determined 'No' for query '{query}' based on score {score} and lack of relevant keywords")
        return "No"