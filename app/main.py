# text preprocessing modules
import re  # regular expression
import uvicorn
from csv import writer
from datetime import datetime
from typing import Optional
from fastapi import FastAPI
import torch

# from transformers import AutoModel, AutoTokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# pip list --format=freeze > requirements.txt

app = FastAPI(
    title="'How To' Answer Generator",
    description="A simple API using GPT-2 fine-tuned model for answering 'How to' questions",
    version="beta 0.1",
)

# # Download models from Hugging face Hub
# model = AutoModel.from_pretrained("plasticfruits/gpt2-finetuned-how-to-qa")
# tokenizer = AutoTokenizer.from_pretrained("plasticfruits/gpt2-finetuned-how-to-qa")

# load the sentiment model from subfolder
path = "./model"
model = GPT2LMHeadModel.from_pretrained(path)
tokenizer = GPT2Tokenizer.from_pretrained(path)


def clean_response(user_prompt, response):
    """
    """
    response = re.sub("(?<=\.)[^.]*$", "", response)  # finish at last sentence dot
    response = (
        response.replace("[WP]", "").replace(user_prompt, "").replace("[RESPONSE]", "")
    )
    response = response.lstrip()
    return response


def save_qa_history(user_prompt, response, length):
    """
    """
    dt = datetime.now()
    history_list = [user_prompt, response, length, dt]
    with open("./history/qa_history.csv", "a", newline="") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(history_list)
        f_object.close()


### TODOS
#
# Convert to post request?
#


@app.get("/answers")
def generate_response(user_prompt: str, length: Optional[int] = 300):
    """
    """
    prompt = f"<|startoftext|>[WP] {user_prompt} [RESPONSE]"
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    sample_outputs = model.generate(
        generated,
        do_sample=True,
        top_k=50,
        max_length=length,
        top_p=0.95,
        num_return_sequences=1,
    )
    data = []
    for i, sample_output in enumerate(sample_outputs):
        response = clean_response(
            user_prompt, tokenizer.decode(sample_output, skip_special_tokens=True)
        )
        response_dict = {"key": i, "response": response}
        save_qa_history(user_prompt, response, length)
        data.append(response_dict)
    # output = tokenizer.decode(sample_outputs, skip_special_tokens=True)
    # output = tokenizer.decode(sample_output, skip_special_tokens=True)
    return {"data": data[0]["response"]}
