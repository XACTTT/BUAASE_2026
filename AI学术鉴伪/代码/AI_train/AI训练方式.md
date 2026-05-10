# AI模型训练与评测方式

## URN训练代码位置

URN训练代码目录：

`/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN`

当前已接入 `rsiil` 生成的数据集 `dsiid_urn`，默认训练/测试清单为：

- `dsiid_urn_train`
- `dsiid_urn_test`

此外，数据生成脚本现在还会自动导出用于复现服务侧 5 个 URN 权重的专项清单：

- `dsiid_urn_coarse_v2_train`
- `dsiid_urn_coarse_v2_test`
- `dsiid_urn_blurring_train`
- `dsiid_urn_blurring_test`
- `dsiid_urn_brute_force_train`
- `dsiid_urn_brute_force_test`
- `dsiid_urn_contrast_train`
- `dsiid_urn_contrast_test`
- `dsiid_urn_inpainting_train`
- `dsiid_urn_inpainting_test`

对应 manifest 链接位于：

- `/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_train.txt`
- `/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_test.txt`

这两个链接实际指向：

- `/mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_train.txt`
- `/mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_test.txt`

## 训练启动

进入目录：

```shell
cd /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN
```

先做一次启动自检：

```shell
conda run -n bert python train.py --smoke-test --gpu 0
```

说明：

- 该命令会加载模型
- 读取 `dsiid_urn_train/test`
- 拉起一个 train batch 和一个 test batch
- 执行一次前向与 loss 计算后退出

正式训练：

```shell
conda run -n bert python train.py --gpu 0
```

常用写法：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --epochs 100 \
  --batch-size 64 \
  --train-set dsiid_urn_train \
  --test-set dsiid_urn_test
```

如果要显式指定 checkpoint 输出目录：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_train \
  --test-set dsiid_urn_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_default
```

## 生成五种数据集

以复现服务侧 5 个 URN 权重为目标，建议先生成一版完整数据集：

```shell
cd /mnt/data14/ccy/Bert/rsiil

/mnt/data14/ccy/pip_packs/miniconda3/envs/rsiil/bin/python build_urn_academic_forgery_dataset.py \
  --src /mnt/data14/ccy/Bert/datasets/dsiid/artificial_forgery_src_data/srcDataset \
  --out /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5 \
  --templates /mnt/data14/ccy/Bert/rsiil/templates_json \
  --service-targets coarse_v2 blurring brute_force contrast inpainting \
  --simple-samples-per-type 2500 \
  --compound-samples-per-type 4500 \
  --workers 0 \
  --cv2-threads 1 \
  --tasks-per-worker 2 \
  --train-ratio 0.8 \
  --seed 42 \
  --n-objects 1
```

生成完成后，`manifests/` 下会同时得到：

- 通用清单：`dsiid_urn_train/test.txt`
- 服务复现清单：
  - `dsiid_urn_coarse_v2_train/test.txt`
  - `dsiid_urn_blurring_train/test.txt`
  - `dsiid_urn_brute_force_train/test.txt`
  - `dsiid_urn_contrast_train/test.txt`
  - `dsiid_urn_inpainting_train/test.txt`

说明：

- `--service-targets` 会自动展开每个服务模型所需的底层 RSIIL 类型
- 每个专项清单会自动包含对应的 forged 样本和配套 `pristine` 负样本
- 不需要手工再写 `splicing / copy_move / retouch_blur / cleaning_bf / cleaning_inpainting` 这些底层类型名

如果训练代码仍使用 `URN/data/` 下的 manifest，建议把这些文件链接进去，例如：

```shell
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_coarse_v2_train.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_coarse_v2_train.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_coarse_v2_test.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_coarse_v2_test.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_blurring_train.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_blurring_train.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_blurring_test.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_blurring_test.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_brute_force_train.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_brute_force_train.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_brute_force_test.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_brute_force_test.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_contrast_train.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_contrast_train.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_contrast_test.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_contrast_test.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_inpainting_train.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_inpainting_train.txt
ln -sfn /mnt/data14/ccy/Bert/datasets/dsiid_urn_service5/manifests/dsiid_urn_inpainting_test.txt /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/data/dsiid_urn_inpainting_test.txt
```

## 训练五个模型

进入目录：

```shell
cd /mnt/data14/ccy/Bert/SE/AI_train/train_code/URN
```

训练 `Coarse_v2`：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_coarse_v2_train \
  --test-set dsiid_urn_coarse_v2_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_coarse_v2
```

训练 `blurring`：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_blurring_train \
  --test-set dsiid_urn_blurring_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_blurring
```

