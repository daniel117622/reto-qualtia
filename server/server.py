from flask import Flask, jsonify, request, send_file
import requests
import json
import pandas as pd
import os

from typing import Any, Dict, Callable
from utils.translations import  translate_lang , translate_cop_to_mxn
from utils.return_declarations import produces , consumes
from schemas.responses import Link, ProduceType , ConsumeType

from graphql_templates.templates import GraphQLTemplate


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
        consumes = [ConsumeType(ct) for ct in getattr(view_func, '_consume', [])]

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

@app.route('/prueba-2', methods=['GET'])
@produces("JSON")
@consumes("application/json")
def prueba_2():
    # Esto es común para cualquier petición
    store_url = "https://www.jumbocolombia.com/api/segments"
    session = requests.Session()

    session.headers = {
        "User-Agent"     : "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept"         : "*/*",
        "Accept-Language": "es-CO,es;q=0.9",
    }

    session.get(store_url)

    # Es necesario evaluar que zona scrapear. Solo para usar el template.

    # Esto se realizará con un servicio de SELENIUM + REDIS

    return extended_jsonify({"data" : []})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
