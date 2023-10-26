"""
https://github.com/ggerganov/llama.cpp

download model in llama repo, then go to llama.cpp repo.

$ ls -lh llama-2-13b
total 50859416
154B Jul 14 16:29 checklist.chk
12G Jul 13 16:12 consolidated.00.pth
12G Jul 13 16:12 consolidated.01.pth
102B Jul 13 16:12 params.json


one time setup:
LLAMA_METAL=1 make
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

convert the model
python3 convert.py ../llama/llama-2-13b

24G Oct 25 22:17 ggml-model-f16.gguf

./quantize ../llama/llama-2-13b/ggml-model-f16.gguf ../llama/llama-2-13b/ggml-model-q4_0.gguf q4_0

6.9G Oct 25 22:19 ggml-model-q4_0.gguf


now, you can run this file!!!

this works well in llama 7B, but not 13B.

you can also try `examples/chat-13B.sh` by using the model path above.

"""

import sys

from llama_cpp import Llama


def get_text():
    """can suppor multiple lines."""

    buffer = []
    while True:
        line = sys.stdin.readline().rstrip('\n')
        if line == '<end>':
            break
        buffer.append(line)

    return ' '.join(buffer)



model_path = '../llama/llama-2-13b/ggml-model-q4_0.gguf'
model = Llama(model_path = model_path,
              n_ctx = 2048,            # context window size
              n_gpu_layers = 1,        # enable GPU
              use_mlock = True)        # enable memory lock so not swap



print('\n======= ready? go! =======\n')

while True:
    print('\n== input until <end>:\n')
    text = get_text()
    if text == 'qqq':
        break

    print(f'\n====== Input ======\n{text}\n')

    output = model(prompt = text, max_tokens = 1200, temperature = 0.2)
    print(f'\n====== Output ======\n{output}\n')

print('\nBye!!\n')
