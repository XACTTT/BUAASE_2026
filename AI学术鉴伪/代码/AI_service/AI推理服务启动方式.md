# AI 推理服务启动方式

本文档仅说明更新后的 AI 服务如何部署与启动。后端与 AI 服务之间的请求/返回协议见同目录下的 `后端-AI服务接口说明.md`。

## 1. 服务形态

当前推荐使用统一入口：

- `AI服务器代码/trigger_unified.py`

统一入口支持三条并行检测 pipeline：

1. 图片鉴伪
2. 结构化文本鉴伪
3. 基于 Bert/QiDeBERTa 的文本 AIGC 鉴伪

服务通过 SSH 启动，读取请求文件，执行检测，再将结果写到标准输出。

## 2. 目录准备

建议服务器目录结构如下：

```text
/mnt/data14/ccy/Bert/SE/AI_service/
├── service_code/
│   ├── trigger_unified.py
│   ├── requests/
│   │   └── request.json
│   ├── structured_models/
│   ├── test/
│   │   ├── img.zip
│   │   └── data.json
│   ├── cache/
│   └── .venv/
├── checkpoints/
│   ├── image_forgery/
│   ├── checkpoints/
│   │   └── hc3_classifier/
│   ├── weights/
│   │   ├── QiDeBERTa-base/
│   │   └── QiDeBERTa-large/
│   └── llm/
│       └── fakeshield-v1-22b/
```

其中：

- `service_code/structured_models/`：结构化文本模型 `*.joblib`
- `checkpoints/image_forgery/`：图像鉴伪模型权重
- `checkpoints/checkpoints/hc3_classifier/`：Bert 文本鉴伪微调 checkpoint
- `checkpoints/weights/`：QiDeBERTa 底座权重
- `checkpoints/llm/fakeshield-v1-22b/`：大模型图像鉴伪权重

## 3. 环境配置

建议在 `AI服务器代码` 目录下创建虚拟环境，并一次性安装统一服务所需依赖：

```bash
cd /mnt/data14/ccy/Bert/SE/AI_service/service_code
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install albumentations baal easydict einops numpy opencv-python Pillow scikit-image scikit-learn scipy timm torchmetrics torchsnooper tqdm joblib openai transformers datasets sentencepiece pandas
```

说明：

- `cu121` 仅为示例，需按服务器 CUDA 版本调整
- 服务器需先具备可用的 NVIDIA 驱动和 CUDA 运行环境

## 4. 模型与环境变量

启动前建议设置：

```bash
export STRUCTURED_AI_MODEL_DIR=/mnt/data14/ccy/Bert/SE/AI_service/service_code/structured_models
export BERT_PROJECT_ROOT=/mnt/data14/ccy/Bert/SE/AI_service/checkpoints
```

如需固定默认 Bert 文本模型，也可以额外设置：

```bash
export BERT_TEXT_MODEL_DIR=/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/checkpoints/hc3_classifier/QiDeBERTa-base/chinese/final
```

图片鉴伪权重默认放在：

```bash
/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/image_forgery
```

至少需要：

- `Coarse_v2.pkl`
- `blurring.pkl`
- `brute_force.pkl`
- `contrast.pkl`
- `inpainting.pkl`

## 5. 启动服务

```bash
cd /mnt/data14/ccy/Bert/SE/AI_service/service_code
source .venv/bin/activate
export STRUCTURED_AI_MODEL_DIR=/mnt/data14/ccy/Bert/SE/AI_service/service_code/structured_models
export BERT_PROJECT_ROOT=/mnt/data14/ccy/Bert/SE/AI_service/checkpoints
python trigger_unified.py
```

推荐使用 `tmux` 或 `nohup` 持久化运行。

启动后，服务默认等待：

```bash
./requests/request.json
```

也可以通过环境变量覆盖：

- `UNIFIED_AI_REQUEST_FILE`
- `UNIFIED_AI_REQUEST_DIR`

## 6. 运行结果

服务启动后先输出：

```text
ai service ready
```

处理成功后输出：

```text
ai service result
<base64-encoded-json>
```

后端读取并解码该 JSON 即可。

## 7. 兼容说明

以下旧入口仍然保留，但不再是推荐方式：

- `trigger.py`：仅图片鉴伪
- `trigger_structured.py`：仅结构化文本鉴伪

新接入请统一使用 `trigger_unified.py`。

## 8. 权重软链接说明

当前已按以下方式组织统一权重入口：

- `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/image_forgery`
  指向：
  `/mnt/data14/ccy/Bert/SE/AI_train/checkpoints`

- `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/checkpoints/hc3_classifier`
  指向：
  `/mnt/data14/ccy/Bert/checkpoints/hc3_classifier`

- `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/weights/QiDeBERTa-base`
  指向：
  `/mnt/data14/ccy/Bert/weights/QiDeBERTa-base`

- `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/weights/QiDeBERTa-large`
  指向：
  `/mnt/data14/ccy/Bert/weights/QiDeBERTa-large`

如需启用大模型图像鉴伪，还需要将：

- `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/llm/fakeshield-v1-22b`

准备为有效模型目录。

## 9. 大模型图像鉴伪开关

图片鉴伪 pipeline 默认不会启用大模型。

请求文件中将：

```json
"if_use_llm": false
```

改为：

```json
"if_use_llm": true
```

即可在图片鉴伪流程中额外启用大模型分析。

示例位置：

- `/mnt/data14/ccy/Bert/SE/AI_service/service_code/requests/request.example.image.json`

该能力依赖：

- `service_code/method/SingleImageMethod.py`
- `service_code/method/llm/DTE-FDM/llava/serve/cli.py`
- `service_code/method/llm/MFLM/cli_demo.py`

其中：

- `DTE-FDM` 负责生成文本/描述类输出
- `MFLM` 负责生成更细的图像级定位结果

注意：

- 该流程当前在 `SingleImageMethod.py` 中固定使用 `/root/miniconda3/envs/llm/bin/python`
- 默认固定使用 `CUDA_VISIBLE_DEVICES=0`
- 权重目录默认读取：
  `/mnt/data14/ccy/Bert/SE/AI_service/checkpoints/llm/fakeshield-v1-22b`

## 10. 模型 GPU 配置

服务侧现在新增统一配置文件：

- `/mnt/data14/ccy/Bert/SE/AI_service/service_code/service_config.py`

其中 `model_devices` 字段用于给各模型指定 GPU 序号，例如：

```python
"model_devices": {
    "urn_coarse_v2": 0,
    "urn_blurring": 1,
    "urn_brute_force": 2,
    "urn_contrast": 3,
    "urn_inpainting": 4,
    "bert_text": 5,
    "llm_image": 6,
}
```

当前支持的配置项有：

- `urn_coarse_v2`
- `urn_blurring`
- `urn_brute_force`
- `urn_contrast`
- `urn_inpainting`
- `bert_text`
- `llm_image`

修改后重新启动服务即可生效。
