# Legal-Advice-AI-NVIDIA-Nemotron-API-

To run the "main.py" pythin file, You will first need to install a few libraries mentioned in the "requirements.txt"

open command prompt on your pc and type

```pip install -r requirements.txt```

all the non-built in requirements will be installed make sure you have python installed on your system

Additionaly you will need to generate an API key from NVIDIA website and paste it in the code.

[Click Here](https://build.nvidia.com/models) to visit the available models offered by NVIDIA and select any nemotron model and generate the API Key and change the following in the code as per the given code on the screen in NVIDIA Page except the content field.

```
completion = client.chat.completions.create(
  model="nvidia/llama-3.3-nemotron-super-49b-v1",
  messages=[{"role":"system","content":<SAME-AS-IN-CURRENT-CODE>}],
  temperature= <AS-PER-THE-CODE>,
  top_p= <AS-PER-THE-CODE>,
  max_tokens= <AS-PER-THE-CODE>,
  frequency_penalty= <AS-PER-THE-CODE>,
  presence_penalty= <AS-PER-THE-CODE>,
  stream= <AS-PER-THE-CODE>
)
```
