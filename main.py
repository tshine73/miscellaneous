import asyncio
import datetime
import uuid

import aiohttp
# from google.cloud import discoveryengine_v1, dialogflowcx_v3, dialogflowcx
import pandas as pd

from utils.io_utils import write


def list_engines(parent):
    client = discoveryengine_v1.EngineServiceClient().from_service_account_json("data-sandbox.json")

    next_page_token = ""
    engines = []

    while True:
        request = discoveryengine_v1.ListEnginesRequest(
            parent=parent,
            # ,filter="solution_type:SOLUTION_TYPE_SEARCH"
            page_token=next_page_token
        )

        response = client.list_engines(request=request)

        engines += response.engines
        next_page_token = response.next_page_token
        if not next_page_token:
            break

    return engines


def list_data_stores(parent):
    client = discoveryengine_v1.DataStoreServiceClient().from_service_account_json("data-sandbox.json")

    next_page_token = ""
    data_stores = []

    while True:
        request = discoveryengine_v1.ListDataStoresRequest(
            parent=parent,
            # ,filter="solution_type:SOLUTION_TYPE_SEARCH"
            page_token=next_page_token
        )

        response = client.list_data_stores(request=request)

        data_stores += response.data_stores
        next_page_token = response.next_page_token
        if not next_page_token:
            break

    return data_stores


def list_documents(parent):
    client = discoveryengine_v1.DocumentServiceClient().from_service_account_json("data-sandbox.json")

    request = discoveryengine_v1.ListDocumentsRequest(parent=parent)

    response = client.list_documents(request=request)

    return response


def create_document(data_store_resource_name):
    document_resource_name = f"{data_store_resource_name}/branches/default_branch"

    gs_file_uri = "gs://llm-product-v1-bq-schema/AI人工智慧技術於稽核實務之應用.pptx"
    content = discoveryengine_v1.Document.Content(
        uri=gs_file_uri,
        mime_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )
    id = str(uuid.uuid4())
    document_id = f"{document_resource_name}/documents/{id}"
    # print(len(str(id)))
    json_schema = """
    {"type":"object","geolocation_detection":true,"$schema":"https://json-schema.org/draft/2020-12/schema","date_detection":true}
    """
    doc = discoveryengine_v1.Document(
        # name=document_id,
        # id=id,
        # schema_id="default_schema",
        content=content,
        # parent_document_id=id,
        # json_data=json_schema
        struct_data={}
    )

    print(doc)

    request = discoveryengine_v1.CreateDocumentRequest(
        parent=document_resource_name,
        document=doc,
        document_id=id
    )
    client = discoveryengine_v1.DocumentServiceClient().from_service_account_json("data-sandbox.json")

    resp = client.create_document(request=request)

    return resp


def list_schemas(data_store_resource_name):
    client = discoveryengine_v1.SchemaServiceClient().from_service_account_json("data-sandbox.json")
    resp = client.list_schemas(discoveryengine_v1.ListSchemasRequest(parent=data_store_resource_name))
    for r in resp:
        print(type(r.json_schema))
        print(r.json_schema)

def other_task():

    parent = "projects/660356120093/locations/global/collections/default_collection"
    id = "bq-schema-datastore-searchapp_1719806416057"
    data_store_resource_name = f"{parent}/dataStores/{id}"

    # list_schemas(data_store_resource_name)
    # exit(1)

    resp = create_document(data_store_resource_name)
    print(resp)

    print("---------created document")
    document_name = "projects/660356120093/locations/global/collections/default_collection/dataStores/bq-schema-datastore-searchapp_1719806416057/branches/default_branch"
    document = list_documents(document_name)
    for d in document:
        print(d)
    exit(1)


    for a in list_data_stores(parent=parent):
        print(a)

    engines = {e.name: e for e in list_engines(parent=parent)}
    data_stores = {e.name: e for e in list_data_stores(parent=parent)}

    for d in data_stores:
        print(data_stores[d])
    exit(1)

    names = ["2f20219a-d493-41b8-bfc9-54c2cbd7dfef", "bq-schema-search-agent_1719806274404"]
    engine_identities = []
    data_store_identities = []

    engine_dict = {}
    data_store_dict = {}
    for name in names:
        engine_name = f"{parent}/engines/{name}"
        engine = engines[engine_name]

        # print(engine.create_time)
        # print(type(engine.create_time))
        # exit(1)

        cur_data_stores = []
        for data_store_id in engine.data_store_ids:
            data_store_name = f"{parent}/dataStores/{data_store_id}"
            data_store = data_stores[data_store_name]
            cur_data_stores.append(data_store)

            connected_engines = data_store_dict.setdefault(data_store_name, [])
            connected_engines.append(engine)

        engine_dict[engine_name] = cur_data_stores

    for (k, v) in engine_dict.items():
        print(f"engine {k} with following data stores")
        for a in v:
            print(a)
        print("--------------")

    print("------------------------------------------")
    for (k, v) in data_store_dict.items():
        print(f"data store {k} with following engines")
        for a in v:
            print(a)
        print("--------------")
    exit(1)

    project = "data-sandbox-344301"
    location = "global"
    serving_config = "projects/data-sandbox-344301/locations/global/collections/default_collection/engines/bq-schema-search-agent_1719806274404/servingConfigs/default_serving_config"

    # client = discoveryengine_v1.ConversationalSearchServiceClient().from_service_account_json("data-sandbox.json")
    # query = discoveryengine_v1.Query()
    # query.text = "how's going?"
    # request = discoveryengine_v1.AnswerQueryRequest(
    #     serving_config=serving_config,
    #     query=query,
    # )

    # Make the request
    # response = client.answer_query(request=request)
    # print(response)

    name = "projects/660356120093/locations/global/collections/default_collection/engines/bq-schema-search-agent_1719806274404"

    client = discoveryengine_v1.EngineServiceClient().from_service_account_json("data-sandbox.json")

    requests = discoveryengine_v1.GetEngineRequest(name=name)
    response = client.get_engine(request=requests)
    print(response)
    # data store list

    for data_store_id in response.data_store_ids:
        print(data_store_id)

    data_store_client = discoveryengine_v1.DataStoreServiceClient().from_service_account_json("data-sandbox.json")

    request = discoveryengine_v1.GetDataStoreRequest(
        name="projects/660356120093/locations/global/collections/default_collection/dataStores/bq-schema-datastore-searchapp_1719806416057")
    data_store = data_store_client.get_data_store(request=request)
    print(data_store)




if __name__ == "__main__":
    # df =pd.read_excel("/Users/steven.fanchiang/geek/project/舊振南/銷售資料.xlsx")
    # records = df.to_json(orient="records", lines=True, force_ascii=False)
    #
    # write(records, "舊振南_sales_data.json")

    df = pd.read_json("舊振南_sales_data.json", lines=True)
    # 1668988800000
    df["date"] = pd.to_datetime(df["販售日"], unit="ms")

    # Assuming df is your DataFrame
    distinct_values = df["項目名稱"].unique()

    # Printing the distinct values
    print(distinct_values)
    print(len(distinct_values.tolist()))

    # print(df.dtypes)
    # print(df)

