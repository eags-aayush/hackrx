import json

def format_output(decision, docs):
    return {
        "decision": decision,
        "clauses": [
            {
                "text": d["text"],
                "source": d.get("source", "unknown"),
                "page": d.get("page", -1)
            } for d in docs
        ]
    }