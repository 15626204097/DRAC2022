# DRAC2022 (MICCAI2022) DR Segmentation

`This project is still under construction` 

<!-- [ABSTRACT] -->

The code is based on [MMSelfsup v0.10.0](https://github.com/open-mmlab/mmselfsup/tree/v0.10.0) and [MMSegmentaion v0.24.1](https://github.com/open-mmlab/mmsegmentation/tree/v0.24.1).
# Stage I: Pre-task training

The pre-training environment is configured as follows:
```shell
pip install openmim
mim install mmcv-full==1.6.0
pip install mmcv-full -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.10/index.html
cd ./Task1/Se_sup/
pip install -e .
```
Note: please configure the lab environment before proceeding to the following steps. If you encounter problems with environment configuration, please refer to [MMSelfsup v0.10.0](https://github.com/open-mmlab/mmselfsup/tree/v0.10.0) .

Then, download the DRAC Task 3 dataset and unzip it. Save the data in the following directory:

```none
├── Se_sup
│   ├── C._Diabetic_Retinopathy_Grading
│   │   ├── 1._Original_Images
│   │   │   ├── a._Training_Set
│   │   │   │   ├── 001.png
│   │   │   │   ├── ...
│   │   ├── 2._Groundtruths
│   │   │   ├── a._DRAC2022_Diabetic_Retinopathy_Grading_Training_Labels.csv
```

In directory `/DRAC2022/Se_sup/`, by using the `pretrain_data_processing.py`, 

```shell
python tools/pretrain_data_processing.py
```
the processing data will be saved in the following directory:

```none
├── Se_sup
│   ├── Data
│   │   ├── Original_Images
│   │   │   ├── Training_Set
│   │   │   │   ├── 001.jpg
│   │   │   │   ├── ...
│   │   ├── Pretrained_files.txt
```

Next, we run the following statement to begin our pre-training：

```shell
python tools/train.py configs/selfsup/mae/mae.py
```

After the above statement runs, the pre-trained MAE model will be saved in the following directory:

```none
├── Se_sup
│   ├── work_dirs
│   │   ├── mae
│   │   │   ├── epoch_1600.pth
```

Then, please run the following shell statement in the `Se_sup` directory to obtain the backbone of pre-trained MAE-ViT.

```shell
python tools/model_converters/extract_backbone_weights.py work_dirs/mae/epoch_1600.pth work_dirs/mae/pretrain_backbone_1600.pth
```

After running, the model is saved in the following directory：

```none
├── Se_sup
│   ├── work_dirs
│   │   ├── mae
│   │   │   ├── pretrain_backbone_1600.pth
```

# Stage II: Semantic segmentation

## Semantic segmentation environment configuration

```shell
pip install torch==1.12.0 torchvision --extra-index-url https://download.pytorch.org/whl/cu113
pip install openmim
mim install mmcv-full==1.6.0
cd ./Task1
pip install -e .
```
Note: please configure the lab environment before proceeding to the following steps. If you encounter problems with environment configuration, please refer to [MMSegmentaion v0.24.1](https://github.com/open-mmlab/mmsegmentation/tree/v0.24.1).

## Semantic segmentation data preprocessing

For Mask A and B, we provide the data preprocessing file `Mask_A_Data_preprocess.py` and `Mask_B_Data_preprocess.py` to preprocess the original data from DRAC2022 Task 1. Before you do that, you need to downlaod the Task 1 data. Then, unzip and put into the folloing directory:

```none
├── DRAC2022_dataset
│   ├── A._Segmentation
│   │   ├── 1._Original Images
│   │   │   ├── a._Training Set
│   │   │   │   ├── 065.png
│   │   │   │   ├── ...
│   │   ├── 2._Groundtruths
│   │   │   ├── a._Training Set
│   │   │   │   ├── 1._Intraretinal Microvascular Abnormalities
│   │   │   │   │   ├── 082.png
│   │   │   │   │   ├── ...
│   │   │   │   ├── 2._Nonperfusion Areas
│   │   │   │   │   ├── 065.png
│   │   │   │   │   ├── ...
│   │   │   │   ├── 3._Neovascularization
│   │   │   │   │   ├── 082.png
│   │   │   │   │   ├── ...
```

For example, for Mask A usage:

```shell
python tools/Mask_A_Data_preprocess.py
```

## The data directory for the semantic segmentation task

The data for this directory can be generated by the `Mask_A_Data_preprocess.py` and `Mask_B_Data_preprocess.py` file.

```none
├── DRAC2022_dataset
│   ├── A. Segmentation
│   │   ├── ...
│   ├── Segmentation
│   │   ├── Training
│   │   │   ├── A
│   │   │   │   ├── 640
│   │   │   │   │   ├── Masks
│   │   │   │   │   │   ├── 082.png
│   │   │   │   │   │   ├── ...
│   │   │   │   │   ├── Original_images
│   │   │   │   │   │   ├── 082.jpg
│   │   │   │   │   │   ├── ...
│   │   │   │   ├── 1024
│   │   │   │   │   ├── Masks
│   │   │   │   │   │   ├── 082.png
│   │   │   │   │   │   ├── ...
│   │   │   │   │   ├── Original_images
│   │   │   │   │   │   ├── 082.jpg
│   │   │   │   │   │   ├── ...
│   │   │   ├── B
│   │   │   │   ├── 640
│   │   │   │   │   ├── Masks
│   │   │   │   │   │   ├── 065.png
│   │   │   │   │   │   ├── ...
│   │   │   │   │   ├── Original_images
│   │   │   │   │   │   ├── 065.jpg
│   │   │   │   │   │   ├── ...
│   │   │   │   ├── 1024
│   │   │   │   │   ├── Masks
│   │   │   │   │   │   ├── 065.png
│   │   │   │   │   │   ├── ...
│   │   │   │   │   ├── Original_images
│   │   │   │   │   │   ├── 065.jpg
│   │   │   │   │   │   ├── ...
```
Due to the limited data available for this contest, we did not set the validation set.


## Algorithm training phase
In order to save the running resources of GPU, we train each sub-algorithm separately.

Running the example script of different sub-algorithm in training Mask A:
```shell
python tools/train.py configs/MCS_DRNet/(sub-algorithm)_Task_1_Mask_A_(640x640/1024x1024).py
```
The sub-algorithm contains three values: `M`, `C`, and `S`. The resolution `1024x1024` is unique to the `S` algorithm.
For example, we want to run the subalgorithm `M`.

For example:
```shell
python tools/train.py configs/MCS_DRNet/M_Task_1_Mask_A_640x640.py
```
Running the example script of sub-algorithm C in training Mask B:

For example:
```shell
python tools/train.py configs/MCS_DRNet/C_Task_1_Mask_B_640x640.py
```
# Testing phase

For Mask `A` and `B` prediction, we provide the data processing file `Test_Data_process.py` to process the original test data from DRAC2022 Task 1. Before you do that, you need to downlaod the Task 1 test data. Then, unzip and put into the folloing directory:

```none
├── DRAC2022_dataset
│   ├── A. Segmentation
│   │   ├── ...
│   ├── Segmentation
│   │   ├── ...
│   ├── Test_Data
│   │   ├── Original_Images
│   │   │   ├── 086.png
│   │   │   ├── ...
```
For example:
```shell
python tools/Test_Data_process.py
```

The data for this directory can be generated by the `Test_Data_process.py` file.

```none
├── DRAC2022_dataset
│   ├── A. Segmentation
│   │   ├── ...
│   ├── Segmentation
│   │   ├── ...
│   ├── Test_Data
│   │   ├── Original_Images
│   │   │   ├── 086.png
│   │   │   ├── ...
│   │   ├── Horizontal_flip
│   │   │   ├── 086.png
│   │   │   ├── ...
│   │   ├── Vertical_flip
│   │   │   ├── 086.png
│   │   │   ├── ...
│   │   ├── R90
│   │   │   ├── 086.png
│   │   │   ├── ...
│   │   ├── R180
│   │   │   ├── 086.png
│   │   │   ├── ...
│   │   ├── R270
│   │   │   ├── 086.png
│   │   │   ├── ...
```

## MCS-DRNet v2

For the tests of Mask A and B, we provide the test file `MCS_DRNet_Task_1_Mask_A_1536x1536.py` and `MCS_DRNet_Task_1_Mask_B_1536x1536.py`(The document will soon be published).

For mask A, usage:
```shell
python tools/MCS_DRNet_Task_1_Mask_A_1536x1536.py --load-from-checkpoint-M ${file_dir} --load-from-checkpoint-C ${file_dir} --load-from-checkpoint-S ${file_dir} --data-dir ${file_dir} --output-data-dir ${file_dir} 
```
For mask B, usage:
```shell
python tools/MCS_DRNet_Task_1_Mask_B_1536x1536.py --load-from-checkpoint-M ${file_dir} --load-from-checkpoint-C ${file_dir} --load-from-checkpoint-S ${file_dir} --data-dir ${file_dir} --output-data-dir ${file_dir} 
```
`--load-from-checkpoint-M`: path to store checkpoints of the pretrained model MAE \
`--load-from-checkpoint-C`: path to store the checkpoints of the pretrained model ConvNeXt \
`--load-from-checkpoint-S`: path to store checkpoints of the pretrained model SegFormer \
`--data-dir`: path to test image \
`--output-data-dir`: output path of test segmentation results

## Contact
If you have any question, please feel free to contact me via tan.joey@student.upm.edu.my

## Acknowledgment

Our implementation is mainly based on [MMSelfsup](https://github.com/open-mmlab/mmselfsup/tree/v0.10.0), [MMsegmentaion](https://github.com/open-mmlab/mmsegmentation/tree/v0.24.1), [MAE](https://github.com/facebookresearch/mae),      [Segformer](https://github.com/NVlabs/SegFormer) and [ConvNeXt](https://github.com/facebookresearch/ConvNeXt). Thanks for their authors.

## LICENSE

This repo is under the Apache-2.0 license. For commercial use, please contact the authors.
