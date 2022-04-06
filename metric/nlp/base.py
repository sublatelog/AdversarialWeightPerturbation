
!pip3 install git+https://github.com/huggingface/transformers



arch = {
        'allenai/longformer-base-4096',
        'google/bigbird-roberta-base',
        }



self.model = AutoModelForTokenClassification.from_pretrained(
            arch,
            num_labels=1 + 2 + num_classes,
            local_files_only=local_files_only)
if with_cp:
    self.model.gradient_checkpointing_enable()

self.tokenizer = AutoTokenizer.from_pretrained(arch, local_files_only=local_files_only)
