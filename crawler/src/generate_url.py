from dotenv import load_dotenv
import os 

load_dotenv()


def generate_url(combo, filter_dict, param_map, category):
    base = os.getenv("CRAWL_URL")

    query_params = {
        "gf": "M",
        "category": category,
        "size": "60",
        "caller": "CATEGORY",
        "page": "1"
    }

    # attribute 파라미터는 따로 모아서 쉼표로 병합
    attribute_values = []

    for key, value in combo.items():
        param_type = param_map.get(key)
        mapped_value = filter_dict[key][value]

        if param_type == "attribute":
            attribute_values.append(mapped_value)
        else:
            query_params[param_type] = mapped_value

    if attribute_values:
        query_params["attribute"] = ",".join(attribute_values)

    query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
    return base + query_string
