from mmcv.runner import BaseModule, build_runner, build_optimizer


start_lr_ratio = 1e-3
lr = 5e-5 * start_lr_ratio
batch_size = 16
lr_config = dict(
    policy='Cyclic',
    by_epoch=False,
    target_ratio=(1 / start_lr_ratio, 1),
    cyclic_times=runner['max_epochs'],
    step_ratio_up=0.05,
    anneal_strategy='linear',
    gamma=1,
)
optimizer = dict(
    type='AdamW',
    lr=lr,
    betas=(0.9, 0.999),
    weight_decay=0.01,
    eps=1e-8,
    paramwise_cfg=dict(norm_decay_mult=0., bias_decay_mult=0.),
)
optimizer_config = dict(type='GradientCumulativeOptimizerHook',
                        cumulative_iters=batch_size,
                        grad_clip=dict(max_norm=1.0, norm_type=2.0))


optimizer = build_optimizer(detector, cfg.optimizer)

















