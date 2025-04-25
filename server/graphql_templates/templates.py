from enum import Enum
import json
import base64
import hashlib

def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def base64_json(content: dict) -> str:
    return base64.b64encode(json.dumps(content, separators=(',', ':')).encode("utf-8")).decode("utf-8")

# Plain JSON variables
variables_dict = {
    "hideUnavailableItems": False,
    "skusFilter": "ALL_AVAILABLE",
    "installationCriteria": "MAX_WITHOUT_INTEREST",
    "category": "",
    "collection": "34830",
    "specificationFilters": [],
    "orderBy": "OrderByTopSaleDESC",
    "from": 0,
    "to": 15,
    "shippingOptions": [],
    "variant": "",
    "advertisementOptions": {
        "showSponsored"          : False,
        "sponsoredCount"         : 2,
        "repeatSponsoredProducts": False,
        "advertisementPlacement" : "home_shelf"
    }
}

encoded_variables = base64_json(variables_dict)

class GraphQLTemplate(Enum):
    ObtenerAceites = {
        "graphql_url": "https://www.jumbocolombia.com/_v/segment/graphql/v1",
        "params": {
            "workspace": "master",
            "maxAge": "short",
            "appsEtag": "remove",
            "domain": "store",
            "locale": "es-CO",
            "__bindingId": "2aad81c0-c729-41f4-a13b-002deae8039a",
            "operationName": "Products",
            "variables": "{}",
            "extensions": json.dumps({
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "21326beabc3e4114a48f876e981ac6f0c1561482d9ef2b773c08b8b57e2f83d6",
                    "sender": "vtex.store-resources@0.x",
                    "provider": "vtex.search-graphql@0.x"
                },
                "variables": encoded_variables
            })
        },
        "raw_variables": variables_dict
    }