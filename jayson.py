import json
import typing as t

import jsonref

from validator import Endpoint, body


def extract_get_params(get_value):
    params_list = []
    params = get_value.get("parameters", [])

    for param in params:
        params_list.append(
            body(
                required=param["required"],
                type=param["schema"]["type"],
                param_name=param["name"],
            )
        )
    return params_list


def extract_post_params(post_value):
    params_list = []

    # Extract parameters from the 'parameters' section
    if "parameters" in post_value:
        for param in post_value["parameters"]:
            params_list.append(
                body(
                    required=param["required"],
                    type=param["schema"]["type"],
                    param_name=param["name"],
                )
            )

    # Extract parameters from the 'requestBody' section
    content_types = ["application/json", "application/x-www-form-urlencoded"]
    if "requestBody" in post_value and "content" in post_value["requestBody"]:
        for content_type in content_types:
            if content_type in post_value["requestBody"]["content"]:
                schema = post_value["requestBody"]["content"][content_type]["schema"]
                if schema.get("type") == "array":
                    schema = schema["items"]

                for param_name, param_properties in schema.get(
                    "properties", {}
                ).items():
                    params_list.append(
                        body(
                            required=param_name in schema.get("required", []),
                            type=param_properties["type"],
                            param_name=param_name,
                        )
                    )
    return params_list


def extract_delete_params(delete_value):
    params_list = []
    params = delete_value.get("parameters", [])

    for param in params:
        params_list.append(
            body(
                required=param["required"],
                type=param["schema"]["type"],
                param_name=param["name"],
            )
        )
    return params_list


def extract_put_params(put_value):
    params_list = []

    # Extract parameters from the 'parameters' section
    if "parameters" in put_value:
        for param in put_value["parameters"]:
            params_list.append(
                body(
                    required=param["required"],
                    type=param["schema"]["type"],
                    param_name=param["name"],
                )
            )

    # Extract parameters from the 'requestBody' section
    content_types = ["application/json", "application/x-www-form-urlencoded"]
    if "requestBody" in put_value and "content" in put_value["requestBody"]:
        for content_type in content_types:
            if content_type in put_value["requestBody"]["content"]:
                schema = put_value["requestBody"]["content"][content_type]["schema"]
                if schema.get("type") == "array":
                    schema = schema["items"]

                for param_name, param_properties in schema.get(
                    "properties", {}
                ).items():
                    params_list.append(
                        body(
                            required=param_name in schema.get("required", []),
                            type=param_properties["type"],
                            param_name=param_name,
                        )
                    )
    return params_list


# update main function
def main():
    endpoints = {}
    #! load source file
    #! load source file
    #! load source file
    #! load source file
    with open("source.json", "r") as source_file:
        source_data = json.load(source_file)

    source_data = jsonref.loads(json.dumps(source_data))

    for path, properties in source_data["paths"].items():
        for method, details in properties.items():
            method_params: t.List[body] = []
            if method == "get":
                method_params = extract_get_params(details)
            elif method == "post":
                method_params = extract_post_params(details)
            elif method == "delete":
                method_params = extract_delete_params(details)
            elif method == "put":
                method_params = extract_put_params(details)
            endpoint_key = f"{details['summary']}({method})"
            # get succesful responses from the 'responses' section
            successful_responses_example = None
            if "responses" in details:
                for response_code, response_details in details["responses"].items():
                    if response_code.startswith("2") and "content" in response_details:
                        properties = response_details["content"]["application/json"][
                            "schema"
                        ].get("properties", {})
                        successful_responses_example = {}
                        for key, property in properties.items():
                            if "default" in property:
                                successful_responses_example[key] = property["default"]
                            else:
                                successful_responses_example[key] = property["type"]
                        successful_responses_example = json.dumps(
                            successful_responses_example, indent=4
                        )
                        break
            print(successful_responses_example)
            str((successful_responses_example))
            request = {}
            for param in method_params:
                request[param.param_name] = (
                    "*" + param.type if param.required else param.type
                )
            request = json.dumps(request, indent=4)

            endpoints[endpoint_key] = Endpoint(
                type=method.upper(),
                body=method_params,
                url=path,
                response=successful_responses_example,
                request=request,
            )
    return endpoints


if __name__ == "__main__":
    endpoints = main()
    print(endpoints)
