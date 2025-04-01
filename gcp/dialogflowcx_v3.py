import asyncio
import datetime
import uuid

import aiohttp
from google.cloud import discoveryengine_v1, dialogflowcx_v3, dialogflowcx
from google.cloud.dialogflowcx_v3 import AgentsClient, SessionsClient
from google.cloud.dialogflowcx_v3.types import session


def run_sample():
    # TODO(developer): Replace these values when running the function
    project_id = "data-sandbox-344301"
    # For more information about regionalization see https://cloud.google.com/dialogflow/cx/docs/how/region
    location_id = "global"
    # For more info on agents see https://cloud.google.com/dialogflow/cx/docs/concept/agent
    agent_id = "a553cc7e-b85a-4244-9db7-033b02b88726"
    agent = f"projects/{project_id}/locations/{location_id}/agents/{agent_id}"
    # For more information on sessions see https://cloud.google.com/dialogflow/cx/docs/concept/session
    session_id = uuid.uuid4()
    texts = ["如要針對融資循環的股東大會通過作業進行查核時，會有哪些控制項目及風險點？"]
    # For more supported languages see https://cloud.google.com/dialogflow/es/docs/reference/language
    language_code = "zh-tw"

    detect_intent_texts(agent, session_id, texts, language_code)


def detect_intent_texts(agent, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_path = f"{agent}/sessions/{session_id}"
    print(f"Session path: {session_path}\n")
    client_options = None
    agent_components = AgentsClient.parse_agent_path(agent)
    location_id = agent_components["location"]
    if location_id != "global":
        api_endpoint = f"{location_id}-dialogflow.googleapis.com:443"
        print(f"API Endpoint: {api_endpoint}\n")
        client_options = {"api_endpoint": api_endpoint}
    session_client = SessionsClient(client_options=client_options)

    for text in texts:
        text_input = session.TextInput(text=text)
        query_input = session.QueryInput(text=text_input, language_code=language_code)
        request = session.DetectIntentRequest(
            session=session_path, query_input=query_input
        )

        response = session_client.detect_intent(request=request)

        print("=" * 20)
        print(f"Query text: {response.query_result.text}")
        response_messages = [
            " ".join(msg.text.text) for msg in response.query_result.response_messages
        ]
        print(f"Response text: {' '.join(response_messages)}\n")


if __name__ == "__main__":
    project = "data-sandbox-344301"
    location = "global"
    # serving_config = "projects/data-sandbox-344301/locations/global/collections/default_collection/engines/search-app-microfusionweb_1721035876007/servingConfigs/default_serving_config"
    serving_config = "projects/data-sandbox-344301/locations/global/collections/default_collection/engines/a553cc7e-b85a-4244-9db7-033b02b88726/servingConfigs/default_serving_config"

    # client = discoveryengine_v1.ConversationalSearchServiceClient().from_service_account_json("data-sandbox.json")

    run_sample()
    #
    #
    # query = discoveryengine_v1.Query()
    # query.text = "如要針對融資循環的股東大會通過作業進行查核時，會有哪些控制項目及風險點？"
    # request = discoveryengine_v1.AnswerQueryRequest(
    #     serving_config=serving_config,
    #     query=query,
    # )

