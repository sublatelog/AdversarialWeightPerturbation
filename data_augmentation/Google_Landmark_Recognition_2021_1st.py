cfg.train_aug = A.Compose([
                          A.HorizontalFlip(p=0.5),
                          A.ImageCompression(quality_lower=99, quality_upper=100),
                          A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=10, border_mode=0, p=0.7),
                          A.Resize(image_size, image_size),
                          A.Cutout(max_h_size=int(image_size * 0.4), max_w_size=int(image_size * 0.4), num_holes=1, p=0.5),
                          ])

cfg.val_aug = A.Compose([
                        A.Resize(image_size, image_size),
                        ])