训练 `brute_force`：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_brute_force_train \
  --test-set dsiid_urn_brute_force_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_brute_force
```

训练 `contrast`：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_contrast_train \
  --test-set dsiid_urn_contrast_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_contrast
```

训练 `inpainting`：

```shell
conda run -n bert python train.py \
  --gpu 0 \
  --train-set dsiid_urn_inpainting_train \
  --test-set dsiid_urn_inpainting_test \
  --checkpoint-dir /mnt/data14/ccy/Bert/SE/AI_train/checkpoints/urn_inpainting
```

## 训练配置位置

默认训练数据配置文件：

`/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/configs/coarse_bio_hyper_para.py`

当前默认值：

- `hp["data"]["train"] = "dsiid_urn_train"`
- `hp["data"]["test"] = "dsiid_urn_test"`

运行时也可以直接用命令行覆盖：

- `--train-set xxx`
- `--test-set xxx`
- `--epochs N`
- `--batch-size N`
- `--gpu N`

URN工程路径配置文件：

`/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/configs/config.py`

当前已经改成按当前代码仓库自动定位，不再依赖旧机器上的固定目录。

## 数据清单格式

manifest txt 文件每行格式为：

```text
图片路径 mask路径 标签
```

例如：

```text
/abs/path/image.png /abs/path/mask.png 1
```

说明：

- 标签 `0` 表示 pristine
- 标签 `1` 表示 forged
- URN 当前直接读取绝对路径

## 批量评测

当前 `eval.py` 里仍有旧的 checkpoint 路径示例，正式评测前需要手动改成目标权重路径。

启动方式：

```shell
conda run -n bert python eval.py
```

## 单图推理

当前 `infer.py` 里也保留了旧 checkpoint 路径示例，正式推理前需要手动改成目标权重路径。

启动方式：

```shell
conda run -n bert python infer.py
```

## ResNet50说明

### 下载位置

URN 会自动下载 `resnet50` 的 ImageNet 预训练权重，下载 URL 定义在：

`/mnt/data14/ccy/Bert/SE/AI_train/train_code/URN/URN/res_net.py`

默认缓存位置是 PyTorch Hub 的 checkpoint 目录，当前用户下通常是：

`/home/ccy/.cache/torch/hub/checkpoints/resnet50-19c8e357.pth`

第一次启动训练时如果本地没有该文件，会自动下载。

### 如何手动指定位置

有两种常用方式。

方式一：直接把权重文件提前放到默认缓存目录：

```shell
mkdir -p /home/ccy/.cache/torch/hub/checkpoints
cp /your/path/resnet50-19c8e357.pth /home/ccy/.cache/torch/hub/checkpoints/
```

这样 `URN` 不需要改代码，启动时会直接复用本地文件。

方式二：修改 `res_net.py` 中的加载逻辑，把：

```python
pretrain_dict = model_zoo.load_url(model_urls[backbone])
```

改成：

```python
pretrain_dict = torch.load("/your/path/resnet50-19c8e357.pth", map_location="cpu")
```

这种方式是显式指定权重文件路径，适合离线环境。

### 为什么URN需要ResNet50

URN 的 coarse 网络把 `ResNet50` 当作骨干特征提取器使用，相关代码在：

- `URN/coarse_net.py`
- `URN/res_net.py`

作用是：

- 从输入图像中提取多尺度特征
- 为后续上采样解码和伪造区域分割提供 backbone feature map
- 提供一个已经在大规模自然图像上预训练过的初始化，比随机初始化更容易收敛

简单理解：`ResNet50` 不是最终的伪造判别头，而是 URN 前半部分的视觉特征 backbone。

## URN是否原生支持多卡

当前这份训练代码不原生支持多卡训练。

判断依据：

- `train.py` 里是 `torch.cuda.set_device(args.gpu)` 后直接 `net = get_model(hp).cuda()`
- 没有 `torch.nn.DataParallel`
- 没有 `DistributedDataParallel`
- 没有分布式初始化代码
- `step.py` 和若干模块里大量直接写死了 `.cuda()`

因此当前状态是：

- 原生支持单卡训练
- 不原生支持多卡并行训练
- 如果要做多卡，需要额外改训练入口、device 放置逻辑、loss 与 batch 数据搬运逻辑

## 当前验证结果

在 `conda` 环境 `bert` 下，已经验证过：

- 可以成功加载 `dsiid_urn_train`
- 可以成功加载 `dsiid_urn_test`
- 可以完成一次 smoke test 前向

验证命令：

```shell
conda run -n bert python train.py --smoke-test --gpu 0
```
