import requests
import json

url = "http://localhost:11434/api/generate"
data = {
    "model": "llama3.2",
    "prompt": "tell me a short story and make it funny.",
}

response = requests.post(
    url, json=data, stream=True
)  # remove the stream=True to get the full response


# check the response status
if response.status_code == 200:
    print("Generated Text:", end=" ", flush=True)
    ### Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            ### Decode the line and parse the JSON
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)
            # ==> {'model': 'llama3.2', 'created_at': '2025-01-08T01:51:41.097773176Z', 'response': '', 'done': True, 'done_reason': 'stop', 'context': [111, 222....], 'total_duration': 2161786470, 'load_duration': 21603705, 'prompt_eval_count': 35, 'prompt_eval_duration': 3000000, 'eval_count': 330, 'eval_duration': 2135000000}

            ### Get the text from the response
            generated_text = result.get("response", "")
            print(generated_text, end="", flush=True)
else:
    print("Error:", response.status_code, response.text)
