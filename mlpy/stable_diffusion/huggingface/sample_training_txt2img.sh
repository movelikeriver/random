set -euv

# TODO: how to fine tune?

# export MODEL_NAME="CompVis/stable-diffusion-v1-4"
# moved from ~/.cache/huggingface/.....
export MODEL_NAME='sd-compvis-model'

export dataset_name="lambdalabs/pokemon-blip-captions"


# if GPU, set --mixed_precision="fp16"
#
# training param to tune
#  --max_train_steps=15000 \
#  --learning_rate=1e-05 \

accelerate launch --mixed_precision="no"  train_text_to_image.py \
  --pretrained_model_name_or_path=$MODEL_NAME \
  --dataset_name=$dataset_name \
  --use_ema \
  --resolution=512 --center_crop --random_flip \
  --train_batch_size=1 \
  --gradient_accumulation_steps=4 \
  --gradient_checkpointing \
  --max_train_steps=10 \
  --learning_rate=1e-03 \
  --max_grad_norm=1 \
  --lr_scheduler="constant" --lr_warmup_steps=0 \
  --output_dir="sd-pokemon-model" 
