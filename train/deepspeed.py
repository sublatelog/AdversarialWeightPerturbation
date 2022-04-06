# torch_cudaのバージョンを調節


!pip3 install git+https://github.com/huggingface/transformers

  
%%bash
git clone https://github.com/microsoft/DeepSpeed/
cd DeepSpeed
rm -rf build
time DS_BUILD_CPU_ADAM=1 DS_BUILD_FUSED_ADAM=1 pip install . --global-option="build_ext" --global-option="-j8" --no-cache -v --disable-pip-version-check 2>&1 | tee build.log
  
  
!ds_report


# https://www.deepspeed.ai/docs/config-json/
ds_config_dict = {
    "fp16": {
        "enabled": "auto",
        "loss_scale": 0,
        "loss_scale_window": 1000,
        "initial_scale_power": 16,
        "hysteresis": 2,
        "min_loss_scale": 1
    },


    "optimizer": {
        "type": "AdamW",
        "params": {
            "lr": "auto",
            "betas": "auto",
            "eps": "auto",
            "weight_decay": "auto"
        }
    },

    "scheduler": {
        "type": "WarmupLR",
        "params": {
            "warmup_min_lr": "auto",
            "warmup_max_lr": "auto",
            "warmup_num_steps": "auto"
        }
    },

    "zero_optimization": {
        "stage": 2,
        "offload_optimizer": {
            "device": "cpu",
            "pin_memory": True
        },
        "allgather_partitions": True,
        "allgather_bucket_size": 2e8,
        "overlap_comm": True,
        "reduce_scatter": True,
        "reduce_bucket_size": 5e8,
        "contiguous_gradients": True
    },

    "gradient_accumulation_steps": "auto",
    "gradient_clipping": "auto",
    # "steps_per_print": 2000,
    "train_batch_size": "auto",
    # "train_micro_batch_size_per_gpu": "auto",
    "wall_clock_breakdown": False,
    "dump_state": False,
}

import json
with open('/content/ds_config_dict.json', 'w') as f:
    json.dump(ds_config_dict, f, indent=2, ensure_ascii=False)


training_args = TrainingArguments(
    output_dir="/content/drive/MyDrive/kaggle/Feedback/models/domain_adaptation",
    evaluation_strategy = "epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    logging_steps=300,
    save_steps=300,
    seed=42,
    weight_decay=0.01,
    # report_to='wandb', 
    gradient_accumulation_steps=1,
    fp16 = True,
    deepspeed="/content/ds_config_dict.json"
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['val'],
    data_collator=data_collator,
    tokenizer=tokenizer,  # This tokenizer has new tokens    
)


trainer.train()











