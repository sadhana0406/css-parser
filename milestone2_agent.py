KNOWLEDGE_BASE = {
    "refund policy": "Refund requests can be submitted within 7 days of purchase.",
    "working hours": "Our working hours are Monday to Friday, 9 AM to 5 PM.",
    "internship duration": "The internship duration depends on the assigned programme."
}

CONTACT_INFO = {
    "email": "support@example.com",
    "phone": "1234567890"
}



def search_knowledge(question):
    question = question.lower()

    for topic, information in KNOWLEDGE_BASE.items():
        if all(word in question for word in topic.split()):
            return information

    return None


# Tool 2: Retrieve contact information
def get_contact_info(question):
    question = question.lower()

    if "email" in question:
        return CONTACT_INFO["email"]

    if "phone" in question or "contact number" in question:
        return CONTACT_INFO["phone"]

    return None



def answer_question(question):
    question = question.strip()

    if not question:
        return "Please enter a question."

    answer = search_knowledge(question)

    if answer is not None:
        return answer

    answer = get_contact_info(question)

    if answer is not None:
        return answer

    return "I don't have enough information to answer that question."



if __name__ == "__main__":
    print("Knowledge-Based Agent")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nYou: ")

        if question.lower().strip() == "exit":
            print("Agent: Goodbye!")
            break

        print("Agent:", answer_question(question))
