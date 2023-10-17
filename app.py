#%%
import openai
import markdown
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    # print(data)
    api_key = data['api_key']
    model = data['model']
    prompt = data['prompt']
    text = data['text']

    split_text_chunks = re.split(r'\n[=]+\n', text)

    split_text_chunks = [chunk.strip() for chunk in split_text_chunks if chunk.strip()] 

    openai.api_key = api_key
    output_html = ""

    for chunk in split_text_chunks:
        full_prompt = f"{prompt}\n{chunk}"
        # print(chunk)
        print(full_prompt)
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_prompt},
                ])
            
            output_text = response['choices'][0]['message']['content']
            # print(output_text)
            output_html += markdown.markdown(output_text)
        except Exception as e:
            output_html += f"<p>Error in API call: {e}</p>"

    return jsonify({"output": output_html})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
