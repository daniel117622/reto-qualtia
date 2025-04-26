from flask import Flask, jsonify, request, send_file
import requests
import json
import pandas as pd
import os
from datetime import datetime
from urllib.parse import urlparse
from typing import Any, Dict, Callable
from utils.translations import  translate_lang , translate_cop_to_mxn
from utils.return_declarations import produces , consumes
from schemas.responses import Link, ProduceType , ConsumeType


import redis
r = redis.Redis(host='redis-service', port=6379, decode_responses=True)


def extended_jsonify(data: Dict[str, Any]) -> Any:
    index_data = index().get_json()
    
    if isinstance(data, dict):
        return jsonify({
            **data,
            "links": index_data.get("links", [])
        })
    elif isinstance(data, list):
        return jsonify({
            "data": data,
            "links": index_data.get("links", [])
        })
    else:
        raise TypeError("extended_jsonify only supports dict or list types")
    return jsonify(data)

app = Flask(__name__)

# Para testear el decorador agregué varios consumos y productores. No representan nada en realidad
@app.route('/', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@produces("JSON")
@consumes(
    "application/json",
    "application/xml",
    "application/x-www-form-urlencoded",
    "multipart/form-data",
    "text/plain"
)
def index():
    links = []

    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
        # Set up reflection
        view_func = app.view_functions.get(rule.endpoint)

        produces = [ProduceType(rt) for rt in getattr(view_func, '_produce_type', [])]
        consumes = [ConsumeType(ct) for ct in getattr(view_func, '_consume_type', [])]

        allowed_methods = sorted(rule.methods & {"GET", "POST", "PUT", "DELETE", "PATCH"})

        links.append(Link(
            path     = rule.rule,
            methods  = allowed_methods,
            produces = produces,
            consumes = consumes
        ))

    sorted_links = sorted(links, key=lambda l: l.path)

    return jsonify({
        "links": [link.as_dict() for link in sorted_links]
    })



@app.route('/prueba-1', methods=['GET'])
@produces("FILE", "JSON")
def prueba_1():
    url      = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"
    response = requests.get(url)
    data     = response.json()

    custom_attr_item = next(
        (item for item in data['allVariants'][0]['attributesRaw'] if item.get("name") == "custom_attributes"),
        None
    )

    langs = ['en-CR', 'es-CR']
    keys = [
        "Allergens", "SKU", "Vegan", "Kosher", "Organic",
        "Vegetarian", "Gluten_free", "Lactose_free",
        "Package_quantity", "Unit_size", "Net_weight",
        "Propiedad_no_existente"
    ]

    rows = []

    for lang in langs:
        props_str = custom_attr_item['value'].get(lang, '') if custom_attr_item else ''
        props_json = json.loads(props_str) if props_str else {}

        row = {"Language": translate_lang(lang)}

        for key in keys:
            val = props_json.get(key.lower(), {}).get("value", "")
            if isinstance(val, list):
                val = ", ".join([item.get("name", "") for item in val])


            row[key] = val

        rows.append(row)

    df = pd.DataFrame(rows)

    if request.args.get("json", "false").lower() == "true":

        return extended_jsonify({
            "data": json.loads(df.to_json(orient='records', force_ascii=False)),
        })
    else:
        filename = "custom_props_bilingual.csv"
        filepath = os.path.join(os.getcwd(), filename)
        df.to_csv(filepath, index=False)
        return send_file(filepath, as_attachment=True)

@app.route('/prueba-2', methods=['POST'])
@produces("JSON")
@consumes("application/json")
def prueba_2():
    data = request.get_json()
    url = data.get("url", "")

    parsed_url = urlparse(url)
    hostname   = parsed_url.hostname or ""
    path       = parsed_url.path.lower()

    if "jumbocolombia.com" not in hostname:
        return extended_jsonify({
            "error": "Invalid domain, only jumbocolombia.com is supported"
        }), 400

    keywords = ["enlatados", "harinas", "chocolates", "aceite"]

    key = next((k for k in keywords if k in path), None)

    if not key:
        return extended_jsonify({
            "error": "No valid category found in URL"
        }), 400

    values    = r.lrange(key, 0, 14) or []
    
    raw_timestamp = r.get(f"{key}:timestamp")

    if raw_timestamp:
        timestamp = datetime.utcfromtimestamp(int(raw_timestamp)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        timestamp = "no timestamp"

    return extended_jsonify({
        "data": {
            "products" : values,
            "timestamp": timestamp,
        }
    })



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
