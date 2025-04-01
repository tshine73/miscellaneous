import os
import yaml
import logging
import google.cloud.logging
from flask import Flask, render_template, request

from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from vertexai.preview.prompts import Prompt
import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from langchain_google_vertexai import VertexAIEmbeddings
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    SafetySetting
)

from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure

# Configure Cloud Logging
logging_client = google.cloud.logging.Client()
logging_client.setup_logging()
logging.basicConfig(level=logging.INFO)

# Read application variables from the config fle
BOTNAME = "FreshBot"
SUBTITLE = "Your Friendly Restaurant Safety Expert"

app = Flask(__name__)

# Initializing the Firebase client
db = firestore.Client()

# TODO: Instantiate a collection reference
collection = db.collection("food-safety")

PROJECT_ID = "qwiklabs-gcp-00-7877708d10e9"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

# TODO: Instantiate an embedding model here
embedding_model = VertexAIEmbeddings(model_name="text-embedding-004")

# TODO: Instantiate a Generative AI model here
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)

gen_model = GenerativeModel(model_name="gemini-pro", generation_config=GenerationConfig(temperature=0))


# TODO: Implement this function to return relevant context
# from your vector database
def search_vector_database(query: str):
    # 1. Generate the embedding of the query
    embedding = embedding_model.embed([query])[0]

    # 2. Get the 5 nearest neighbors from your collection.
    # Call the get() method on the result of your call to
    # find_neighbors to retrieve document snapshots.
    vector_query = collection.find_nearest(
        vector_field="embedding",
        query_vector=Vector(embedding),
        # query_vector=Vector([3.0, 1.0, 2.0]),
        distance_measure=DistanceMeasure.EUCLIDEAN,
        limit=5,
        distance_result_field="vector_distance",
    )

    # 3. Call to_dict() on each snapshot to load its data.
    # Combine the snapshots into a single string named context
    docs = vector_query.get()
    context = " ".join(doc.to_dict().get("content", "") for doc in docs)

    # Don't delete this logging statement.
    logging.info(
        context, extra={"labels": {"service": "cymbal-service", "component": "context"}}
    )
    return context


# TODO: Implement this function to pass Gemini the context data,
# generate a response, and return the response text.
def ask_gemini(question):
    # 1. Create a prompt_template with instructions to the model
    # to use provided context info to answer the question.
    prompt_template = """
        Role: You work for Cymbal Shops, a chain offering prepared meals to-go in busy downtown areas.
        The company's employees in the New York area needs to meet the New York City Department of Health and Mental Hygiene's food safety guidelines as provided in this Food Protection Training Manual.
        You are an assistant for question-answering tasks.
        Use the following pieces of retrieved context to answer the question.
        If you don't know the answer, just say that you don't know or NA.
        Keep the answer to the point follow the guidelines below.
        Guidelines:        
        - For yes/no questions, answer with either 'Yes' or 'No' based on the context.
        - If no relevant information is available, return 'NA'.
        - Do not provide any additional commentary or filler text. Focus on precision and brevity.
        Use the following pieces of retrieved context to answer.
        Question: {query}
        Context: {context}
    """

    # 2. Use your search_vector_database function to retrieve context
    # relevant to the question.
    context = search_vector_database(question)

    # 3. Format the prompt template with the question & context
    variables = [
        {
            "query": [question],
            "context": [context]
        },
    ]

    generation_config = GenerationConfig(temperature=0)

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
    ]

    prompt = Prompt(
        prompt_data=prompt_template,
        model_name="gemini-pro",
        variables=variables,
        generation_config=generation_config,
        safety_settings=safety_settings,
        system_instruction=["""Respond to the question concisely"""]
    )

    # 4. Pass the complete prompt template to gemini and get the text
    # of its response to return below.

    response = prompt.generate_content(
        contents=prompt.assemble_contents(**prompt.variables[0])
    )

    return response.text


# The Home page route
@app.route("/", methods=["POST", "GET"])
def main():
    # The user clicked on a link to the Home page
    # They haven't yet submitted the form
    if request.method == "GET":
        question = ""
        answer = "Hi, I'm FreshBot, what can I do for you?"

    # The user asked a question and submitted the form
    # The request.method would equal 'POST'
    else:
        question = request.form["input"]
        # Do not delete this logging statement.
        logging.info(
            question,
            extra={"labels": {"service": "cymbal-service", "component": "question"}},
        )

        # Ask Gemini to answer the question using the data
        # from the database
        answer = ask_gemini(question)

    # Do not delete this logging statement.
    logging.info(
        answer, extra={"labels": {"service": "cymbal-service", "component": "answer"}}
    )
    print("Answer: " + answer)

    # Display the home page with the required variables set
    config = {
        "title": BOTNAME,
        "subtitle": SUBTITLE,
        "botname": BOTNAME,
        "message": answer,
        "input": question,
    }

    return render_template("index.html", config=config)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))