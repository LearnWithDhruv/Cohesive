from transformers import pipeline
import torch
CONFIDENCE_THRESHOLD = 0.7

def enrich_data(content, query):
    if not content or not query:
        return "NO"
    
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli",
        device=0 if torch.cuda.is_available() else -1
    )
    
    candidate_labels = ["yes", "no"]
    
    sequence_to_classify = f"Question: {query}\nContext: {content[:1000]}"  # Limit context
    
    try:
        result = classifier(sequence_to_classify, candidate_labels)
        
        if result['scores'][0] > CONFIDENCE_THRESHOLD:
            return "YES" if result['labels'][0] == "yes" else "NO"
        return "NO"
    except Exception as e:
        print(f"Classification error: {e}")
        return "NO"
