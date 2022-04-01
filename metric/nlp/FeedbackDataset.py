class FeedbackDataset(Dataset):
    def __init__(self,
                 csv_file,
                 text_dir,
                 tokenizer,
                 mask_prob=0.0,
                 mask_ratio=0.0):
        self.df = pd.read_csv(csv_file)
        self.samples = list(self.df.groupby('id'))
        self.text_dir = text_dir
        self.tokenizer = tokenizer
        print(f'Loaded {len(self)} samples.')

        assert 0 <= mask_prob <= 1
        assert 0 <= mask_ratio <= 1
        self.mask_prob = mask_prob
        self.mask_ratio = mask_ratio

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        text_id, df = self.samples[index]
        text_path = osp.join(self.text_dir, f'{text_id}.txt')

        with open(text_path) as f:
            text = f.read().rstrip()

        tokens = self.tokenizer(text, return_offsets_mapping=True)
        input_ids = torch.LongTensor(tokens['input_ids'])
        attention_mask = torch.LongTensor(tokens['attention_mask'])
        offset_mapping = np.array(tokens['offset_mapping'])
        offset_mapping = self.strip_offset_mapping(text, offset_mapping)
        num_tokens = len(input_ids)

        # token slices of words
        woff = self.get_word_offsets(text)
        toff = offset_mapping
        wx1, wx2 = woff.T
        tx1, tx2 = toff.T
        ix1 = np.maximum(wx1[..., None], tx1[None, ...])
        ix2 = np.minimum(wx2[..., None], tx2[None, ...])
        ux1 = np.minimum(wx1[..., None], tx1[None, ...])
        ux2 = np.maximum(wx2[..., None], tx2[None, ...])
        ious = (ix2 - ix1).clip(min=0) / (ux2 - ux1 + 1e-12)
        assert (ious > 0).any(-1).all()

        word_boxes = []
        for row in ious:
            inds = row.nonzero()[0]
            word_boxes.append([inds[0], 0, inds[-1] + 1, 1])
        word_boxes = torch.FloatTensor(word_boxes)

        # word slices of ground truth spans
        gt_spans = []
        for _, row in df.iterrows():
                      winds = row['predictionstring'].split()
            start = int(winds[0])
            end = int(winds[-1])
            span_label = TYPE2LABEL[row['discourse_type']]
            gt_spans.append([start, end + 1, span_label])
        gt_spans = torch.LongTensor(gt_spans)

        # random mask augmentation
        if np.random.random() < self.mask_prob:
            all_inds = np.arange(1, len(input_ids) - 1)
            n_mask = max(int(len(all_inds) * self.mask_ratio), 1)
            np.random.shuffle(all_inds)
            mask_inds = all_inds[:n_mask]
            input_ids[mask_inds] = self.tokenizer.mask_token_id

        return dict(text=text,
                    text_id=text_id,
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    word_boxes=word_boxes,
                    gt_spans=gt_spans)

    def strip_offset_mapping(self, text, offset_mapping):
        ret = []
        for start, end in offset_mapping:
            match = list(re.finditer('\S+', text[start:end]))
            if len(match) == 0:
                ret.append((start, end))
                        else:
                span_start, span_end = match[0].span()
                ret.append((start + span_start, start + span_end))
        return np.array(ret)

    def get_word_offsets(self, text):
        matches = re.finditer("\S+", text)
        spans = []
        words = []
        for match in matches:
            span = match.span()
            word = match.group()
            spans.append(span)
            words.append(word)
        assert tuple(words) == tuple(text.split())
        return np.array(spans)
      
class CustomCollator(object):
    def __init__(self, tokenizer, model):
        self.pad_token_id = tokenizer.pad_token_id
        if hasattr(model.config, 'attention_window'):
            # For longformer
            # https://github.com/huggingface/transformers/blob/v4.17.0/src/transformers/models/longformer/modeling_longformer.py#L1548
            self.attention_window = (model.config.attention_window
                                     if isinstance(
                                         model.config.attention_window, int)
                                     else max(model.config.attention_window))
        else:
            self.attention_window = None

    def __call__(self, samples):
        batch_size = len(samples)
        assert batch_size == 1, f'Only batch_size=1 supported, got batch_size={batch_size}.'

        sample = samples[0]

        max_seq_length = len(sample['input_ids'])
        if self.attention_window is not None:
            attention_window = self.attention_window
            padded_length = (attention_window -
                             max_seq_length % attention_window
                             ) % attention_window + max_seq_length
        else:
            padded_length = max_seq_length

        input_shape = (1, padded_length)
        input_ids = torch.full(input_shape,
                                                              self.pad_token_id,
                               dtype=torch.long)
        attention_mask = torch.zeros(input_shape, dtype=torch.long)

        seq_length = len(sample['input_ids'])
        input_ids[0, :seq_length] = sample['input_ids']
        attention_mask[0, :seq_length] = sample['attention_mask']

        text_id = sample['text_id']
        text = sample['text']
        word_boxes = sample['word_boxes']
        gt_spans = sample['gt_spans']

        return dict(text_id=text_id,
                    text=text,
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    word_boxes=word_boxes,
                    gt_spans=gt_spans)





