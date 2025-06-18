@app.post("/api/")
async def get_response(data: QueryInput):
    if db is None:
        return {
            "answer": "Vectorstore is not available.",
            "links": []
        }

    try:
        docs = db.similarity_search(data.question)
        content = "\n\n".join([doc.page_content for doc in docs])

        prompt = PromptTemplate.from_template(
            "You're a helpful TA for the TDS course. Use the context below:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"
        )
        final_prompt = prompt.format(context=content, question=data.question)
        response = llm.invoke(final_prompt)

        # Dummy links if needed — replace with real ones if desired
        links = [
            {
                "url": "https://discourse.onlinedegree.iitm.ac.in/",
                "text": "Refer to course discussion for more clarity."
            }
        ]

        return {
            "answer": response,
            "links": links
        }

    except Exception as e:
        return {
            "answer": f"Error generating response: {str(e)}",
            "links": []
        }
