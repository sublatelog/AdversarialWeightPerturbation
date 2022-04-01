from mmcv.runner import BaseModule, build_runner, build_optimizer










runner = dict(type='EpochBasedRunner', max_epochs=1 if debug else 6)



runner = build_runner(cfg.runner,
                      default_args=dict(model=detector,
                                        batch_processor=None,
                                        optimizer=optimizer,
                                        work_dir=cfg.work_dir,
                                        logger=logger,
                                        meta=None))
runner.timestamp = timestamp
runner.register_training_hooks(cfg.lr_config,
                               cfg.optimizer_config,
                               cfg.checkpoint_config,
                               cfg.log_config,
                               cfg.get('momentum_config', None),
                               custom_hooks_config=cfg.get(
                                   'custom_hooks', None))



runner.run([train_dl], [('train', 1)])
