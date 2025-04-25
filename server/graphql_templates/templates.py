from enum import Enum
import json
import base64
import hashlib

def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def base64_json(content: dict) -> str:
    return base64.b64encode(json.dumps(content, separators=(',', ':')).encode("utf-8")).decode("utf-8")


ACEITES_COLLECTION_ID    = "34830"
CHOCOLATES_COLLECTION_ID = "32777"

# Plain JSON variables
aceites_dict = {
    "hideUnavailableItems": False,
    "skusFilter": "ALL_AVAILABLE",
    "installationCriteria": "MAX_WITHOUT_INTEREST",
    "category": "",
    "collection": ACEITES_COLLECTION_ID,
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
chocolates_dict = {
    "hideUnavailableItems": False,
    "skusFilter": "ALL_AVAILABLE",
    "installationCriteria": "MAX_WITHOUT_INTEREST",
    "category": "",
    "collection": CHOCOLATES_COLLECTION_ID,
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

encoded_aceites    = base64_json(aceites_dict)
encoded_chocolates = base64_json(chocolates_dict)

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
                "variables": encoded_aceites
            })
        },
        "raw_variables": aceites_dict
    }

    ObtenerChocolates = {
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
                    "sha256Hash": "05731b760fbbc3cb012c734bd800c522f6a37c0082e38ca0bf7c4323b6c25712",
                    "sender": "vtex.store-resources@0.x",
                    "provider": "vtex.search-graphql@0.x"
                },
                "variables": encoded_chocolates
            })
        },
        "raw_variables": chocolates_dict
    }