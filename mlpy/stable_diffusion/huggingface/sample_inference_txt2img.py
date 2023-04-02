"""
usage:
python sample_inference_txt2img.py

sample code from https://github.com/huggingface/diffusers

one time setup:

conda create -n sd2 pytorch==1.12.1 torchvision==0.13.1
conda activate sd2
# conda install -c conda-forge diffusers==0.12.1    <-- conda version
# conda install -c conda-forge transformers==4.19.2   <-- one repo needs this version
conda install -c conda-forge transformers==4.27.4
conda install -c conda-forge accelerate==0.18.0
conda install -c conda-forge datasets==2.11.0
conda install -c conda-forge ftfy==6.1.1
pip install invisible-watermark


for training, need to install `diffusers` from local:
# https://huggingface.co/docs/diffusers/installation#install-from-source
"""

import torch
from diffusers import DiffusionPipeline


load_from_local = False

if not load_from_local:
    # option-1: download from Hub
    # will download to ~/.cache/huggingface/...
    pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")

else:
    # option-2: load from local path
    model_path = "path_to_saved_model"
    pipe = DiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)


pipe = pipe.to("cpu")
# Recommended if your computer has < 64 GB of RAM
pipe.enable_attention_slicing()

# Note: maximum sequence length for this model
# promt = "yoda"
prompt = "beautiful elven woman sitting in a white elven city, (full body), (blush), (sitting on stone staircase), pinup pose, (world of warcraft blood elf), (cosplay wig), (medium blonde hair:1.3), (light blue eyes:1.2), ((red, and gold elf minidress)), intricate elven dress"


print(prompt)

# First-time "warmup" pass (see explanation above)
_ = pipe(prompt, num_inference_steps=1)

# Results match those from the CPU device after the warmup pass.
img_list = pipe(prompt).images

print(len(img_list))
image = img_list[0]

output_fn = 'output1.png'
image.save(output_fn)
print(f"file saved in {output_fn}")
