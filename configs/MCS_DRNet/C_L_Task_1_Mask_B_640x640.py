_base_ = [
    '../_base_/models/upernet_convnext.py',
    '../_base_/datasets/DRAC2022_Task_1_Mask_B_640x640.py', '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_130k.py'
]
crop_size = (640, 640)
checkpoint_file = 'https://download.openmmlab.com/mmclassification/v0/convnext/downstream/convnext-large_3rdparty_in21k_20220301-e6e0ea0a.pth'  # noqa
model = dict(
    backbone=dict(
        type='mmcls.ConvNeXt',
        arch='large',
        out_indices=[0, 1, 2, 3],
        drop_path_rate=0.4,
        layer_scale_init_value=1.0,
        gap_before_final_norm=False,
        init_cfg=dict(
            type='Pretrained', checkpoint=checkpoint_file,
            prefix='backbone.')),
    decode_head=dict(
        in_channels=[192, 384, 768, 1536],
        num_classes=10,
    ),
    auxiliary_head=dict(in_channels=768, num_classes=10),
    test_cfg=dict(mode='slide', crop_size=crop_size, stride=(426, 426)),
)

optimizer = dict(
    constructor='LearningRateDecayOptimizerConstructor',
    _delete_=True,
    type='AdamW',
    lr=0.00001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg={
        'decay_rate': 0.9,
        'decay_type': 'stage_wise',
        'num_layers': 12
    })

lr_config = dict(
    _delete_=True,
    policy='poly',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=1e-6,
    power=1.0,
    min_lr=0.0,
    by_epoch=False)

# By default, models are trained on 8 GPUs with 2 images per GPU
data = dict(samples_per_gpu=2)
# fp16 settings
optimizer_config = dict(type='Fp16OptimizerHook', loss_scale='dynamic')
# fp16 placeholder
fp16 = dict()
