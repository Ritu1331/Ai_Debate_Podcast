from rag.retrieve import retrieve_context

query = "social media"

context = retrieve_context(query)

print("\nRETRIEVED CONTEXT:\n")
print(context)