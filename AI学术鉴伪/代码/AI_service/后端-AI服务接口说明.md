# 后端-AI服务接口说明

本文档说明后端如何通过 SSH 调用统一 AI 服务 `trigger_unified.py`。

## 1. 通信方式

统一 AI 服务不是 HTTP 接口，而是：

1. 后端通过 SSH 启动 `python trigger_unified.py`
2. 后端将请求写入请求文件
3. AI 服务读取请求文件并执行对应 pipeline
4. AI 服务将结果输出到标准输出

默认请求文件路径：

```bash
AI服务器代码/requests/request.json
```

## 2. 服务输出标记

服务启动后先输出：

```text
ai service ready
```

处理完成后输出：

```text
ai service result
<base64-encoded-json>
```

后端应读取 `ai service result` 下一行，并进行 base64 解码，再解析 JSON。

## 3. 统一请求格式

请求必须是一个 JSON 对象：

```json
{
  "request_id": "req-001",
  "pipeline": "image | structured | bert | auto",
  "detect_type": "paper | review",
  "payload": {}
}
```

字段说明：

- `request_id`：后端生成的请求 ID，结果会原样返回
- `pipeline`：
  - `image`：图片鉴伪
  - `structured`：结构化文本鉴伪
  - `bert`：Bert/QiDeBERTa 文本 AIGC 鉴伪
  - `auto`：由服务端自动判断
- `detect_type`：仅结构化文本 pipeline 需要
- `payload`：对应 pipeline 的具体输入

## 4. 图片鉴伪请求

图片鉴伪沿用原项目范式，后端实际上传的是两个文件，而不是把图片直接写进请求 JSON：

1. `img.zip`
2. `data.json`

其中 `img.zip` 内是待检测图片，`data.json` 内容大致为：

```json
{
  "cmd_block_size": 64,
  "urn_k": 0.3,
  "if_use_llm": false
}
```

统一入口为了兼容三类 pipeline，允许在请求 JSON 中只传文件路径引用，例如：

```json
{
  "request_id": "img-demo-001",
  "pipeline": "image",
  "payload": {
    "image_zip": "../test/img.zip",
    "config_path": "../test/data.json"
  }
}
```

说明：

- `image_zip`：图片压缩包路径引用
- zip 中应直接放图片文件，不要再嵌套子目录
- `config_path`：图片鉴伪参数文件路径引用
- 如果后端已经把 `img.zip` 和 `data.json` 放到约定目录，也可以不显式传 `config_path`

## 5. 结构化文本鉴伪请求

```json
{
  "request_id": "structured-demo-001",
  "pipeline": "structured",
  "detect_type": "paper",
  "payload": {
    "paper_files": [
      {
        "file_id": 1,
        "file_name": "demo.pdf",
        "resource_role": "paper_main",
        "file_ext": "pdf",
        "parse_status": "parsed",
        "sections": [
          {
            "title": "第1页",
            "text": "这里放论文解析后的正文文本。",
            "source": "pdf_extracted",
            "page_number": 1
          }
        ]
      }
    ],
    "images": [
      {
        "image_id": 10,
        "file_management_id": 1,
        "image_role": "figure",
        "source_kind": "pdf_extracted",
        "page_number": 1,
        "image_url": "/media/extracted_images/demo_page1_image1.png",
        "width": 1280,
        "height": 720
      }
    ]
  }
}
```

`detect_type` 当前支持：

- `paper`
- `review`

说明：

- 原后端会把文本内容直接写入 JSON
- `images` 中放的是图片元数据和路径引用，不是图片二进制内容
- 当前结构化 AI 服务主要消费文本和图片元数据，不直接读取图片像素内容

## 6. Bert 文本 AIGC 鉴伪请求

### 6.1 单文本模式

```json
{
  "request_id": "bert-demo-001",
  "pipeline": "bert",
  "payload": {
    "lang": "chinese",
    "text": "这是一个待检测是否由大模型生成的学术文本片段。",
    "max_length": 256
  }
}
```

### 6.2 问答对模式

```json
{
  "request_id": "bert-demo-002",
  "pipeline": "bert",
  "payload": {
    "lang": "chinese",
    "pair_mode": true,
    "question": "请总结这项研究的核心结论",
    "answer": "这里放待检测回答文本"
  }
}
```

说明：

- `text`：单文本输入
- `question + answer`：问答对输入
- `lang`：当前建议使用 `chinese`

## 7. 统一返回格式

服务返回的是 base64 编码后的 JSON。解码后格式如下：

### 7.1 成功

```json
{
  "success": true,
  "request_id": "req-001",
  "pipeline": "bert_text",
  "result": {}
}
```

### 7.2 失败

```json
{
  "success": false,
  "request_id": "req-001",
  "error": {
    "type": "ValueError",
    "message": "..."
  }
}
```

## 8. 各 pipeline 返回内容概览

### 8.1 图片鉴伪

返回结构大致为：

```json
{
  "summary": {},
  "transport": {}
}
```

其中：

- `summary.image_count`
- `summary.config`
- `summary.method_names`
- `transport.format`
- `transport.data`

需要注意：

- 原项目图片鉴伪的返回范式不是 JSON 内直接展开图像结果
- 原服务返回的是 `pickle` 序列化结果，再做 `base64` 编码
- 因此统一接口下，图片 pipeline 也保持“结果载荷以 `pickle+base64` 传输”的兼容方式，而不是把图像矩阵直接塞进 JSON

### 8.2 结构化文本鉴伪

返回结构沿用原有逻辑，核心字段包括：

- `overall.is_fake`
- `overall.confidence_score`
- `overall.risk_level`
- `dimensions`
- `evidence`

### 8.3 Bert 文本 AIGC 鉴伪

返回结构大致为：

```json
{
  "model_dir": "...",
  "base_model_dir": "...",
  "lang": "chinese",
  "is_aigc": true,
  "label": 1,
  "label_name": "aigc",
  "confidence_score": 0.97,
  "probabilities": {
    "human": 0.03,
    "aigc": 0.97
  },
  "input_summary": {}
}
```

后端一般重点使用：

- `is_aigc`
- `label_name`
- `confidence_score`
- `probabilities`

说明：

- `confidence_score` 和 `probabilities` 不是模型 checkpoint 自带字段
- 它们是服务端拿到分类 `logits` 后，额外做 `softmax` 计算出来的派生结果

## 9. 推荐后端调用流程

推荐流程：

1. 后端生成请求 JSON
2. 将请求写入 `requests/request.json`
3. SSH 启动 `python trigger_unified.py`
4. 等待 `ai service ready`
5. 等待 `ai service result`
6. 读取下一行 base64
7. 解码并解析 JSON
8. 返回业务层
