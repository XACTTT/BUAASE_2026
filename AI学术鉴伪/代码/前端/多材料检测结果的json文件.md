{
  "overall": {
    "is_fake": false,
    "confidence_score": 0.2187,
    "risk_level": "low"
  },
  "task_type": "multi",
  "validation": {
    "valid": true,
    "material_types_present": [
      "paper",
      "image",
      "review"
    ],
    "missing_required": [],
    "message": "校验通过"
  },
  "material_cards": [
    {
      "type": "paper",
      "label": "论文材料",
      "summary": "1 篇论文，共 1890 个章节",
      "score": 0.2117,
      "file_count": 1,
      "files": [
        {
          "file_id": 66,
          "file_name": "KVTuner.pdf"
        }
      ]
    },
    {
      "type": "review",
      "label": "评审材料",
      "summary": "1 个评审文件，0 段评审文本",
      "score": 0.3523,
      "file_count": 1,
      "files": [
        {
          "file_id": 67,
          "file_name": "kvtuner-review.pdf"
        }
      ]
    },
    {
      "type": "image",
      "label": "图片材料",
      "summary": "15 张图片",
      "file_count": 15,
      "images": [
        {
          "image_id": 598,
          "image_url": "/media/extracted_images/63_9e506317cebe4c42b4b4f10dcd0f6e89.png"
        },
        {
          "image_id": 599,
          "image_url": "/media/extracted_images/64_cd61c3fd546a47eeb85b1dde0a0683a2.png"
        },
        {
          "image_id": 600,
          "image_url": "/media/extracted_images/65_964009cc74f74a8d8c4b78c77c83a95d.png"
        },
        {
          "image_id": 601,
          "image_url": "/media/extracted_images/7e14d2ea42d74a45baccd2fce378aae9_66_page24_image1.png"
        },
        {
          "image_id": 602,
          "image_url": "/media/extracted_images/4cb3aeb5d444438bb04fbdbfdb4bd476_66_page24_image2.png"
        },
        {
          "image_id": 603,
          "image_url": "/media/extracted_images/623c7c0f134c4066a43ad9d007a461e5_66_page24_image3.png"
        },
        {
          "image_id": 604,
          "image_url": "/media/extracted_images/dd266f670c3d48fc8d6090d0e65f2bee_66_page24_image4.png"
        },
        {
          "image_id": 605,
          "image_url": "/media/extracted_images/6102aa2ca46f4f509b13a874be109ed5_66_page24_image5.png"
        },
        {
          "image_id": 606,
          "image_url": "/media/extracted_images/70a4d9f321cd41a1982e4e9c7e97653d_66_page24_image6.png"
        },
        {
          "image_id": 607,
          "image_url": "/media/extracted_images/aa0c389f1d9a4b96a43c3b1d9875d968_66_page25_image1.png"
        },
        {
          "image_id": 608,
          "image_url": "/media/extracted_images/67b05cb0f6934f7ca24a1d2531d71712_66_page25_image2.png"
        },
        {
          "image_id": 609,
          "image_url": "/media/extracted_images/4cab87c9abe34f95874832c9d42690cb_66_page25_image3.png"
        },
        {
          "image_id": 610,
          "image_url": "/media/extracted_images/4c54cea0208540408d14c7ac21a96f69_66_page25_image4.png"
        },
        {
          "image_id": 611,
          "image_url": "/media/extracted_images/030514caeb784869a53b90eebb1b07a0_66_page25_image5.png"
        },
        {
          "image_id": 612,
          "image_url": "/media/extracted_images/894c723b7b28402ca33b76202e5d8142_66_page25_image6.png"
        }
      ]
    }
  ],
  "cross_material_analysis": null,
  "ai_contribution": [],
  "evidence": {
    "model_dir": "/mnt/data/ccy/Bert/checkpoints/hc3_classifier/QiDeBERTa-base/chinese/final",
    "lang": "chinese",
    "section_count": 1988,
    "aigc_section_count": 435,
    "aggregate": {
      "aigc_ratio": 0.21881287726358148,
      "mean_aigc_probability": 0.21865960017533878,
      "mean_confidence": 0.9495185352786926,
      "max_confidence": 0.9999963045120239,
      "min_confidence": 0.5013912320137024
    },
    "per_section": [
      {
        "item_id": "multi_paper_0_0",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9916959404945374,
        "probabilities": {
          "human": 0.008304079994559288,
          "aigc": 0.9916959404945374
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache\nQuantization for Efficient and Nearly Lossless LLM Inference",
        "title": "第1页-段落1",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8093733787536621,
        "probabilities": {
          "human": 0.19062666594982147,
          "aigc": 0.8093733787536621
        },
        "text": "Xing Li * 1 Zeyu Xing * 2 Yiming Li 1 Linping Qu 1 Hui-Ling Zhen 1 Yiwu Yao 3 Wulong Liu 1",
        "title": "第1页-段落2",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_2",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9901669025421143,
        "probabilities": {
          "human": 0.9901669025421143,
          "aigc": 0.009833053685724735
        },
        "text": "Sinno Jialin Pan 2 Mingxuan Yuan 1",
        "title": "第1页-段落3",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_3",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978336691856384,
        "probabilities": {
          "human": 0.9978336691856384,
          "aigc": 0.002166296821087599
        },
        "text": "Abstract",
        "title": "第1页-段落4",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_4",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7519552707672119,
        "probabilities": {
          "human": 0.7519552707672119,
          "aigc": 0.2480446845293045
        },
        "text": "Search space:\nlayer-wise KV cache\nquant. precision pairs",
        "title": "第1页-段落5",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_5",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9784542322158813,
        "probabilities": {
          "human": 0.9784542322158813,
          "aigc": 0.021545812487602234
        },
        "text": "Constraints & objectives:",
        "title": "第1页-段落6",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_6",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9606003761291504,
        "probabilities": {
          "human": 0.9606003761291504,
          "aigc": 0.039399635046720505
        },
        "text": "LLMs with layer-wise KV cache\nprecision pairs e.g. KV8, K8V4, K4V2",
        "title": "第1页-段落7",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_7",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9127709865570068,
        "probabilities": {
          "human": 0.9127709865570068,
          "aigc": 0.08722900599241257
        },
        "text": "memory footprint,\nmodel accuracy, etc",
        "title": "第1页-段落8",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_8",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976968169212341,
        "probabilities": {
          "human": 0.9976968169212341,
          "aigc": 0.002303178422152996
        },
        "text": "Low-sensitivity layers Prefix/Recent KV16",
        "title": "第1页-段落9",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_9",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990791082382202,
        "probabilities": {
          "human": 0.0009208688861690462,
          "aigc": 0.9990791082382202
        },
        "text": "KV cache quantization can improve Large Lan-\nguage Models (LLMs) inference throughput and\nlatency in long contexts and large batch-size\nscenarios while preserving LLMs effectiveness.\nHowever, current methods have three unsolved\nissues: overlooking layer-wise sensitivity to KV\ncache quantization, high overhead of online fine-\ngrained decision-making, and low flexibility to\ndifferent LLMs and constraints. Therefore, we\ntheoretically analyze the inherent correlation of\nlayer-wise transformer attention patterns to KV\ncache quantization errors and study why key\ncache is generally more important than value\ncache for quantization error reduction. We fur-\nther propose a simple yet effective framework\nKVTuner to adaptively search for the optimal\nhardware-friendly layer-wise KV quantization\nprecision pairs for coarse-grained KV cache with\nmulti-objective optimization and directly utilize\nthe offline searched configurations during on-\nline inference. To reduce the computational cost\nof offline calibration, we utilize the intra-layer\nKV precision pair pruning and inter-layer clus-\ntering to reduce the search space. Experimen-\ntal results show that we can achieve nearly loss-\nless 3.25-bit mixed precision KV cache quantiza-\ntion for LLMs like Llama-3.1-8B-Instruct and\n4.0-bit for sensitive models like Qwen2.5-7B-\nInstruct on mathematical reasoning tasks. The\nmaximum inference throughput can be improved\nby 21.25% compared with KIVI-KV8 quantiza-\ntion over various context lengths. Our code and\nsearched configurations are available at https:\n//github.com/cmd2001/KVTuner.",
        "title": "第1页-段落10",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_10",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929444193840027,
        "probabilities": {
          "human": 0.9929444193840027,
          "aigc": 0.007055575493723154
        },
        "text": "K4",
        "title": "第1页-段落11",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_11",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999434947967529,
        "probabilities": {
          "human": 0.9999434947967529,
          "aigc": 0.000056478755141142756
        },
        "text": "arXiv:2502.04420v5  [cs.LG]  20 Nov 2025",
        "title": "第1页-段落12",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_12",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9889481067657471,
        "probabilities": {
          "human": 0.9889481067657471,
          "aigc": 0.011051837354898453
        },
        "text": "V2",
        "title": "第1页-段落13",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_13",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977479577064514,
        "probabilities": {
          "human": 0.9977479577064514,
          "aigc": 0.0022520553320646286
        },
        "text": "Layer-wise",
        "title": "第1页-段落14",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_14",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9821908473968506,
        "probabilities": {
          "human": 0.9821908473968506,
          "aigc": 0.01780921220779419
        },
        "text": "Intra-layer Pareto efficient",
        "title": "第1页-段落15",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_15",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6793113946914673,
        "probabilities": {
          "human": 0.6793113946914673,
          "aigc": 0.3206885755062103
        },
        "text": "KV cache qunatization\nprecision pair pruning",
        "title": "第1页-段落16",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_16",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977479577064514,
        "probabilities": {
          "human": 0.9977479577064514,
          "aigc": 0.0022520553320646286
        },
        "text": "Layer-wise",
        "title": "第1页-段落17",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_17",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989705085754395,
        "probabilities": {
          "human": 0.9989705085754395,
          "aigc": 0.0010295145912095904
        },
        "text": "Medium-sensitivity layers",
        "title": "第1页-段落18",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_18",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9781854152679443,
        "probabilities": {
          "human": 0.9781854152679443,
          "aigc": 0.0218146201223135
        },
        "text": "Pruned KV precision pairs",
        "title": "第1页-段落19",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_19",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9868859052658081,
        "probabilities": {
          "human": 0.9868859052658081,
          "aigc": 0.013114074245095253
        },
        "text": "Inter-layer clustering",
        "title": "第1页-段落20",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_20",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9900038838386536,
        "probabilities": {
          "human": 0.9900038838386536,
          "aigc": 0.009996048174798489
        },
        "text": "K8",
        "title": "第1页-段落21",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_21",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7699215412139893,
        "probabilities": {
          "human": 0.23007848858833313,
          "aigc": 0.7699215412139893
        },
        "text": "based on\nattention output errors",
        "title": "第1页-段落22",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_22",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8500379323959351,
        "probabilities": {
          "human": 0.14996208250522614,
          "aigc": 0.8500379323959351
        },
        "text": "Attention error vector",
        "title": "第1页-段落23",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_23",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9941442608833313,
        "probabilities": {
          "human": 0.9941442608833313,
          "aigc": 0.00585574796423316
        },
        "text": "V4",
        "title": "第1页-段落24",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_24",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9710932970046997,
        "probabilities": {
          "human": 0.9710932970046997,
          "aigc": 0.028906702995300293
        },
        "text": "Whole model",
        "title": "第1页-段落25",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_25",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979052543640137,
        "probabilities": {
          "human": 0.9979052543640137,
          "aigc": 0.002094802213832736
        },
        "text": "High-sensitivity layers",
        "title": "第1页-段落26",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_26",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7269794940948486,
        "probabilities": {
          "human": 0.27302050590515137,
          "aigc": 0.7269794940948486
        },
        "text": "Optimal KV precision search\nmulti-objective optimization",
        "title": "第1页-段落27",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_27",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9801924824714661,
        "probabilities": {
          "human": 0.9801924824714661,
          "aigc": 0.019807495176792145
        },
        "text": "Final memory&accuracy",
        "title": "第1页-段落28",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_28",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9900038838386536,
        "probabilities": {
          "human": 0.9900038838386536,
          "aigc": 0.009996048174798489
        },
        "text": "K8",
        "title": "第1页-段落29",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_29",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988687634468079,
        "probabilities": {
          "human": 0.9988687634468079,
          "aigc": 0.0011312373680993915
        },
        "text": "KVTuner",
        "title": "第1页-段落30",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_30",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9911256432533264,
        "probabilities": {
          "human": 0.9911256432533264,
          "aigc": 0.00887430738657713
        },
        "text": "V8",
        "title": "第1页-段落31",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_31",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8840392827987671,
        "probabilities": {
          "human": 0.11596076935529709,
          "aigc": 0.8840392827987671
        },
        "text": "Offline efficient search based on\nlayer-wise sensitivities to KV quant.",
        "title": "第1页-段落32",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_32",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9985803365707397,
        "probabilities": {
          "human": 0.0014196266420185566,
          "aigc": 0.9985803365707397
        },
        "text": "Figure 1: The layer-wise KV cache quantization tuning\nframework KVTuner with two-stage search space pruning\nfor efficient MOO search using the final memory and model\naccuracy.",
        "title": "第1页-段落33",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_33",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第1页-段落34",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_34",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9945218563079834,
        "probabilities": {
          "human": 0.9945218563079834,
          "aigc": 0.005478155333548784
        },
        "text": "BF16\nKV8\nKV4\nKV2",
        "title": "第1页-段落35",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_35",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9945218563079834,
        "probabilities": {
          "human": 0.9945218563079834,
          "aigc": 0.005478155333548784
        },
        "text": "BF16\nKV8\nKV4\nKV2",
        "title": "第1页-段落36",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_36",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第1页-段落37",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_37",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第1页-段落38",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_38",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第1页-段落39",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_39",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第1页-段落40",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_40",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5999752283096313,
        "probabilities": {
          "human": 0.5999752283096313,
          "aigc": 0.40002480149269104
        },
        "text": "Attention score",
        "title": "第1页-段落41",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_41",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5999752283096313,
        "probabilities": {
          "human": 0.5999752283096313,
          "aigc": 0.40002480149269104
        },
        "text": "Attention score",
        "title": "第1页-段落42",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_42",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第1页-段落43",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_43",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第1页-段落44",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_44",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第1页-段落45",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_45",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第1页-段落46",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_46",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第1页-段落47",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_47",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979687333106995,
        "probabilities": {
          "human": 0.9979687333106995,
          "aigc": 0.002031297655776143
        },
        "text": "0.04",
        "title": "第1页-段落48",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_48",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第1页-段落49",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_49",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977206587791443,
        "probabilities": {
          "human": 0.9977206587791443,
          "aigc": 0.00227933912537992
        },
        "text": "0.02",
        "title": "第1页-段落50",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_50",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9965678453445435,
        "probabilities": {
          "human": 0.9965678453445435,
          "aigc": 0.003432193072512746
        },
        "text": "0.00",
        "title": "第1页-段落51",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_51",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9965678453445435,
        "probabilities": {
          "human": 0.9965678453445435,
          "aigc": 0.003432193072512746
        },
        "text": "0.00",
        "title": "第1页-段落52",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_52",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8567771315574646,
        "probabilities": {
          "human": 0.8567771315574646,
          "aigc": 0.1432228684425354
        },
        "text": "0\n10\n20\n30\n40\n50\n60\n70\nKey position",
        "title": "第1页-段落53",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_53",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8567771315574646,
        "probabilities": {
          "human": 0.8567771315574646,
          "aigc": 0.1432228684425354
        },
        "text": "0\n10\n20\n30\n40\n50\n60\n70\nKey position",
        "title": "第1页-段落54",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_54",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858111143112183,
        "probabilities": {
          "human": 0.9858111143112183,
          "aigc": 0.014188830740749836
        },
        "text": "(a) Layer-0 query head-2",
        "title": "第1页-段落55",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_55",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9870044589042664,
        "probabilities": {
          "human": 0.9870044589042664,
          "aigc": 0.012995605356991291
        },
        "text": "(b) Layer-21 query head-4",
        "title": "第1页-段落56",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_56",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9968248605728149,
        "probabilities": {
          "human": 0.003175170859321952,
          "aigc": 0.9968248605728149
        },
        "text": "Figure 2: Token-level attention score of the 79-th query\ntoken to previous key tokens with the per-token-asym key\ncache quantization (Qwen2.5-7B-Instruct, GSM8K). Low-\nprecision KV quantization (4-bit and 2-bit) causes signif-\nicant distribution shifts, resulting in errors of missing or\nincorrect critical key identification.",
        "title": "第1页-段落57",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_57",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5456386208534241,
        "probabilities": {
          "human": 0.5456386208534241,
          "aigc": 0.4543613791465759
        },
        "text": "1. Introduction",
        "title": "第1页-段落58",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_58",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997181296348572,
        "probabilities": {
          "human": 0.0002818937646225095,
          "aigc": 0.9997181296348572
        },
        "text": "Large language models (LLMs) and multi-modality large\nmodels can comprehend and generate text, audio, image,\nand video like humans, showing the strong capability of\nassisting and interacting with humans. LLM inference effi-\nciency such as throughput and latency is critical to enhance\nuser experience and reduce cost. To improve the inference\nefficiency of LLMs, previously processed KV tokens are\ncached to avoid redundant recomputation. However, the\nmemory usage of the KV cache linearly grows with the",
        "title": "第1页-段落59",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_59",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5646750926971436,
        "probabilities": {
          "human": 0.5646750926971436,
          "aigc": 0.43532487750053406
        },
        "text": "*Equal contribution\n1Huawei Noah’s Ark Lab 2The Chi-\nnese University of Hong Kong 3Huawei Computing Product\nLine.\nCorrespondence to: Xing Li <li.xing2@huawei.com>,\nZeyu\nXing\n<zeyuxing@link.cuhk.edu.hk>,\nSinno\nJialin\nPan\n<sinnopan@cuhk.edu.hk>,\nMingxuan\nYuan\n<yuan.mingxuan@huawei.com>.",
        "title": "第1页-段落60",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_60",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8800745010375977,
        "probabilities": {
          "human": 0.11992546170949936,
          "aigc": 0.8800745010375977
        },
        "text": "Proceedings of the 42 nd International Conference on Machine\nLearning, Vancouver, Canada. PMLR 267, 2025. Copyright 2025\nby the author(s).",
        "title": "第1页-段落61",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_61",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9798263311386108,
        "probabilities": {
          "human": 0.9798263311386108,
          "aigc": 0.020173681899905205
        },
        "text": "1",
        "title": "第1页-段落62",
        "page_number": 1,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_62",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第2页-段落1",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_63",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997453093528748,
        "probabilities": {
          "human": 0.0002547201875131577,
          "aigc": 0.9997453093528748
        },
        "text": "cache quantization under constrained hardware resources:\n1) Can we further almost losslessly compress KV cache\nwith hardware-friendly and mixed precision quantization in\na plug-and-play way? 2) Are there any other inherent model\nproperties such as attention patterns (Tang et al., 2025; Xiao\net al., 2025) that can help better trade-off memory reduction\nand model accuracy? 3) There are normally multiple de-\nployed LLMs in the industrial service systems and Artificial\nIntelligence (AI) agents. How to adaptively tune the KV\ncache quantization precision considering the accuracy re-\nquirement of requests and the LLM sensitivity to KV cache\nquantization?",
        "title": "第2页-段落2",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_64",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994055032730103,
        "probabilities": {
          "human": 0.0005945011507719755,
          "aigc": 0.9994055032730103
        },
        "text": "number of batch size and sequence length, so the KV cache\nbecomes the new bottleneck of LLM serving systems with\nlarge batching requests and long context. Valuable long con-\ntext generation applications include multi-turn dialogues,\nlong document understanding, and OpenAI o1-like level-2\nreasoning. Commercial companies are releasing their sup-\nports for long context generation and KV cache-based ser-\nvices like prompt caching for better capability and efficiency\n(OpenAI, 2024; DeepSeek, 2024). Efficient KV cache man-\nagement and compression can accelerate LLM inference\nand reduce hardware resource consumption, making it a\nfoundational technique for advancing both enterprise-scale\nLLM deployment and personalized AI agents.",
        "title": "第2页-段落3",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_65",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996954202651978,
        "probabilities": {
          "human": 0.00030465656891465187,
          "aigc": 0.9996954202651978
        },
        "text": "To address these issues, we thoroughly study the sensitiv-\nity of LLM transformer layers to KV cache quantization\nand theoretically find out that error accumulation caused\nby KV cache quantization is strongly correlated with\nattention patterns in Section 4.1 and 4.4. According to\nour observation of the sensitivity of key and value cache\nin the same layer in Section 4.2 and 4.3 and the layer-wise\ndifference of transformer layers in Section 4.5, we propose\nto quantize coarse-grained key and value cache in the\nsame layer with different precision and automatically\nsearch for the optimal layer-wise KV cache quantiza-\ntion precision pairs based on the inherent importance\nof intermediate layers in Section 5. During online serv-\ning, the offline calibrated layer-wise KV cache quantization\nprecision pairs are directly loaded without any additional\noverhead to improve inference throughput and latency. Our\ncontributions are summarized as follows:",
        "title": "第2页-段落4",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_66",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.996920108795166,
        "probabilities": {
          "human": 0.0030798905063420534,
          "aigc": 0.996920108795166
        },
        "text": "KV cache quantization is one of the most stable and eas-\nily deployable KV cache compression methods to reduce\nthe memory footprint and improve throughput (Yuan et al.,\n2024). INT8/FP8 KV cache with dynamic asymmetric\ntoken-wise (per-token-asym) or channel-wise (per-channel-\nasym) quantization can achieve lossless compression in\nmost practical applications. However, lower-bit KV cache\nquantization easily leads to model accuracy degradation.",
        "title": "第2页-段落5",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_67",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9978746175765991,
        "probabilities": {
          "human": 0.00212534936144948,
          "aigc": 0.9978746175765991
        },
        "text": "Intra-layer mixed precision KV quantization methods re-\ntain important KV tokens with high precision to reduce\nKV cache quantization errors and quantize other cache in\nthe same layer with uniformly low precision such as 2-bit.\nKIVI (Liu et al., 2024e), IntactKV (Liu et al., 2024c), and\nKVQuant (Hooper et al., 2024) statically keep prefix and\ninitial KV cache blocks with high precision. They need\nspecially designed operators for hardware like GPUs and\nrequire more careful KV cache management. Besides, the\nassumption that the static prefix and recent KV is important\nmay not always hold as demonstrated in Figure 2, where\nlow-precision quantization (4-bit and 2-bit) leads to dra-\nmatic attention distribution shift in sensitive models like\nQwen2.5-7B-Instruct. Existing static and uniform KV preci-\nsion methods including KIVI 4-bit cannot effectively handle\nthese non-sparse retrieval heads. The only viable and effi-\ncient solution is to increase KV cache quantization precision\nof the whole model or some critical and sensitive layers.",
        "title": "第2页-段落6",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_68",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998205304145813,
        "probabilities": {
          "human": 0.0001794451236492023,
          "aigc": 0.9998205304145813
        },
        "text": "• We study the underlying mechanism of why key cache\nnormally is more important than value cache. The\nLLM accuracy degradation with low-bit key cache\nquantization is mainly caused by error accumulation\nand the layer-wise attention error distribution shift. We\nfind out that the sensitivity of LLMs and intermediate\nlayers to KV cache quantization is the model property\nand independent of input prompts.",
        "title": "第2页-段落7",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_69",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996403455734253,
        "probabilities": {
          "human": 0.00035966496216133237,
          "aigc": 0.9996403455734253
        },
        "text": "• We propose to automatically search for the hardware-\nfriendly layer-wise KV cache precision pairs such as\nK8V4 and K4V2 with multi-objective optimization\n(MOO) under certain memory or accuracy constraints\nfor efficient online inference. The intra-layer prun-\ning and inter-layer clustering are used to significantly\nreduce the search space and the offline tuning cost.",
        "title": "第2页-段落8",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_70",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9957420229911804,
        "probabilities": {
          "human": 0.004257986322045326,
          "aigc": 0.9957420229911804
        },
        "text": "In contrast, fine-grained methods, such as QAQ (Dong et al.,\n2024), MiKV (Yang et al., 2024b), and ZipCache (He et al.,\n2024b), dynamically identify critical KV cache and update\ntheir precision on-the-fly to improve accuracy. However,\nthey cannot be easily integrated with flash attention (Dao\net al., 2022) and vLLM (Kwon et al., 2023), because of the\nintra-layer fine-grained KV cache precision difference and\nadditional deployment efforts. In addition, the online com-\nputation and control flow logic for critical token identifica-\ntion introduce overhead and do not fit into static graph-based\ninference acceleration methods.",
        "title": "第2页-段落9",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_71",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990190267562866,
        "probabilities": {
          "human": 0.0009809518232941628,
          "aigc": 0.9990190267562866
        },
        "text": "• We empirically demonstrate that our mixed-precision\nKV tuning framework KVTuner can achieve almost\nlossless KV cache quantization with equivalent 4-bit\neven 3.25-bit precision in mathematical reasoning tasks\nfor most LLMs with 21.25% inference throughput im-\nprovement.",
        "title": "第2页-段落10",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_72",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9979612827301025,
        "probabilities": {
          "human": 0.0020387289114296436,
          "aigc": 0.9979612827301025
        },
        "text": "There are still several issues to improve the inference\nthroughput and maximum supported context length with KV",
        "title": "第2页-段落11",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_73",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9529740214347839,
        "probabilities": {
          "human": 0.9529740214347839,
          "aigc": 0.04702598601579666
        },
        "text": "2",
        "title": "第2页-段落12",
        "page_number": 2,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_74",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第3页-段落1",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_75",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990935325622559,
        "probabilities": {
          "human": 0.0009064949117600918,
          "aigc": 0.9990935325622559
        },
        "text": "Table 1: The error accumulation caused by low-bit KV cache quantization (KIVI-2) potentially leads to wrong responses of\nmathematical reasoning tasks. The input prompt is combined with 15-shot Chain-of-Thoughts (CoTs) (Wei et al., 2023)\nfrom GSM8K training dataset for Llama2-13B-chat-hf model generation. The official KIVI CUDA kernel and code are used\nto generate the output.",
        "title": "第3页-段落2",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_76",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999863862991333,
        "probabilities": {
          "human": 0.00013609134475700557,
          "aigc": 0.999863862991333
        },
        "text": "Results with 15-th input prompt In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining enrolled in jazz dance, and the rest\nenrolled in hip-hop dance. What percentage of the entire students enrolled in hip-hop dance?\nFP16\nLet X be the number of students enrolled in hip-hop dance. The number of students enrolled in contemporary dance is 20% of 20 = 4. The number of stu-\ndents enrolled in jazz dance is 25% of the remaining = 25% of (20 - 4) = 25% of 16 = 4. Therefore, the number of students enrolled in hip-hop dance is",
        "title": "第3页-段落3",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_77",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8737108707427979,
        "probabilities": {
          "human": 0.8737108707427979,
          "aigc": 0.12628909945487976
        },
        "text": "KV cache\nprecision",
        "title": "第3页-段落4",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_78",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995983242988586,
        "probabilities": {
          "human": 0.0004016592283733189,
          "aigc": 0.9995983242988586
        },
        "text": "20 - 4 - 4 = «20-4-4=12»12 . The percentage of the entire students enrolled in hip-hop dance is 12/20 x 100% = 60% . #### 60%.\nKIVI-4\nLet X be the number of students enrolled in hip-hop dance. The number of students enrolled in contemporary dance is 20% of 20 = 4. The number of stu-\ndents enrolled in jazz dance is 25% of the remaining = 25% of (20 - 4) = 25% of 16 = 4. Therefore, the number of students enrolled in hip-hop dance is",
        "title": "第3页-段落5",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_79",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995735287666321,
        "probabilities": {
          "human": 0.00042643339838832617,
          "aigc": 0.9995735287666321
        },
        "text": "20 - 4 - 4 = «20-4-4=12»12 . The percentage of the entire students enrolled in hip-hop dance is 12/20 x 100% = 60% . #### 60%.\nKIVI-2\nLet X be the number of students who enrolled in hip-hop dance. The number of students who enrolled in contemporary dance is 20% of 20 = 4. The number\nof students who enrolled in jazz dance is 25% of 16 = 4. Therefore, the total number of students who enrolled in hip-hop dance is 20 + 4 + 4 = 28 . The\npercentage of the entire students who enrolled in hip-hop dance is 28/20 = «28/20=14»14% . #### 14.",
        "title": "第3页-段落6",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_80",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5328117609024048,
        "probabilities": {
          "human": 0.46718817949295044,
          "aigc": 0.5328117609024048
        },
        "text": "2. Related Work",
        "title": "第3页-段落7",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_81",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9578801989555359,
        "probabilities": {
          "human": 0.9578801989555359,
          "aigc": 0.04211976379156113
        },
        "text": "3. Background",
        "title": "第3页-段落8",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_82",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9873110055923462,
        "probabilities": {
          "human": 0.9873110055923462,
          "aigc": 0.012689008377492428
        },
        "text": "3.1. Transformer and KV Cache",
        "title": "第3页-段落9",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_83",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9670055508613586,
        "probabilities": {
          "human": 0.032994408160448074,
          "aigc": 0.9670055508613586
        },
        "text": "KV cache management and compression methods include\npaged KV cache (Kwon et al., 2023), prefilling-decoding\n(PD) disaggregation (Qin et al., 2024), quantization (Liu\net al., 2024e;c; Hooper et al., 2024; Zhang et al., 2024c;\nYang et al., 2024b; He et al., 2024b;a; Dong et al., 2024),\neviction (Zhang et al., 2023; Ge et al., 2024; Liu et al.,\n2023; Li et al., 2024a; Adnan et al., 2024), merging (Zhang\net al., 2024b; Wang et al., 2024; Wan et al., 2024; Liu et al.,\n2024b), low-rank decomposition (Kang et al., 2024b; Sun\net al., 2024a), offloading (Sheng et al., 2023; Zhang et al.,\n2024a), prefetching (Lee et al., 2024b), and retrieval (Tang\net al., 2024). Among them, KV cache quantization is orthog-\nonal to most other KV cache management and compression\nmethods, so it has been integrated with eviction, retrieval,\nand transferring (Tang et al., 2024; Liu et al., 2024d).",
        "title": "第3页-段落10",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_84",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994019269943237,
        "probabilities": {
          "human": 0.0005980890709906816,
          "aigc": 0.9994019269943237
        },
        "text": "In LLMs, there are multiple intermediate transformer layers\nstacked and executed to generate final output responses.\nFor the l-th transformer layer, given i-th D-dimensional\ninput hidden state xl\ni ∈RD, the l-th query, key, and value\nfeedforward neural network layers generate ql\ni = W l\nqxl\ni,\nkl\ni = W l\nkxl\ni, and vl\ni = W l\nvxl\ni with the corresponding\nweight matrices W l\nq, W l\nk, and W l\nv, respectively. Then\nthe self-attention scores al\ni are computed with the current\nquery embedding and all key embeddings until the i-th step.\nFinally, the l-th self-attention layer generates the output\nstate ol\ni, which is forwarded to downstream sub-layers in\nthe l-th transformer layer, with the softly weighted value\nembeddings V l using the attention scores al\ni:",
        "title": "第3页-段落11",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_85",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9897251129150391,
        "probabilities": {
          "human": 0.010274923406541348,
          "aigc": 0.9897251129150391
        },
        "text": "Model and activation quantization methods such as GPTQ\n(Frantar et al., 2022), SmoothQuant (Xiao et al., 2023),\nAWQ (Lin et al., 2024a), SpinQuant (Liu et al., 2024f), and\nQServe (Lin et al., 2024b) are also used to reduce model\nmemory usage and inference latency with low-bit computa-\ntion units. Model pruning and layer skipping reduce compu-\ntational cost by directly pruning unimportant layers or heads\n(Ma et al., 2023; Zeng et al., 2023; Elhoushi et al., 2024).",
        "title": "第3页-段落12",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_86",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9615721106529236,
        "probabilities": {
          "human": 0.9615721106529236,
          "aigc": 0.038427870720624924
        },
        "text": "ql\niKl⊤\n√",
        "title": "第3页-段落13",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_87",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5860936045646667,
        "probabilities": {
          "human": 0.41390642523765564,
          "aigc": 0.5860936045646667
        },
        "text": "!",
        "title": "第3页-段落14",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_88",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7343947887420654,
        "probabilities": {
          "human": 0.7343947887420654,
          "aigc": 0.26560527086257935
        },
        "text": ", ol\ni = al\niV l,\n(1)",
        "title": "第3页-段落15",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_89",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5912057757377625,
        "probabilities": {
          "human": 0.40879419445991516,
          "aigc": 0.5912057757377625
        },
        "text": "al\ni = softmax",
        "title": "第3页-段落16",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_90",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9011561870574951,
        "probabilities": {
          "human": 0.9011561870574951,
          "aigc": 0.09884379059076309
        },
        "text": "D",
        "title": "第3页-段落17",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_91",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.998126208782196,
        "probabilities": {
          "human": 0.0018738189246505499,
          "aigc": 0.998126208782196
        },
        "text": "where Kl=concat(Kl\n:i−1, kl\ni) and V l=concat(V l\n:i−1, vl\ni)\nare the key and value embeddings generated in the prefilling\nand decoding stage in l-th transformer layer until i-th step.\nThey will still be re-used in subsequent generation steps\nfor self-attention computation. Therefore, we need to store\nthem as KV cache in each layer independently to remove the\nadditional computational cost of KV cache re-computation.",
        "title": "第3页-段落18",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_92",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998757839202881,
        "probabilities": {
          "human": 0.00012424301530700177,
          "aigc": 0.9998757839202881
        },
        "text": "Speculative decoding is another promising direction for\nlossless LLM inference acceleration by reducing the LLM\ninference iteration times and KV cache memory movement\ncost in the memory-bounded decoding stage. LLMs verify\nmultiple tokens speculated with smaller models (Li et al.,\n2024b), self-partial layers (Cai et al., 2024; Liu et al., 2024a;\nGloeckle et al., 2024; Stern et al., 2018), or other training-\nfree algorithms (Zhao et al., 2024) in one forward step. In\naddition, Triforce (Sun et al., 2024b) is proposed to inte-\ngrate KV cache compression with hierarchical speculative\ndecoding to improve long context generation efficiency.",
        "title": "第3页-段落19",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_93",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9936896562576294,
        "probabilities": {
          "human": 0.9936896562576294,
          "aigc": 0.006310369353741407
        },
        "text": "3.2. KV Cache Quantization",
        "title": "第3页-段落20",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_94",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998286962509155,
        "probabilities": {
          "human": 0.00017128353647422045,
          "aigc": 0.9998286962509155
        },
        "text": "Although storing KV cache can reduce the re-computation\ncost, the KV cache may become the new inference memory\nand latency bottleneck in the large batch size and long con-\ntext scenario. KV cache quantization can effectively address\nthese problems. The round-to-nearest B-bit quantization\nand dequantization along the channel or token dimension to\ninput X ∈RS×D are defined as",
        "title": "第3页-段落21",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_95",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7915232181549072,
        "probabilities": {
          "human": 0.20847678184509277,
          "aigc": 0.7915232181549072
        },
        "text": "Q(X) = round\n\u0012X −z",
        "title": "第3页-段落22",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_96",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9017423391342163,
        "probabilities": {
          "human": 0.09825759381055832,
          "aigc": 0.9017423391342163
        },
        "text": "\u0013\n, ˆX = Q(X) · s + z,\n(2)",
        "title": "第3页-段落23",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_97",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6890420913696289,
        "probabilities": {
          "human": 0.6890420913696289,
          "aigc": 0.3109579086303711
        },
        "text": "s",
        "title": "第3页-段落24",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_98",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9549646377563477,
        "probabilities": {
          "human": 0.9549646377563477,
          "aigc": 0.04503533989191055
        },
        "text": "3",
        "title": "第3页-段落25",
        "page_number": 3,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_99",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第4页-段落1",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_100",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9945304989814758,
        "probabilities": {
          "human": 0.005469505209475756,
          "aigc": 0.9945304989814758
        },
        "text": "Table 2: Word-perplexity of different KV cache quantization\nprecision pairs with the huggingface transformers KIVI-\nHQQ implementation on the wikitext dataset and lm-eval-\nharness.",
        "title": "第4页-段落2",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_101",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7719811201095581,
        "probabilities": {
          "human": 0.2280188798904419,
          "aigc": 0.7719811201095581
        },
        "text": "where the offset z\n=\nmin(X) and the scale s\n=\nmax(X)−min(X)",
        "title": "第4页-段落3",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_102",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7654716372489929,
        "probabilities": {
          "human": 0.7654716372489929,
          "aigc": 0.23452836275100708
        },
        "text": "2B−1\n. We measure the relative KV cache and\nattention output errors and the absolute attention score er-",
        "title": "第4页-段落4",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_103",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6665289402008057,
        "probabilities": {
          "human": 0.33347102999687195,
          "aigc": 0.6665289402008057
        },
        "text": "\u0013\n, el\nv = mean\n\u0012\n|V l−ˆ\nV\nl|\n|V l|",
        "title": "第4页-段落5",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_104",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6669893860816956,
        "probabilities": {
          "human": 0.33301064372062683,
          "aigc": 0.6669893860816956
        },
        "text": "ror as el\nk = mean\n\u0012\n|Kl−ˆ\nK\nl|\n|Kl|",
        "title": "第4页-段落6",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_105",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8680261373519897,
        "probabilities": {
          "human": 0.8680261373519897,
          "aigc": 0.13197392225265503
        },
        "text": "\u0013\n,",
        "title": "第4页-段落7",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_106",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9973821043968201,
        "probabilities": {
          "human": 0.9973821043968201,
          "aigc": 0.0026178329717367887
        },
        "text": "Model\nKV8\nK8V4\nK8V2\nK4V8\nKV4\nK4V2\nK2V8\nK2V4\nKV2\nLlama3-8B-Instruct\n9.95\n9.94\n10.04\n9.99\n9.99\n10.11\n31.92\n31.48\n37.29\nLlama2-7B-chat-hf\n11.60\n11.60\n11.67\n11.61\n11.62\n11.67\n13.86\n13.92\n14.92\nLlama2-13B-chat-hf\n10.04\n10.05\n10.08\n10.06\n10.07\n10.11\n13.30\n13.37\n14.25\nMistral-7B-Instruct-v0.3\n8.28\n8.27\n8.35\n8.31\n8.29\n8.44\n12.61\n12.71\n15.18\nQwen2.5-3B-Instruct\n10.60\n10.59\n11.36\n11.11\n11.11\n12.28\n147.03\n151.30\n251.89\nQwen2.5-7B-Instruct\n9.56\n9.39\n9.45\n220.83\n235.03\n149.15\n1866.33\n1831.33\n4016.10\nQwen2.5-Math-7B-Instruct\n168.92\n169.60\n175.34\n588.34\n599.02\n725.10\n1746.07\n1760.31\n1829.26\nQwen2.5-14B-Instruct\n6.65\n6.67\n7.19\n6.81\n6.83\n7.32\n16.05\n16.37\n18.22\nQwen2.5-32B-Instruct\n6.68\n6.85\n6.34\n6.47\n6.52\n6.43\n9.13\n9.20\n9.56",
        "title": "第4页-段落8",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_107",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6295450329780579,
        "probabilities": {
          "human": 0.3704550266265869,
          "aigc": 0.6295450329780579
        },
        "text": "el\na = mean(|al −ˆal|), and el\no = mean\n\u0010\n|ol−ˆol|",
        "title": "第4页-段落9",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_108",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7993091344833374,
        "probabilities": {
          "human": 0.7993091344833374,
          "aigc": 0.2006908357143402
        },
        "text": "|ol|\n\u0011\n, where",
        "title": "第4页-段落10",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_109",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9136109948158264,
        "probabilities": {
          "human": 0.0863889679312706,
          "aigc": 0.9136109948158264
        },
        "text": "the attention score with dequantized key cache ˆal\ni =",
        "title": "第4页-段落11",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_110",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6051032543182373,
        "probabilities": {
          "human": 0.39489680528640747,
          "aigc": 0.6051032543182373
        },
        "text": "\u0013\nand the attention output with dequan-",
        "title": "第4页-段落12",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_111",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8644185662269592,
        "probabilities": {
          "human": 0.8644185662269592,
          "aigc": 0.13558144867420197
        },
        "text": "softmax\n\u0012\nql\ni ˆ\nK\nl⊤\n√",
        "title": "第4页-段落13",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_112",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9011561870574951,
        "probabilities": {
          "human": 0.9011561870574951,
          "aigc": 0.09884379059076309
        },
        "text": "D",
        "title": "第4页-段落14",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_113",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8934746980667114,
        "probabilities": {
          "human": 0.8934746980667114,
          "aigc": 0.10652527958154678
        },
        "text": "tized KV cache ˆol\ni = ˆal\ni ˆV\nl.",
        "title": "第4页-段落15",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_114",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8091935515403748,
        "probabilities": {
          "human": 0.19080640375614166,
          "aigc": 0.8091935515403748
        },
        "text": "4.2. Sensitivity to Quantization Mode and Precision",
        "title": "第4页-段落16",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_115",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7171599268913269,
        "probabilities": {
          "human": 0.7171599268913269,
          "aigc": 0.2828401029109955
        },
        "text": "4. Observation",
        "title": "第4页-段落17",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_116",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996973276138306,
        "probabilities": {
          "human": 0.00030266883550211787,
          "aigc": 0.9996973276138306
        },
        "text": "KV cache quantization errors strongly correlate with the\nquantization mode and precision as in Table 4. In terms\nof relative key error ek, the per-channel-asym quantization\nmode consistently outperforms the per-token-asym counter-\npart under the same precision for key cache, because key\ncache has strong channel-wise outliers (Liu et al., 2024e;\nHooper et al., 2024), more detailed experiment results can\nbe found in Table 9. Therefore, for specific KV cache,\nthe quantization mode modification may lead to the shift\nof importance of key and value to attention output errors.\nAs shown in Table 4, the Pareto-optimal intra-layer KV\ncache quantization precision pairs significantly differ be-\ntween these two modes. Therefore, the KV cache preci-\nsion pairs need to be adapted to quantization modes. More\ndetailed experimental settings and results are available in\nAppendix B and D.1 due to space limitations.",
        "title": "第4页-段落18",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_117",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5828750133514404,
        "probabilities": {
          "human": 0.5828750133514404,
          "aigc": 0.4171249270439148
        },
        "text": "4.1. Error Accumulation",
        "title": "第4页-段落19",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_118",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999796450138092,
        "probabilities": {
          "human": 0.00020353677973616868,
          "aigc": 0.999796450138092
        },
        "text": "Due to the sequential nature of LLMs along both the model\nlayer and token sequence dimensions, the previous layer\noutput with KV cache quantization errors is the input of the\ncurrent layer and the previous step model output token with\nerrors is the input of the input and subsequent transformer\nlayers. Therefore, KV cache quantization leads to two-\ndimensional error accumulation. The error in the l-th layer\nand i-th token el\ni depends on previous 1 ∼l −1 layers and\n1 ∼i −1 steps, as defined in",
        "title": "第4页-段落20",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_119",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5933805704116821,
        "probabilities": {
          "human": 0.40661942958831787,
          "aigc": 0.5933805704116821
        },
        "text": "el\ni = fe(e1:l−1\ni\n, e1:L\ni−1, · · · , e1:L\n1\n).\n(3)",
        "title": "第4页-段落21",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_120",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8661267161369324,
        "probabilities": {
          "human": 0.13387323915958405,
          "aigc": 0.8661267161369324
        },
        "text": "4.3. Why Key Cache Is Generally More Important?",
        "title": "第4页-段落22",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_121",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998045563697815,
        "probabilities": {
          "human": 0.00019542391237337142,
          "aigc": 0.9998045563697815
        },
        "text": "The KV cache quantization error of a single token and layer\nmay be ignorable. However, the error accumulation over the\nwhole model and long context length is noticeable and may\nlead to token flipping and generation error, which is similar\nto model quantization (Lee et al., 2024a). The error accu-\nmulation caused by low-precision KV cache quantization\nis a general problem in domain knowledge QA, AI Gener-\nated Contents (AIGC), coding, and mathematical reasoning\ntasks, which may lead to critical factual errors and loss of\ninstruction following ability.",
        "title": "第4页-段落23",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_122",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997323155403137,
        "probabilities": {
          "human": 0.00026772060664370656,
          "aigc": 0.9997323155403137
        },
        "text": "We discover the diverse model and transformer layer sensi-\ntivity to KV cache quantization mode and pairs, which is\nmainly caused by attention distribution shift as in Figure 2.\nIn this section, we thus analyze the reason why key cache\nis normally more important than value cache from both the\nempirical and theoretical perspectives.",
        "title": "第4页-段落24",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_123",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9172338247299194,
        "probabilities": {
          "human": 0.9172338247299194,
          "aigc": 0.08276616781949997
        },
        "text": "1e\n5",
        "title": "第4页-段落25",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_124",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995079040527344,
        "probabilities": {
          "human": 0.9995079040527344,
          "aigc": 0.0004921150975860655
        },
        "text": "0.0005",
        "title": "第4页-段落26",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_125",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995154142379761,
        "probabilities": {
          "human": 0.9995154142379761,
          "aigc": 0.0004845462099183351
        },
        "text": "0.0020",
        "title": "第4页-段落27",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_126",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999617338180542,
        "probabilities": {
          "human": 0.999617338180542,
          "aigc": 0.0003826090833172202
        },
        "text": "0.0018",
        "title": "第4页-段落28",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_127",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898854494094849,
        "probabilities": {
          "human": 0.9898854494094849,
          "aigc": 0.010114525444805622
        },
        "text": "3.0",
        "title": "第4页-段落29",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_128",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995656609535217,
        "probabilities": {
          "human": 0.9995656609535217,
          "aigc": 0.0004343086911831051
        },
        "text": "0.0004",
        "title": "第4页-段落30",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_129",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993894100189209,
        "probabilities": {
          "human": 0.9993894100189209,
          "aigc": 0.000610548653639853
        },
        "text": "0.0016",
        "title": "第4页-段落31",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_130",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第4页-段落32",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_131",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第4页-段落33",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_132",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第4页-段落34",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_133",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第4页-段落35",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_134",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996699094772339,
        "probabilities": {
          "human": 0.9996699094772339,
          "aigc": 0.00033006552257575095
        },
        "text": "0.0014",
        "title": "第4页-段落36",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_135",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994980096817017,
        "probabilities": {
          "human": 0.9994980096817017,
          "aigc": 0.0005019403761252761
        },
        "text": "0.0003",
        "title": "第4页-段落37",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_136",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第4页-段落38",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_137",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997007846832275,
        "probabilities": {
          "human": 0.9997007846832275,
          "aigc": 0.0002992149966303259
        },
        "text": "0.0012",
        "title": "第4页-段落39",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_138",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999698281288147,
        "probabilities": {
          "human": 0.0003017897251993418,
          "aigc": 0.999698281288147
        },
        "text": "Accumulated errors and intermediate token flipping can ren-\nder the entire mathematical and logical reasoning process\nineffective, resulting in unnecessary computational over-\nhead in long-context reasoning models like OpenAI o1. As\ndemonstrated in Table 1, KIVI-4 has exactly the same re-\nsponse with half-precision KV cache of an example from\nthe GSM8K 15-shot dataset, while the first three generated\nsentences with low-precision KIVI-2 are highly similar to\noriginal generation except for minor differences. Addition-\nally, there is a small token flipping from −to +, which\nleads to the arithmetic operation error in the fourth sen-\ntence with KIVI-2. The wrong 20 + 4 + 4 = 28 instead of\n20 −4 −4 = 12 finally leads to the arithmetic error 28/20 =\n«28/20=14»14% and the completely wrong final answer 14.",
        "title": "第4页-段落40",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_139",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996285438537598,
        "probabilities": {
          "human": 0.9996285438537598,
          "aigc": 0.00037139817140996456
        },
        "text": "0.0010",
        "title": "第4页-段落41",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_140",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第4页-段落42",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_141",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996066689491272,
        "probabilities": {
          "human": 0.9996066689491272,
          "aigc": 0.0003933655098080635
        },
        "text": "0.0002",
        "title": "第4页-段落43",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_142",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995049238204956,
        "probabilities": {
          "human": 0.9995049238204956,
          "aigc": 0.0004950642469339073
        },
        "text": "0.0008",
        "title": "第4页-段落44",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_143",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第4页-段落45",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_144",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992005228996277,
        "probabilities": {
          "human": 0.9992005228996277,
          "aigc": 0.0007995329797267914
        },
        "text": "0.0006",
        "title": "第4页-段落46",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_145",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996529817581177,
        "probabilities": {
          "human": 0.9996529817581177,
          "aigc": 0.00034700107062235475
        },
        "text": "0.0001",
        "title": "第4页-段落47",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_146",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995656609535217,
        "probabilities": {
          "human": 0.9995656609535217,
          "aigc": 0.0004343086911831051
        },
        "text": "0.0004",
        "title": "第4页-段落48",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_147",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第4页-段落49",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_148",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第4页-段落50",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_149",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第4页-段落51",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_150",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第4页-段落52",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_151",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.996701180934906,
        "probabilities": {
          "human": 0.996701180934906,
          "aigc": 0.0032988518942147493
        },
        "text": "(a) K8 ea 1.8×10−5",
        "title": "第4页-段落53",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_152",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948786497116089,
        "probabilities": {
          "human": 0.9948786497116089,
          "aigc": 0.005121318623423576
        },
        "text": "(b) K4 ea 2.5×10−4",
        "title": "第4页-段落54",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_153",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9962002635002136,
        "probabilities": {
          "human": 0.9962002635002136,
          "aigc": 0.0037997260224074125
        },
        "text": "(c) K2 ea 1.2×10−3",
        "title": "第4页-段落55",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_154",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.998989999294281,
        "probabilities": {
          "human": 0.0010099943028762937,
          "aigc": 0.998989999294281
        },
        "text": "Figure 3: Layer-wise attention score error of per-token-\nasym KV cache quantization with simulated offline quanti-\nzation and dequantization (without error accumulation) of\nthe Llama-3.1-8B-Instruct model and the first 20 prompts\nin the zero-shot GSM8K dataset.",
        "title": "第4页-段落56",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_155",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9977201819419861,
        "probabilities": {
          "human": 0.002279757522046566,
          "aigc": 0.9977201819419861
        },
        "text": "Intermediate Attention Errors. Following the settings\nin Table 9, we visualize the simulated layer-wise attention\nscore errors of Llama-3.1-8B-Instruct with the per-token-",
        "title": "第4页-段落57",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_156",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9662643074989319,
        "probabilities": {
          "human": 0.9662643074989319,
          "aigc": 0.0337357223033905
        },
        "text": "4",
        "title": "第4页-段落58",
        "page_number": 4,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_157",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第5页-段落1",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_158",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9562584757804871,
        "probabilities": {
          "human": 0.04374152421951294,
          "aigc": 0.9562584757804871
        },
        "text": "Table 3: Layer-wise relative attention output error (eo)\nof per-token-asym KV Quant. method on Llama-3.1-8B-\nInstruct on the first 20 prompts from the GSM8K dataset.",
        "title": "第5页-段落2",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_159",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996377229690552,
        "probabilities": {
          "human": 0.000362283579306677,
          "aigc": 0.9996377229690552
        },
        "text": "table exceptions: Qwen2.5-{7B, Math-7B}-Instruct. These\ntwo LLMs are sensitive even to int4 key cache quantization,\nindicating a lower tolerance for precision reduction. Based\non these findings, we conclude that the key cache plays a\nmore critical role than the value cache during quantization.\nThis characteristic can be leveraged to optimize memory\nusage while maintaining model effectiveness.",
        "title": "第5页-段落3",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_160",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9793490171432495,
        "probabilities": {
          "human": 0.9793490171432495,
          "aigc": 0.020650973543524742
        },
        "text": "Precision\nKV8\nK8V4\nK8V2\nK4V8\nKV4\nK4V2\nK2V8\nK2V4\nKV2",
        "title": "第5页-段落4",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_161",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5139592289924622,
        "probabilities": {
          "human": 0.48604074120521545,
          "aigc": 0.5139592289924622
        },
        "text": "Relative Attention Output Error (eo)\n0.014\n0.100\n0.401\n0.168\n0.207\n0.453\n0.882\n0.892\n0.962",
        "title": "第5页-段落5",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_162",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996416568756104,
        "probabilities": {
          "human": 0.0003583701909519732,
          "aigc": 0.9996416568756104
        },
        "text": "asym KV cache quantization mode in Figure 3. More results\nof diverse LLMs and datasets are available in Appendix F.\nDecreasing the key cache quantization precision from 8-bit\nto 4-bit and from 4-bit to 2-bit leads to 13.9× and 4.6×\naverage attention score error degradation in Figure 3, re-\nspectively. It may result in attention distribution shift in the\ntoken levels of specific sensitive heads as in Figure 2 and\nthus degrade the final accuracy. A similar phenomenon oc-\ncurs in the final output token probability when implementing\nKV cache eviction (Adnan et al., 2024).",
        "title": "第5页-段落6",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_163",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9002086520195007,
        "probabilities": {
          "human": 0.09979132562875748,
          "aigc": 0.9002086520195007
        },
        "text": "4.4. Correlation of KV Quantization Errors and\nAttention Patterns",
        "title": "第5页-段落7",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_164",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997544884681702,
        "probabilities": {
          "human": 0.0002455422072671354,
          "aigc": 0.9997544884681702
        },
        "text": "As shown in Figure 4, heads with high KV cache quantiza-\ntion errors typically exhibit non-sparse attention patterns.\nThe sparsity patterns of the attention heads are correlated\nwith the head-wise and layer-wise sensitivity to KV cache\nquantization, Highly sparse streaming heads are generally\nmore robust to KV cache quantization than retrieval heads.\nThe proof of Lemma 1 is available in Appendix A.",
        "title": "第5页-段落8",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_165",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999782145023346,
        "probabilities": {
          "human": 0.0002178694703616202,
          "aigc": 0.999782145023346
        },
        "text": "As shown in Table 3, the relative attention output errors\nof high-precision key cache quantization with the same\noverall memory usage e.g. K4V2 is significantly lower than\nthe high-precision value quantization e.g. K2V4, which\nempirically validates that key cache is more important than\nvalue cache during KV cache quantization of intermediate\ntransformer layers. More detailed experiment setting and\nresults can be found in Figure 13 and 14.",
        "title": "第5页-段落9",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_166",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9925594329833984,
        "probabilities": {
          "human": 0.007440558169037104,
          "aigc": 0.9925594329833984
        },
        "text": "Lemma 1. Only attention heads with sparse and concen-\ntrated patterns demonstrate consistent robustness to low-\nprecision KV cache quantization.",
        "title": "第5页-段落10",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_167",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995563626289368,
        "probabilities": {
          "human": 0.00044359316234476864,
          "aigc": 0.9995563626289368
        },
        "text": "The optimal strategy to mitigate attention shift and enhance\naccuracy is to increase key quantization precision, specif-\nically reducing q∆K in highly sensitive layers. This ap-\nproach is recommended when dynamic fine-grained token or\npage-level KV cache quantization for better accuracy is not\nfeasible, as such methods remain challenging to implement\non existing hardware.",
        "title": "第5页-段落11",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_168",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994081258773804,
        "probabilities": {
          "human": 0.0005918507231399417,
          "aigc": 0.9994081258773804
        },
        "text": "Final Generation Errors. We also study the final LLM\ngeneration performance with error accumulation enabled\nduring decoding. Low-precision KV cache in all intermedi-\nate layers are quantized with the same KV precision pairs\nsuch as K8V4 and K4V2. We utilize the KIVI implemen-\ntation with the HQQ backend in huggingface transformers\nv4.46.2 (Wolf et al., 2020), which supports popular LLMs\nwith different scales and proposes, and measure the word-\nperplexity with lm-evaluation-harness (Gao et al., 2024) in\nTable 2.",
        "title": "第5页-段落12",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_169",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第5页-段落13",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_170",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第5页-段落14",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_171",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9945218563079834,
        "probabilities": {
          "human": 0.9945218563079834,
          "aigc": 0.005478155333548784
        },
        "text": "BF16\nKV8\nKV4\nKV2",
        "title": "第5页-段落15",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_172",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9945218563079834,
        "probabilities": {
          "human": 0.9945218563079834,
          "aigc": 0.005478155333548784
        },
        "text": "BF16\nKV8\nKV4\nKV2",
        "title": "第5页-段落16",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_173",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第5页-段落17",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_174",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第5页-段落18",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_175",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第5页-段落19",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_176",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5999752283096313,
        "probabilities": {
          "human": 0.5999752283096313,
          "aigc": 0.40002480149269104
        },
        "text": "Attention score",
        "title": "第5页-段落20",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_177",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5999752283096313,
        "probabilities": {
          "human": 0.5999752283096313,
          "aigc": 0.40002480149269104
        },
        "text": "Attention score",
        "title": "第5页-段落21",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_178",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第5页-段落22",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_179",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第5页-段落23",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_180",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第5页-段落24",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_181",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第5页-段落25",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_182",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第5页-段落26",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_183",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第5页-段落27",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_184",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第5页-段落28",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_185",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9965678453445435,
        "probabilities": {
          "human": 0.9965678453445435,
          "aigc": 0.003432193072512746
        },
        "text": "0.00",
        "title": "第5页-段落29",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_186",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8567771315574646,
        "probabilities": {
          "human": 0.8567771315574646,
          "aigc": 0.1432228684425354
        },
        "text": "0\n10\n20\n30\n40\n50\n60\n70\nKey position",
        "title": "第5页-段落30",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_187",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8567771315574646,
        "probabilities": {
          "human": 0.8567771315574646,
          "aigc": 0.1432228684425354
        },
        "text": "0\n10\n20\n30\n40\n50\n60\n70\nKey position",
        "title": "第5页-段落31",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_188",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995405673980713,
        "probabilities": {
          "human": 0.00045950498315505683,
          "aigc": 0.9995405673980713
        },
        "text": "As shown in Table 2, both KV8 and K8V4 quantization\ndemonstrate similar perplexity levels across all models. Sim-\nilarly, KV4 and K4V2 quantization demonstrate comparable\npatterns. These results suggest that we can achieve equiva-\nlent performance using either 6-bit (K8V4) or 3-bit (K4V2)\nKV cache quantization while maintaining accuracy levels\nsimilar to those of KV8 or KV4 quantization, respectively.\nIn contrast, K4V8 and K2V4 quantizations lead to substan-\ntial increases in perplexity scores, resulting in significant\ndegradation of generation quality. A noticeable decline\nin generation quality occurs when reducing the precision\nof the key cache rather than the value cache. The 5-bit\nK8V2 precision pair achieves performance equal to or better\nthan the higher 6-bit K4V8 precision pair while achieving\nan additional 12.5% reduction in memory usage. These\nLLMs demonstrate varying levels of sensitivity to KV cache\nquantization. Most models experience significant perplexity\nincreases only with int2 key cache quantization, with two no-",
        "title": "第5页-段落32",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_189",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9772697687149048,
        "probabilities": {
          "human": 0.9772697687149048,
          "aigc": 0.022730208933353424
        },
        "text": "(a) Layer-2 streaming head",
        "title": "第5页-段落33",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_190",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9405239224433899,
        "probabilities": {
          "human": 0.9405239224433899,
          "aigc": 0.05947605520486832
        },
        "text": "(b) Layer-13 retrieval head",
        "title": "第5页-段落34",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_191",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5508498549461365,
        "probabilities": {
          "human": 0.5508498549461365,
          "aigc": 0.4491501450538635
        },
        "text": "Figure 4:\nToken-level attention distribution shift with\nthe per-token-asym key cache quantization(Llama-3.1-8B-\nInstruct, GSM8k)",
        "title": "第5页-段落35",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_192",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.802390992641449,
        "probabilities": {
          "human": 0.802390992641449,
          "aigc": 0.19760900735855103
        },
        "text": "4.5. Layer-Wise Sensitivity to KV Cache Quantization",
        "title": "第5页-段落36",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_193",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999729335308075,
        "probabilities": {
          "human": 0.00027067444170825183,
          "aigc": 0.999729335308075
        },
        "text": "According to the layer-wise attention score and relative out-\nput errors of different prompts and KV cache quantization\nprecision pairs of Llama-3.1-8B-Instruct in Figure 3 and\n13, transformer layers sensitive to KV cache quantization\nremain consistent across different input prompts. The ob-\nserved shifts in layer-wise error distribution primarily stem\nfrom variations in key cache quantization precision. Both\nQwen2.5-7B-Instruct and Mistral-7B-Instruct-v0.3 exhibit\nsimilar behavioral patterns in this respect. Further analysis\nresults can be found in Appendix F. We can thus conclude",
        "title": "第5页-段落37",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_194",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9590485692024231,
        "probabilities": {
          "human": 0.9590485692024231,
          "aigc": 0.04095141589641571
        },
        "text": "5",
        "title": "第5页-段落38",
        "page_number": 5,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_195",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第6页-段落1",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_196",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8442866802215576,
        "probabilities": {
          "human": 0.15571331977844238,
          "aigc": 0.8442866802215576
        },
        "text": "fm(P) =\nP(P)",
        "title": "第6页-段落2",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_197",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.866977334022522,
        "probabilities": {
          "human": 0.1330227255821228,
          "aigc": 0.866977334022522
        },
        "text": "that layer-wise sensitivity to KV cache quantization is an\ninherent characteristic of LLMs.",
        "title": "第6页-段落3",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_198",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9989663362503052,
        "probabilities": {
          "human": 0.0010337175335735083,
          "aigc": 0.9989663362503052
        },
        "text": "2L\ncaptures the average equivalent quanti-\nzation bits of all KV cache, fa(P) = ALLM(KVhalf) −\nALLM(KVP) measures the final LLM accuracy loss with\nthe KV precision as P compared with LLM inference us-\ning 16-bit half precision KV cache. For instance, we can\nlimit the average KV cache quantization precision to 2.5-bit,\nwhile optimizing the equivalent quantization precision and\ninference accuracy.",
        "title": "第6页-段落4",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_199",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998496770858765,
        "probabilities": {
          "human": 0.0001503037492511794,
          "aigc": 0.9998496770858765
        },
        "text": "KV cache quantization errors are accumulated over both\nthe model layer and generation sequence dimensions, and\nthe sensitive layer will further amplify errors and lead to\ndramatic model performance degradation. We can perform\nan offline search to identify the optimal coarse-grained KV\ncache quantization configuration, determining the most ef-\nfective precision pairs for each layer, particularly for sensi-\ntive layers, to achieve a balance between memory reduction\nand generation efficiency without incurring any overhead\nduring online inference.",
        "title": "第6页-段落5",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_200",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9517196416854858,
        "probabilities": {
          "human": 0.9517196416854858,
          "aigc": 0.048280421644449234
        },
        "text": "5.2. Framework",
        "title": "第6页-段落6",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_201",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996882677078247,
        "probabilities": {
          "human": 0.00031174885225482285,
          "aigc": 0.9996882677078247
        },
        "text": "To reduce the overhead of online fine-grained KV cache\nmixed-precision quantization tuning, we propose offline\ncalibration of the optimal coarse-grained KV cache quan-\ntization precision pairs for each layer or head using multi-\nobjective optimization algorithms (Akiba et al., 2019; Zhang\n& Li, 2007). These pre-calibrated settings are then directly\napplied during online quantization. The efficiency of of-\nfline calibration is crucial for practical applications due to\nthe large combinatorial search space of KV cache quanti-\nzation pairs across multiple transformer layers. Therefore,\nas demonstrated in Figure 1, we propose the intra-layer and\ninter-layer search space pruning algorithms to accelerate the\nsearch process while preserving optimization opportunities.\nAfter the efficient preprocessing, the final LLM inference\naccuracy is utilized to search the Pareto optimal layer-wise\nKV precision pairs P capturing complex dependencies of\nthe nonlinear error accumulation.",
        "title": "第6页-段落7",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_202",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9753583073616028,
        "probabilities": {
          "human": 0.9753583073616028,
          "aigc": 0.024641651660203934
        },
        "text": "5. Method",
        "title": "第6页-段落8",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_203",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994100332260132,
        "probabilities": {
          "human": 0.0005899801035411656,
          "aigc": 0.9994100332260132
        },
        "text": "KVTuner is an adaptive tuning framework for hardware-\nfriendly mixed-precision KV cache quantization. It opti-\nmizes layer-wise KV precision pairs by considering their\ninherent sensitivity properties, aiming to achieve a better\ntrade-off between inference efficiency and model accuracy.",
        "title": "第6页-段落9",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_204",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997865557670593,
        "probabilities": {
          "human": 0.00021348943118937314,
          "aigc": 0.9997865557670593
        },
        "text": "Instead of making online decisions about fine-grained token\nor page-level KV cache quantization precision for improved\nmodel accuracy, we conduct offline search to identify the\nPareto-optimal quantization precision settings for coarse-\ngrained KV cache in each transformer layer using multi-\nobjective optimization algorithms. Here, we refer to the\nentire low-bit KV cache being quantized with a specific pre-\ncision pair, such as K8V4 or K4V2. This approach ensures\nthat no additional overhead is introduced during dynamic\nquantization and online inference. Due to the flexibility\nintroduced by layer-wise KV cache quantization precision\ntuning, KVTuner is able to accommodate more hardware\nand accuracy constraints of different deployed LLMs com-\npared to uniform 8-bit or even lower precision quantization.\nMoreover, KVTuner accelerates LLM inference and reduces\nmemory footprint, while still maintaining lossless or slightly\nlossy final model generation.",
        "title": "第6页-段落10",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_205",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5472046732902527,
        "probabilities": {
          "human": 0.4527952969074249,
          "aigc": 0.5472046732902527
        },
        "text": "5.3. Automatic Layer-Wise KV Cache Quantization\nPrecision Pair Search",
        "title": "第6页-段落11",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_206",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998084902763367,
        "probabilities": {
          "human": 0.00019158050417900085,
          "aigc": 0.9998084902763367
        },
        "text": "As analyzed in Section 4.2 and 4.3, the model-wise and\nlayer-wise sensitivity to KV cache quantization mode and\nprecision is the inherent model property and is independent\nof the input prompts. Therefore, we can search for the\noptimal layer-wise KV cache quantization precision pairs\noffline to eliminate the additional online decision-making\noverhead with high generalization. If the candidate layer-\nwise KV precision pairs are {2, 4, 8} × {2, 4, 8}, then the\nnumber of possible combinations is 9L, where the L is the\nnumber of transformer layers. For example, the Llama-\n3.1-8B-Instruct model with 32 layers has about 3.4 × 1030,\nwhich is intractable. Therefore, we design the following\ntwo-level search space pruning algorithm to reduce P from\nSL to Sp\nG, where Sp is the pruned candidate set in a group\nand G is the number of clustered layer groups.",
        "title": "第6页-段落12",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_207",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9654083847999573,
        "probabilities": {
          "human": 0.9654083847999573,
          "aigc": 0.034591611474752426
        },
        "text": "5.1. Problem Formulation",
        "title": "第6页-段落13",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_208",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999661922454834,
        "probabilities": {
          "human": 0.0003381289716344327,
          "aigc": 0.999661922454834
        },
        "text": "The offline layer-wise KV precision pair tuning problem\ncan be formulated as a discrete combinatorial optimization\ntask, considering hardware limitations and accuracy loss\nconstraints. It can be solved using multi-objective optimiza-\ntion algorithms. We aim to minimize the quantized KV\ncache memory usage across all transformer layers while\nminimizing the final model accuracy loss, subject to the\nmaximum M memory and ∆A accuracy loss constraints:",
        "title": "第6页-段落14",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_209",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.974699079990387,
        "probabilities": {
          "human": 0.974699079990387,
          "aigc": 0.02530098520219326
        },
        "text": "INTRA-LAYER KV CACHE QUANTIZATION PRECISION\nPAIR PRUNING",
        "title": "第6页-段落15",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_210",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6443448066711426,
        "probabilities": {
          "human": 0.6443448066711426,
          "aigc": 0.35565516352653503
        },
        "text": "min\nP (fm(P), fa(P)) s.t. fm(P) ≤M, fa(P) ≤∆A, (4)",
        "title": "第6页-段落16",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_211",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997444748878479,
        "probabilities": {
          "human": 0.00025549143902026117,
          "aigc": 0.9997444748878479
        },
        "text": "KV cache quantization errors in each layer accumulate\nacross both the model layers and generation token dimen-\nsions. Therefore, we must control the layer-wise error by\npruning KV cache quantization pairs to limit the final model",
        "title": "第6页-段落17",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_212",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9983166456222534,
        "probabilities": {
          "human": 0.0016834338894113898,
          "aigc": 0.9983166456222534
        },
        "text": "where the search space P ∈SL is the KV cache precision\npairs in L layers. The layer-wise search space S is defined\nas the KV cache precision pair (P l\nk, P l\nv) in the l-th layer.",
        "title": "第6页-段落18",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_213",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9290469288825989,
        "probabilities": {
          "human": 0.9290469288825989,
          "aigc": 0.07095304131507874
        },
        "text": "6",
        "title": "第6页-段落19",
        "page_number": 6,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_214",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第7页-段落1",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_215",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997456669807434,
        "probabilities": {
          "human": 0.00025432099937461317,
          "aigc": 0.9997456669807434
        },
        "text": "Table 4: Intra-layer KV cache quantization precision pair\npruning results of special transformer layers. The pruned\nPareto efficient KV cache precision pairs in most layers are\n{KV8, K8V4, KV4, K4V2, KV2}, so we omit them in the\ntable. Value is always quantized with the per-token-asym\nmode. G1 of Mistral-7B-Instruct-v0.3 is 2∼4, 6, 7∼10,\n14, 18, 27, and 29. G2 of Qwen2.5-32B-Instruct is 5 ∼\n10, 12, 14, 16, 18 ∼21, 23, 26 ∼28, and 32.",
        "title": "第7页-段落2",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_216",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998310804367065,
        "probabilities": {
          "human": 0.00016887449601199478,
          "aigc": 0.9998310804367065
        },
        "text": "error. For all candidate KV cache quantization pairs in each\nlayer, we prune those that are not part of the Pareto frontier,\nconsidering both the equivalent KV cache quantization pre-\ncision and the relative attention output errors. For example,\nthe precision pairs KV8, K8V4, KV4, K4V2, and KV2 are\nPareto efficient for most layers in Llama-3.1-8B-Instruct in\nFigure 13, except for the 0-th layer, where K4V8 results in\nsmaller errors than K8V4.",
        "title": "第7页-段落3",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_217",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6411816477775574,
        "probabilities": {
          "human": 0.6411816477775574,
          "aigc": 0.358818382024765
        },
        "text": "Model name\nL\nKey quant. mode\nKV cache precision pairs\nLayer ids",
        "title": "第7页-段落4",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_218",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986509680747986,
        "probabilities": {
          "human": 0.9986509680747986,
          "aigc": 0.001349032623693347
        },
        "text": "INTER-LAYER CLUSTERING",
        "title": "第7页-段落5",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_219",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999704897403717,
        "probabilities": {
          "human": 0.999704897403717,
          "aigc": 0.00029508903389796615
        },
        "text": "Llama-3.1-8B-Instruct\n32\nper-token-asym\nKV8, K4V8, KV4, K4V2, KV2\n0",
        "title": "第7页-段落6",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_220",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991596937179565,
        "probabilities": {
          "human": 0.9991596937179565,
          "aigc": 0.0008402825333178043
        },
        "text": "per-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0\nKV8, K4V8, KV4, K4V2, KV2\n1, 2, 3, 7, 29, 31",
        "title": "第7页-段落7",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_221",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992387294769287,
        "probabilities": {
          "human": 0.0007612736080773175,
          "aigc": 0.9992387294769287
        },
        "text": "Although the above intra-layer pruning already significantly\nreduces the search space to Sp\nL such as 532 ≈2.3×1022 in\nLlama-3.1-8B-Instruct, it is still too computationally costly\nfor searching. Therefore, we further propose the inter-layer\nclustering algorithm based on relative attention output errors\nand the pruned candidate KV quantization pairs to Sp\nG",
        "title": "第7页-段落8",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_222",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999725878238678,
        "probabilities": {
          "human": 0.999725878238678,
          "aigc": 0.00027406346634961665
        },
        "text": "Mistral-7B-Instruct-v0.3\n32\nper-token-asym\nKV8, K4V8, KV4, K2V4, KV2\n0",
        "title": "第7页-段落9",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_223",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993888139724731,
        "probabilities": {
          "human": 0.9993888139724731,
          "aigc": 0.0006111850379966199
        },
        "text": "per-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0\nKV8, K4V8, KV4, K4V2, KV2\nG1",
        "title": "第7页-段落10",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_224",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991410970687866,
        "probabilities": {
          "human": 0.9991410970687866,
          "aigc": 0.0008588343043811619
        },
        "text": "Qwen2.5-3B-Instruct\n36\nper-token-asym\nKV8, K8V4, K8V2, K4V2, KV2\n0\nKV8, K8V4, K8V2, KV4, K4V2, KV2\n18, 27, 29",
        "title": "第7页-段落11",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_225",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989286065101624,
        "probabilities": {
          "human": 0.9989286065101624,
          "aigc": 0.001071430742740631
        },
        "text": "per-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0, 1, 2, 4, 34, 35\nKV8, K4V8, KV4, K4V2, KV2\n3, 6, 11, 13, 23",
        "title": "第7页-段落12",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_226",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.997718870639801,
        "probabilities": {
          "human": 0.997718870639801,
          "aigc": 0.00228105834685266
        },
        "text": "Qwen2.5-7B-Instruct\n28\nper-token-asym\nKV8, K8V4, K8V2, K4V2, KV2\n0\nKV8, K8V4, K8V2, KV4, K4V2, KV2\n3, 13, 27\nper-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0, 1, 2, 3\nKV8, K4V8, KV4, K4V2, KV2\n6",
        "title": "第7页-段落13",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_227",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998277425765991,
        "probabilities": {
          "human": 0.0001722503366181627,
          "aigc": 0.9998277425765991
        },
        "text": "such as 56 = 15625. The initial step involves partitioning\nlayers based on distinct candidate sets of pruned KV cache\nquantization precision pairs. These candidate sets serve\nas indicators of how individual layers respond differently\nto specific KV cache quantization precision configurations.\nThe subsequent step involves clustering layers that share\nthe same candidate set, using quantization sensitivity as\nthe clustering metric. This sensitivity is quantified with\nthe relative attention output errors produced by the pruned\nprecision pairs.",
        "title": "第7页-段落14",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_228",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998144507408142,
        "probabilities": {
          "human": 0.9998144507408142,
          "aigc": 0.0001855495647760108
        },
        "text": "Qwen2.5-14B-Instruct\n48\nper-token-asym\nNone",
        "title": "第7页-段落15",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_229",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989135265350342,
        "probabilities": {
          "human": 0.9989135265350342,
          "aigc": 0.0010864388896152377
        },
        "text": "per-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0, 1, 2, 3, 4\nKV8, K4V8, KV4, K4V2, KV2\n5, 6, 8, 9, 12",
        "title": "第7页-段落16",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_230",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9982470273971558,
        "probabilities": {
          "human": 0.9982470273971558,
          "aigc": 0.001753005781210959
        },
        "text": "per-token-asym\nNone",
        "title": "第7页-段落17",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_231",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990069270133972,
        "probabilities": {
          "human": 0.9990069270133972,
          "aigc": 0.0009930884698405862
        },
        "text": "per-channel-asym\nKV8, K4V8, KV4, K2V4, KV2\n0, 1, 2, 3, 4, 11\nKV8, K4V8, KV4, K4V2, KV2\nG2\nKV8, K8V4, KV4, K2V4, KV2\n63",
        "title": "第7页-段落18",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_232",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997811913490295,
        "probabilities": {
          "human": 0.9997811913490295,
          "aigc": 0.000218850516830571
        },
        "text": "Qwen2.5-32B-Instruct\n64",
        "title": "第7页-段落19",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_233",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9029906392097473,
        "probabilities": {
          "human": 0.9029906392097473,
          "aigc": 0.09700937569141388
        },
        "text": "6.1. Pareto-Optimal KV Cache Precision Pair Search",
        "title": "第7页-段落20",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_234",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9987524747848511,
        "probabilities": {
          "human": 0.0012474973918870091,
          "aigc": 0.9987524747848511
        },
        "text": "KIVI. The mixed precision KIVI quantization mode can\nmaintain high accuracy. As shown in Figure 5a, KVTuner\nwith KIVI effectively maintains Llama-3.1-8B-Instruct per-\nformance while reducing the equivalent quantization preci-\nsion to 3.06-bit. In addition, KVTuner also finds out four\nsettings including lower-precision 4.91-bit in the Pareto\nfrontier whose memory usage and accuracy are better than\nKV8. Most sampled settings are close to the Pareto fron-\ntier, indicating that Llama-3.1-8B-Instruct is more robust\nto low-precision KV quantization. These demonstrate that\nKVTuner increases the flexibility of KV cache quantization\nand can achieve lower precision and even better precision\nthan uniform KV precision.",
        "title": "第7页-段落21",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_235",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974325299263,
        "probabilities": {
          "human": 0.9974325299263,
          "aigc": 0.002567493123933673
        },
        "text": "CALIBRATION DATASET DESIGN",
        "title": "第7页-段落22",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_236",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998113512992859,
        "probabilities": {
          "human": 0.00018863567674998194,
          "aigc": 0.9998113512992859
        },
        "text": "To effectively evaluate different quantization settings, we\ndevelop an approach that amplifies KV cache quantization\nerror accumulation and distinguishes the performance of\nKV precision pairs during the calibration process. This\napproach utilizes dequantized KV cache for self-attention\ncomputation during the prefilling stage, enabling error ac-\ncumulation across model layers. Furthermore, we utilize\nlong-context generation and challenging calibration datasets\nsuch as mathematical reasoning. In these tasks, minor errors\npropagating in decoding steps may result in intermediate\ngeneration token flipping and substantial mistakes in final\nanswers as demonstrated by Table 1.",
        "title": "第7页-段落23",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_237",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9987382292747498,
        "probabilities": {
          "human": 0.0012617619941011071,
          "aigc": 0.9987382292747498
        },
        "text": "Per-token-asym.\nAccording to Figure 5b, when using\nthe per-token-asym quantization mode on the sensitive\nQwen2.5-7B-Instruct model, the Pareto frontier identified\nby KVTuner consistently outperforms uniform precision\nquantization. Especially, KVTuner can achieve KV8 accu-\nracy with the equivalent 3.92-bit KV precision, while the\nuniform KV4 accuracy significantly degrades to around 0%.\nTherefore, even leveraging the simple and commonly used\nper-token-asym mode (Lin et al., 2024b; Sheng et al., 2023),\nKVTuner can reduce the memory footprint with the main-\ntained accuracy of models with high knowledge density.",
        "title": "第7页-段落24",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_238",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5079421997070312,
        "probabilities": {
          "human": 0.5079421997070312,
          "aigc": 0.49205780029296875
        },
        "text": "6. Experimental Results",
        "title": "第7页-段落25",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_239",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997232556343079,
        "probabilities": {
          "human": 0.0002766823163256049,
          "aigc": 0.9997232556343079
        },
        "text": "The detailed experimental settings are available in Section\nC. The intra-layer and inter-layer KV precision pairs prun-\ning results of various LLMs are available in Appendix D.1.\nThe proposed pruning algorithm can significantly reduce\nthe search space to Sp\nG and speedup convergence of MOO\nsearch. The final model accuracy on mathematical reason-\ning datasets and the throughput improvement validate the\neffectiveness of KVTuner.",
        "title": "第7页-段落26",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_240",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993653893470764,
        "probabilities": {
          "human": 0.0006346148438751698,
          "aigc": 0.9993653893470764
        },
        "text": "6.2. Mathematical and Scientific Reasoning Accuracy\nApart from the in-context few-shot GSM8K datasets, we\nalso utilize them as the internal reasoning steps in a multi-\nturn way to imitate OpenAI o1 like reasoning systems in\nTable 5. KIVI-2 and KIVI-4 result in dramatic accuracy loss\nin Qwen2.5-{3B, 7B}-Instruct due to their high sensitivity",
        "title": "第7页-段落27",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_241",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.918914794921875,
        "probabilities": {
          "human": 0.918914794921875,
          "aigc": 0.081085205078125
        },
        "text": "7",
        "title": "第7页-段落28",
        "page_number": 7,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_242",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第8页-段落1",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_243",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9976232647895813,
        "probabilities": {
          "human": 0.0023767235688865185,
          "aigc": 0.9976232647895813
        },
        "text": "Table 6: Scientific reasoning accuracy comparison of dif-\nferent KV cache precision settings with the per-token-asym\nKV quantization mode on the GPQA Extended dataset.",
        "title": "第8页-段落2",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_244",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第8页-段落3",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_245",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第8页-段落4",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_246",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第8页-段落5",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_247",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第8页-段落6",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_248",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第8页-段落7",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_249",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第8页-段落8",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_250",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第8页-段落9",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_251",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第8页-段落10",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_252",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第8页-段落11",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_253",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第8页-段落12",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_254",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第8页-段落13",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_255",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第8页-段落14",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_256",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第8页-段落15",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_257",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第8页-段落16",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_258",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第8页-段落17",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_259",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第8页-段落18",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_260",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第8页-段落19",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_261",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9476805925369263,
        "probabilities": {
          "human": 0.05231942608952522,
          "aigc": 0.9476805925369263
        },
        "text": "Precision\nGPQA Extended\nAverage\nPrecision\nGPQA Extended\nAverage\n5-shot\n10-shot\n20-shot\n5-shot\n10-shot\n20-shot\nLlama-3.1-8B-Instruct\nMistral-7B-Instruct-v0.3\nBF16\n0.3095\n0.3114\n0.2985\n0.3065\nBF16\n0.2930\n0.2784\n0.2766\n0.2827\nKV8\n0.3242\n0.3022\n0.3059\n0.3108\nKV8\n0.2985\n0.2839\n0.2784\n0.2869\nKV4\n0.3095\n0.3168\n0.3077\n0.3113\nKV4\n0.3040\n0.2839\n0.3022\n0.2967\nKV2\n0.1996\n0.2198\n0.2473\n0.2222\nKV2\n0.2857\n0.2106\n0.2344\n0.2436\nKVTuner-C5.43\n0.3187\n0.3077\n0.3187\n0.3150\nKVTuner-C5.38\n0.3004\n0.2839\n0.2912\n0.2918\nKVTuner-C3.59\n0.3223\n0.3205\n0.3059\n0.3162\nKVTuner-C3.78\n0.3260\n0.2857\n0.3040\n0.3052",
        "title": "第8页-段落20",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_262",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第8页-段落21",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_263",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第8页-段落22",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_264",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第8页-段落23",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_265",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第8页-段落24",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_266",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第8页-段落25",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_267",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第8页-段落26",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_268",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第8页-段落27",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_269",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第8页-段落28",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_270",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第8页-段落29",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_271",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第8页-段落30",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_272",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第8页-段落31",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_273",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996644258499146,
        "probabilities": {
          "human": 0.9996644258499146,
          "aigc": 0.0003356066590640694
        },
        "text": "(a)\nLlama-3.1-8B-Instruct\nwith KIVI",
        "title": "第8页-段落32",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_274",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993915557861328,
        "probabilities": {
          "human": 0.9993915557861328,
          "aigc": 0.0006083985208533704
        },
        "text": "(b) Qwen2.5-7B-Instruct with\nper-token-asym",
        "title": "第8页-段落33",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_275",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9641160368919373,
        "probabilities": {
          "human": 0.9641160368919373,
          "aigc": 0.03588399663567543
        },
        "text": "Qwen2.5-3B-Instruct\nQwen2.5-7B-Instruct\nBF16\n0.3059\n0.3095\n0.3150\n0.3101\nBF16\n0.3168\n0.3352\n0.3297\n0.3272\nKV8\n0.3095\n0.3059\n0.3187\n0.3114\nKV8\n0.3242\n0.3333\n0.3407\n0.3327\nKV4\n0.2564\n0.2711\n0.2692\n0.2656\nKV4\n0.0586\n0.0641\n0.0751\n0.0659\nKV2\n0.0971\n0.0806\n0.1026\n0.0934\nKV2\n0.2216\n0.1941\n0.1996\n0.2051\nKVTuner-C5.06\n0.2985\n0.3040\n0.3278\n0.3101\nKVTuner-C5.0\n0.3315\n0.3297\n0.3187\n0.3266\nKVTuner-C3.64\n0.2949\n0.3059\n0.2985\n0.2998\nKVTuner-C4.0\n0.3333\n0.3223\n0.3205\n0.3254",
        "title": "第8页-段落34",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_276",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9971901774406433,
        "probabilities": {
          "human": 0.0028097948525100946,
          "aigc": 0.9971901774406433
        },
        "text": "Figure 5: Pareto frontier on the first 200 GSM8K 4-shot\nprompts. Red points indicates the accuracy of 9 uniform\nlayer-wise KV cache precision pairs including KV8, K8V4,\nK4V8, KV4, K4V2, and K2V4. For Qwen2.5-7B-Instruct,\nwe can easily see that K2V8, KV4, and other lower pre-\ncision pairs lose the capability of mathematical reasoning,\nobtaining around 0% accuracy. However, KVTuner still\nmaintain nearly lossless overall 4-bit KV cache quantiza-\ntion.",
        "title": "第8页-段落35",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_277",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999404788017273,
        "probabilities": {
          "human": 0.0005952368373982608,
          "aigc": 0.999404788017273
        },
        "text": "to low-precision KV quantization. KVTuner with KIVI can\nnearly losslessly quantizate KV cache to 3.92-bit, 3.17-bit,\nand 5.96-bit of the three models, respectively, further re-\nducing the memory footprint compared with KIVI-4 and\nKIVI-8. In addition, we find out an interesting observation:\nKVTuner enables longer context and lower KV precision\nfor better CoT and multi-turn mathematical reasoning ac-\ncuracy than short-context and original BF16 precision KV.\nMost LLMs benefit from longer CoT and KVTuner enables\nnearly lossless lower-precision KV quantization. We ob-\nserve that KVTuner significantly reduces the performance\ngap between the per-token-asym and KIVI quantization\nmodes.",
        "title": "第8页-段落36",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_278",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996669292449951,
        "probabilities": {
          "human": 0.0003330256149638444,
          "aigc": 0.9996669292449951
        },
        "text": "Table 5: Mathematical reasoning accuracy comparison of\ndifferent KV cache precision settings with the KIVI and per-\ntoken-asym quant. mode on the GSM8K few-shot CoT and\nCoT as multiturn dataset. We highlight the average scores\nwith significant accuracy degradation in red and those with\nmoderate accuracy degradation in orange. Notably, for the\nQwen2.5-3B-Instruct model using KIVI quantization mode,\nall configurations within the 4-bit to 6-bit equivalent preci-\nsion range exhibit lower accuracy on the calibration dataset\ncompared to a configuration with an equivalent precision of\n3.44-bit. As a result, we choose this 3.44-bit configuration\nas the highest-accuracy representative for cases where the\nequivalent precision is constrained to ≤6-bit.",
        "title": "第8页-段落37",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_279",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9985804557800293,
        "probabilities": {
          "human": 0.0014195761177688837,
          "aigc": 0.9985804557800293
        },
        "text": "We extend our evaluation to the GPQA dataset with few-\nshot CoTs, as detailed in Table 6. KVTuner successfully\nenables lower than 4-bit, such as 3.59-bit, KV cache quanti-\nzation with minimal performance degradation across various\nmodels. These results demonstrate the effectiveness of our\nmethod in maintaining high mathematical reasoning accu-\nracy while significantly reducing memory usage.",
        "title": "第8页-段落38",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_280",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8231104016304016,
        "probabilities": {
          "human": 0.1768895834684372,
          "aigc": 0.8231104016304016
        },
        "text": "Quant. method\nPrecision\nFew-shot CoT\nFew-shot as multiturn\nAverage\n4-shot\n8-shot\n16-shot\n4-shot\n8-shot\n16-shot\nLlama-3.1-8B-Instruct\nBF16\nBF16\n0.7635\n0.7741\n0.7854\n0.8355\n0.8309\n0.8332\n0.8038",
        "title": "第8页-段落39",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_281",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.603404700756073,
        "probabilities": {
          "human": 0.396595299243927,
          "aigc": 0.603404700756073
        },
        "text": "6.3. Long Context Generation Accuracy",
        "title": "第8页-段落40",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_282",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9943106174468994,
        "probabilities": {
          "human": 0.9943106174468994,
          "aigc": 0.005689320620149374
        },
        "text": "KV8\n0.7635\n0.7710\n0.7908\n0.8340\n0.8302\n0.8279\n0.8029\nKV4\n0.7240\n0.7506\n0.7354\n0.8211\n0.8180\n0.8097\n0.7765\nKV2\n0.0174\n0.019\n0.0250\n0.0167\n0.019\n0.0197\n0.0195\nKVTuner-C5.44\n0.7604\n0.7726\n0.7726\n0.8287\n0.8385\n0.8309\n0.8006\nKVTuner-C3.59\n0.7210\n0.7316\n0.7407\n0.8021\n0.8014\n0.7991\n0.7660",
        "title": "第8页-段落41",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_283",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9927270412445068,
        "probabilities": {
          "human": 0.007272922899574041,
          "aigc": 0.9927270412445068
        },
        "text": "We compare KVTuner on the sensitive Qwen2.5-7B-Instruct\nmodel with the baselines KIVI-8, KIVI-4, our proposed vari-\nant KIVI-K8V4, and per-token-asym ones in the 20 Long-\nBench datasets (Bai et al., 2024). The averaged scores are\navailable in Table 7. KVTuner pushes KV cache quantiza-\ntion for the nearly lossless long context generation to 3.92-\nbit, outperforming the uniform KV precision. KVTuner\nwith both KIVI and per-token-asym quantization methods\nachieve high accuracy and KV compression rates simultane-\nously.",
        "title": "第8页-段落42",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_284",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第8页-段落43",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_285",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956972599029541,
        "probabilities": {
          "human": 0.9956972599029541,
          "aigc": 0.004302737303078175
        },
        "text": "KIVI-8\n0.7733\n0.7748\n0.7756\n0.8347\n0.8317\n0.8294\n0.8033\nKIVI-4\n0.7566\n0.7718\n0.7839\n0.8370\n0.8241\n0.8332\n0.8011\nKIVI-2\n0.6073\n0.6080\n0.5929\n0.6649\n0.6543\n0.6687\n0.6327\nKVTuner-C4.91\n0.7506\n0.7665\n0.7657\n0.8173\n0.8188\n0.8378\n0.7928\nKVTuner-C3.25\n0.7483\n0.7566\n0.7604\n0.8362\n0.8256\n0.8279\n0.7925\nQwen2.5-3B-Instruct\nBF16\nBF16\n0.6020\n0.6490\n0.7020\n0.5679\n0.6005\n0.6490\n0.6284",
        "title": "第8页-段落44",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_286",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第8页-段落45",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_287",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9970792531967163,
        "probabilities": {
          "human": 0.9970792531967163,
          "aigc": 0.002920769853517413
        },
        "text": "KV8\n0.5959\n0.6573\n0.7081\n0.5686\n0.6080\n0.6323\n0.6284\nKV4\n0.1888\n0.1721\n0.2312\n0.2229\n0.2616\n0.2464\n0.2205\nKV2\n0.0099\n0.0121\n0.0106\n0.0106\n0.0091\n0.0129\n0.0109\nKVTuner-C5.06\n0.6058\n0.6664\n0.6823\n0.5914\n0.6133\n0.6490\n0.6347\nKVTuner-C4.00\n0.6156\n0.6482\n0.6672\n0.5815\n0.6118\n0.6422\n0.6278",
        "title": "第8页-段落46",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_288",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第8页-段落47",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_289",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960302710533142,
        "probabilities": {
          "human": 0.9960302710533142,
          "aigc": 0.0039696842432022095
        },
        "text": "KIVI-8\n0.5974\n0.6619\n0.7096\n0.5648\n0.5989\n0.6346\n0.6279\nKIVI-4\n0.6156\n0.6550\n0.7066\n0.5732\n0.6073\n0.6414\n0.6332\nKIVI-2\n0.0546\n0.0576\n0.0675\n0.047\n0.0478\n0.0591\n0.0556\nKVTuner-C3.44\n0.5989\n0.6429\n0.7089\n0.5701\n0.5997\n0.6475\n0.6280\nKVTuner-C3.17\n0.6065\n0.6444\n0.6998\n0.5512\n0.5891\n0.6406\n0.6219\nQwen2.5-7B-Instruct\nBF16\nBF16\n0.8059\n0.8287\n0.8218\n0.7081\n0.7339\n0.7544\n0.7755",
        "title": "第8页-段落48",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_290",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第8页-段落49",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_291",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992215633392334,
        "probabilities": {
          "human": 0.9992215633392334,
          "aigc": 0.0007783981855027378
        },
        "text": "6.4. Throughput",
        "title": "第8页-段落50",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_292",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997374415397644,
        "probabilities": {
          "human": 0.0002624992048367858,
          "aigc": 0.9997374415397644
        },
        "text": "We measure the maximum throughput and the correspond-\ning batch size under specific input prompt length with the\nimplementation of the KIVI GPU kernel, which supports\nLlama series models. We follow the same settings and defi-\nnitions of KIVI. Throughput is defined as the the number of\ntokens generated per second (measured end-to-end, includ-",
        "title": "第8页-段落51",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_293",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9969758987426758,
        "probabilities": {
          "human": 0.9969758987426758,
          "aigc": 0.0030241613276302814
        },
        "text": "KV8\n0.7998\n0.8203\n0.8196\n0.7134\n0.7384\n0.7354\n0.7712\nKV4\n0.0106\n0.0121\n0.0121\n0.003\n0.003\n0.0061\n0.0078\nKV2\n0.0068\n0.0099\n0.0076\n0.0083\n0.0106\n0.0106\n0.0090\nKVTuner-C5.00\n0.7885\n0.8302\n0.8203\n0.6914\n0.7445\n0.7468\n0.7703\nKVTuner-C4.00\n0.7847\n0.8112\n0.7726\n0.6929\n0.7331\n0.7407\n0.7559",
        "title": "第8页-段落52",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_294",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第8页-段落53",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_295",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953122138977051,
        "probabilities": {
          "human": 0.9953122138977051,
          "aigc": 0.0046878173016011715
        },
        "text": "KIVI-8\n0.8021\n0.8271\n0.8302\n0.7066\n0.7354\n0.7506\n0.7753\nKIVI-4\n0.0735\n0.1137\n0.1554\n0.0667\n0.0705\n0.1463\n0.1043\nKIVI-2\n0.0379\n0.0402\n0.0356\n0.0326\n0.0258\n0.0235\n0.0326\nKVTuner-C5.96\n0.8218\n0.8309\n0.8150\n0.6907\n0.7248\n0.7513\n0.7724\nKVTuner-C3.92\n0.5959\n0.6664\n0.6558\n0.5588\n0.6156\n0.6035\n0.6160",
        "title": "第8页-段落54",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_296",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第8页-段落55",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_297",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9457684755325317,
        "probabilities": {
          "human": 0.9457684755325317,
          "aigc": 0.054231490939855576
        },
        "text": "8",
        "title": "第8页-段落56",
        "page_number": 8,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_298",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第9页-段落1",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_299",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993440508842468,
        "probabilities": {
          "human": 0.0006559520261362195,
          "aigc": 0.9993440508842468
        },
        "text": "Table 7: Accuracy comparison between offline searched\nlayer-wise KV cache precision using KVTuner in Table 5\nand 6 and uniform KV precision settings of the sensitive\nQwen2.5-7B-Instruct on 20 LongBench long context gener-\nation benchmarks.",
        "title": "第9页-段落2",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_300",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第9页-段落3",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_301",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第9页-段落4",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_302",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第9页-段落5",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_303",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第9页-段落6",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_304",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第9页-段落7",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_305",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第9页-段落8",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_306",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第9页-段落9",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_307",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第9页-段落10",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_308",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983661770820618,
        "probabilities": {
          "human": 0.9983661770820618,
          "aigc": 0.0016338169807568192
        },
        "text": "KIVI\nBF16\nKV8\nK8V4\nKV4\nKVTuner-C5.96\nKVTuner-C3.92\n0.7956\n0.7992\n0.8001\n0.7723\n0.7956\n0.7903\nPer-token-asym\nBF16\nKV8\nK8V4\nKV4\nKVTuner-C5.0\nKVTuner-C4.0\n0.7956\n0.7971\n0.7953\n0.6343\n0.8005\n0.7960",
        "title": "第9页-段落11",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_309",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第9页-段落12",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_310",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第9页-段落13",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_311",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第9页-段落14",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_312",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第9页-段落15",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_313",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第9页-段落16",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_314",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第9页-段落17",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_315",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.858566164970398,
        "probabilities": {
          "human": 0.14143380522727966,
          "aigc": 0.858566164970398
        },
        "text": "Figure 6: Pareto frontier of Llama-3.1-8B-Instruct with\nthe per-token-asym KV quantization mode and without the\nproposed two-stage search space pruning on the first 200\nGSM8k 4-shot prompts.",
        "title": "第9页-段落18",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_316",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994706511497498,
        "probabilities": {
          "human": 0.9994706511497498,
          "aigc": 0.0005294194561429322
        },
        "text": "ing quantization/dequantization overhead).",
        "title": "第9页-段落19",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_317",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9980218410491943,
        "probabilities": {
          "human": 0.001978130778297782,
          "aigc": 0.9980218410491943
        },
        "text": "The layer-wise KV cache precision tuning in KVTuner are\ncompletely offline and no online overhead for precision se-\nlection is introduced. The model-level efficiency reflects\nthe overall effects of layer-wise efficiency of all KV cache\nprecision pairs. The memory movement cost from CPUs to\nGPUs and from GPU HBM to GPU cache linearly increases\nwith the KV cache size in most case and attention is nor-\nmally memory bounded. We report the total model-level\nthroughput comparison of Llama-3.1-8B-Instruct using the\nsearched configuration in Table 5 as below. Compared with\nKIVI-KV8, KVTuner-C3.25 can improve decoding through-\nput by 16.79%∼21.25%. More efficient KV dequantization\nand attention kernels proposed in Qserve (Lin et al., 2024b)\nand TurboAttention (Kang et al., 2024a) may further en-\nhance the throughout benefit of KVTuner than INT8 KV\nbaselines.",
        "title": "第9页-段落20",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_318",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996154308319092,
        "probabilities": {
          "human": 0.00038449966814368963,
          "aigc": 0.9996154308319092
        },
        "text": "with larger quantization errors. Reducing the quan-\ntization precision of the key for a crucial group of\nlayers can significantly degrade the performance. For\ninstance, in Llama-3.1-8B-Instruct, the layer group\n[8 ∼11, 14 ∼17, 20, 30] is particularly sensitive\nto the reduction of the key precision, and if the pre-\ncision of the key is reduced from 4-bit to 2-bit, the\nperformance would drop from 0.67 to 0.495.",
        "title": "第9页-段落21",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_319",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9619172215461731,
        "probabilities": {
          "human": 0.9619172215461731,
          "aigc": 0.03808273375034332
        },
        "text": "6.6. Ablation Studies",
        "title": "第9页-段落22",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_320",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990565180778503,
        "probabilities": {
          "human": 0.0009434817475266755,
          "aigc": 0.9990565180778503
        },
        "text": "According to Figure 6, when using the per-token-asym\nquantization mode on the Llama-3.1-8B-Instruct model, the\nsearch results deteriorate significantly if the proposed intra-\nlayer and inter-layer search space pruning algorithms are\nnot applied. In comparison with the counterpart with search\nspace pruning as pre-processing in Figure 9a, this highlights\nsearch space pruning is helpful for MOO search conver-\ngence and maintaining quantization performance.",
        "title": "第9页-段落23",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_321",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9922175407409668,
        "probabilities": {
          "human": 0.00778241315856576,
          "aigc": 0.9922175407409668
        },
        "text": "Table 8: Throughput comparison between offline searched\nlayer-wise KV cache precision using KVTuner in Table 5\nand uniform KV precision settings with KIVI of Llama-3.1-\n8B-Instruct.",
        "title": "第9页-段落24",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_322",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995397329330444,
        "probabilities": {
          "human": 0.9995397329330444,
          "aigc": 0.0004602703847922385
        },
        "text": "BS\ninputLen\nKV8(baseline)\nK8V4\nKV4\nK4V2\nKVTuner-C4.91\nKVTuner-C3.25\n64\n128\n3836\n4193\n4567\n4697\n4240 +10.53%\n4652 +21.25%\n16\n512\n1102\n1205\n1275\n1304\n1239 +12.41%\n1296 +17.55%\n8\n1024\n549\n597\n632\n645\n600\n+9.22%\n641 +16.79%",
        "title": "第9页-段落25",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_323",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7832255363464355,
        "probabilities": {
          "human": 0.7832255363464355,
          "aigc": 0.21677443385124207
        },
        "text": "7. Conclusion",
        "title": "第9页-段落26",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_324",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9971938133239746,
        "probabilities": {
          "human": 0.9971938133239746,
          "aigc": 0.002806141972541809
        },
        "text": "6.5. Detailed Analysis",
        "title": "第9页-段落27",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_325",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995627999305725,
        "probabilities": {
          "human": 0.0004372023104224354,
          "aigc": 0.9995627999305725
        },
        "text": "KVTuner enables efficient and adaptive layer-wise mixed-\nprecision KV cache quantization via sensitivity-aware op-\ntimization techniques. It systematically reduces KV cache\nquantization errors by prioritizing key cache precision while\nbalancing memory efficiency and inference accuracy. Exper-\nimental results demonstrate that KVTuner achieves nearly\nlossless compression at 3.25-bit for Llama-3.1-8B-Instruct\nand 4-bit for sensitive Qwen2.5-7B-Instruct. KVTuner also\ndemonstrates that employing longer CoTs with lower and\nmixed precision KV cache quantization yields superior per-\nformance compared to shorter CoTs utilizing higher pre-\ncision KV cache. This improvement is evident in both\nmemory efficiency and accuracy, particularly in the con-\ntext of mathematical reasoning tasks. KVTuner also greatly\nnarrows the performance difference between the simple per-\ntoken-asym and accurate KIVI quantization modes, even\nwhen using overall similar low-precision settings.",
        "title": "第9页-段落28",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_326",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8970857858657837,
        "probabilities": {
          "human": 0.1029142290353775,
          "aigc": 0.8970857858657837
        },
        "text": "By analyzing the detailed configurations in the Pareto fron-\ntier identified for Llama-3.1-8B-Instruct, we observe that:",
        "title": "第9页-段落29",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_327",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.99981290102005,
        "probabilities": {
          "human": 0.00018716549675446004,
          "aigc": 0.99981290102005
        },
        "text": "• In most cases, all layer groups adopt a quantization\nconfiguration where the precision of the key is higher\nthan the precision of the value. This supports our ear-\nlier observation from uniform quantization that the key\nplays a more critical role in quantization.",
        "title": "第9页-段落30",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_328",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999752938747406,
        "probabilities": {
          "human": 0.0002470681502018124,
          "aigc": 0.999752938747406
        },
        "text": "• In other cases, in certain specialized layer groups, the\nvalue is set at a higher precision than the key for certain\nspecialized layer groups. This aligns with the patterns\nidentified in Table 4, which highlight specific layer\ngroups may require higher precision for values.",
        "title": "第9页-段落31",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_329",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.684237539768219,
        "probabilities": {
          "human": 0.684237539768219,
          "aigc": 0.3157624304294586
        },
        "text": "• KVTuner tends to allocate higher precision to groups",
        "title": "第9页-段落32",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_330",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.967556357383728,
        "probabilities": {
          "human": 0.967556357383728,
          "aigc": 0.032443709671497345
        },
        "text": "9",
        "title": "第9页-段落33",
        "page_number": 9,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_331",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第10页-段落1",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_332",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9729577302932739,
        "probabilities": {
          "human": 0.9729577302932739,
          "aigc": 0.027042260393500328
        },
        "text": "Impact Statement",
        "title": "第10页-段落2",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_333",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994612336158752,
        "probabilities": {
          "human": 0.9994612336158752,
          "aigc": 0.0005387437995523214
        },
        "text": "view.net, 2024. URL https://openreview.net/\nforum?id=PEpbUobfJv.",
        "title": "第10页-段落3",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_334",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997250437736511,
        "probabilities": {
          "human": 0.00027488829800859094,
          "aigc": 0.9997250437736511
        },
        "text": "This paper thoroughly studies the layer-wise sensitivity of\ntransformers to KV cache quantization methods, which is\nthe inherent property of LLMs. Low-precision KV cache\nquantization may lead to significantly token-level atten-\ntion distribution shift in heads with non-sparse and non-\nconcentrated attention patterns. The attention head related\nproperty may also be applied to LLM weight and activa-\ntion quantization and other KV cache compression fields.\nThe proposed automatic KV cache precision pairs tuning\nalgorithm makes inference acceleration of LLMs with low-\nprecision KV cache possible, which can help reduce the\ndeployment cost and carbon footprint. Low-precision KV\ncache quantization with ignorable LLM accuracy loss is an\nimportant direction to reduce the KV cache memory usage\nand cost in online inference, KV cache offloading (Sheng\net al., 2023; Zhang et al., 2024a), storage (Jin et al., 2024),\ntransferring (Liu et al., 2024d), and more LLM inference\nrelated applications.",
        "title": "第10页-段落4",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_335",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9110654592514038,
        "probabilities": {
          "human": 0.9110654592514038,
          "aigc": 0.08893457800149918
        },
        "text": "Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun,\nH., Kaiser, L., Plappert, M., Tworek, J., Hilton, J.,\nNakano, R., Hesse, C., and Schulman, J. Training ver-\nifiers to solve math word problems.\nArXiv preprint,\nabs/2110.14168, 2021. URL https://arxiv.org/\nabs/2110.14168.",
        "title": "第10页-段落5",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_336",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.881043553352356,
        "probabilities": {
          "human": 0.881043553352356,
          "aigc": 0.11895643174648285
        },
        "text": "Contributors, L. Lmdeploy: A toolkit for compressing,\ndeploying, and serving llm. https://github.com/\nInternLM/lmdeploy, 2023.",
        "title": "第10页-段落6",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_337",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999755322933197,
        "probabilities": {
          "human": 0.00024465512251481414,
          "aigc": 0.999755322933197
        },
        "text": "Dao, T., Fu, D. Y., Ermon, S., Rudra, A., and Ré,\nC.\nFlashattention: Fast and memory-efficient exact\nattention with io-awareness. In Koyejo, S., Mohamed,\nS., Agarwal, A., Belgrave, D., Cho, K., and Oh, A.\n(eds.), Advances in Neural Information Processing\nSystems 35:\nAnnual Conference on Neural Infor-\nmation Processing Systems 2022,\nNeurIPS 2022,\nNew Orleans, LA, USA, November 28 - December 9,\n2022,\n2022.\nURL http://papers.nips.cc/\npaper_files/paper/2022/hash/\n67d57c32e20fd0a7a302cb81d36e40d5-\nAbstract-Conference.html.",
        "title": "第10页-段落7",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_338",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9942777752876282,
        "probabilities": {
          "human": 0.9942777752876282,
          "aigc": 0.00572227593511343
        },
        "text": "References",
        "title": "第10页-段落8",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_339",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9973224997520447,
        "probabilities": {
          "human": 0.0026774967554956675,
          "aigc": 0.9973224997520447
        },
        "text": "Adnan, M., Arunkumar, A., Jain, G., Nair, P., Solovey-\nchik, I., and Kamath, P. Keyformer: Kv cache reduction\nthrough key tokens selection for efficient generative in-\nference. Proceedings of Machine Learning and Systems,\n6:114–127, 2024.",
        "title": "第10页-段落9",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_340",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996565580368042,
        "probabilities": {
          "human": 0.9996565580368042,
          "aigc": 0.00034341553691774607
        },
        "text": "DeepSeek,\n2024.\nURL\nhttps://api-\ndocs.deepseek.com/guides/kv_cache.",
        "title": "第10页-段落10",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_341",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6435620784759521,
        "probabilities": {
          "human": 0.35643795132637024,
          "aigc": 0.6435620784759521
        },
        "text": "Dong, S., Cheng, W., Qin, J., and Wang, W. Qaq: Quality\nadaptive quantization for llm kv cache. ArXiv preprint,\nabs/2403.04643, 2024. URL https://arxiv.org/\nabs/2403.04643.",
        "title": "第10页-段落11",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_342",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992609620094299,
        "probabilities": {
          "human": 0.0007390361279249191,
          "aigc": 0.9992609620094299
        },
        "text": "Akiba, T., Sano, S., Yanase, T., Ohta, T., and Koyama, M.\nOptuna: A next-generation hyperparameter optimization\nframework. In Teredesai, A., Kumar, V., Li, Y., Rosales,\nR., Terzi, E., and Karypis, G. (eds.), Proceedings of the\n25th ACM SIGKDD International Conference on Knowl-\nedge Discovery & Data Mining, KDD 2019, Anchor-\nage, AK, USA, August 4-8, 2019, pp. 2623–2631. ACM,\n2019. doi: 10.1145/3292500.3330701. URL https:\n//doi.org/10.1145/3292500.3330701.",
        "title": "第10页-段落12",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_343",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7732645869255066,
        "probabilities": {
          "human": 0.7732645869255066,
          "aigc": 0.22673539817333221
        },
        "text": "Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle,\nA., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan,\nA., et al. The llama 3 herd of models. ArXiv preprint,\nabs/2407.21783, 2024. URL https://arxiv.org/\nabs/2407.21783.",
        "title": "第10页-段落13",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_344",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.569951057434082,
        "probabilities": {
          "human": 0.4300489127635956,
          "aigc": 0.569951057434082
        },
        "text": "Elhoushi, M., Shrivastava, A., Liskovich, D., Hosmer, B.,\nWasti, B., Lai, L., Mahmoud, A., Acun, B., Agarwal,\nS., Roman, A., et al. Layer skip: Enabling early exit\ninference and self-speculative decoding. ArXiv preprint,\nabs/2404.16710, 2024. URL https://arxiv.org/\nabs/2404.16710.",
        "title": "第10页-段落14",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_345",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990981817245483,
        "probabilities": {
          "human": 0.0009018677519634366,
          "aigc": 0.9990981817245483
        },
        "text": "Bai, Y., Lv, X., Zhang, J., Lyu, H., Tang, J., Huang,\nZ., Du, Z., Liu, X., Zeng, A., Hou, L., Dong, Y.,\nTang, J., and Li, J.\nLongBench: A bilingual, mul-\ntitask benchmark for long context understanding.\nIn\nProceedings of the 62nd Annual Meeting of the As-\nsociation for Computational Linguistics (Volume 1:\nLong Papers), pp. 3119–3137, Bangkok, Thailand, Au-\ngust 2024. Association for Computational Linguistics.\ndoi: 10.18653/v1/2024.acl-long.172.\nURL https:\n//aclanthology.org/2024.acl-long.172.",
        "title": "第10页-段落15",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_346",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9980037808418274,
        "probabilities": {
          "human": 0.001996194012463093,
          "aigc": 0.9980037808418274
        },
        "text": "Ester, M., Kriegel, H.-P., Sander, J., Xu, X., et al. A density-\nbased algorithm for discovering clusters in large spatial\ndatabases with noise. In kdd, volume 96, pp. 226–231,\n1996.",
        "title": "第10页-段落16",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_347",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996178150177002,
        "probabilities": {
          "human": 0.00038216530811041594,
          "aigc": 0.9996178150177002
        },
        "text": "Cai, T., Li, Y., Geng, Z., Peng, H., Lee, J. D., Chen, D.,\nand Dao, T. Medusa: Simple LLM inference accelera-\ntion framework with multiple decoding heads. In Forty-\nfirst International Conference on Machine Learning,\nICML 2024, Vienna, Austria, July 21-27, 2024. OpenRe-",
        "title": "第10页-段落17",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_348",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6602373123168945,
        "probabilities": {
          "human": 0.6602373123168945,
          "aigc": 0.33976274728775024
        },
        "text": "Frantar, E., Ashkboos, S., Hoefler, T., and Alistarh,\nD.\nGptq:\nAccurate post-training quantization for\ngenerative pre-trained transformers.\nArXiv preprint,\nabs/2210.17323, 2022. URL https://arxiv.org/\nabs/2210.17323.",
        "title": "第10页-段落18",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_349",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9957696199417114,
        "probabilities": {
          "human": 0.9957696199417114,
          "aigc": 0.004230361897498369
        },
        "text": "10",
        "title": "第10页-段落19",
        "page_number": 10,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_350",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第11页-段落1",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_351",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992427825927734,
        "probabilities": {
          "human": 0.0007572926697321236,
          "aigc": 0.9992427825927734
        },
        "text": "Mackey, L., Belgrave, D., Fan, A., Paquet, U., Tomczak,\nJ. M., and Zhang, C. (eds.), Advances in Neural Infor-\nmation Processing Systems 38: Annual Conference on\nNeural Information Processing Systems 2024, NeurIPS\n2024, Vancouver, BC, Canada, December 10 - 15,\n2024,\n2024.\nURL http://papers.nips.cc/\npaper_files/paper/2024/hash/\n028fcbcf85435d39a40c4d61b42c99a4-\nAbstract-Conference.html.",
        "title": "第11页-段落2",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_352",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.975702702999115,
        "probabilities": {
          "human": 0.024297330528497696,
          "aigc": 0.975702702999115
        },
        "text": "Gao, L., Tow, J., Abbasi, B., Biderman, S., Black, S., DiPofi,\nA., Foster, C., Golding, L., Hsu, J., Le Noac’h, A., Li,\nH., McDonell, K., Muennighoff, N., Ociepa, C., Phang,\nJ., Reynolds, L., Schoelkopf, H., Skowron, A., Sutawika,\nL., Tang, E., Thite, A., Wang, B., Wang, K., and Zou,\nA. A framework for few-shot language model evalua-\ntion, 2024. URL https://zenodo.org/records/\n12608602.",
        "title": "第11页-段落3",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_353",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992146492004395,
        "probabilities": {
          "human": 0.0007853137794882059,
          "aigc": 0.9992146492004395
        },
        "text": "Ge, S., Zhang, Y., Liu, L., Zhang, M., Han, J., and\nGao, J.\nModel tells you what to discard: Adaptive\nKV cache compression for llms.\nIn The Twelfth In-\nternational Conference on Learning Representations,\nICLR 2024, Vienna, Austria, May 7-11, 2024. OpenRe-\nview.net, 2024. URL https://openreview.net/\nforum?id=uNrFpDPMyo.",
        "title": "第11页-段落4",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_354",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993552565574646,
        "probabilities": {
          "human": 0.00064472685335204,
          "aigc": 0.9993552565574646
        },
        "text": "Huang, Y., Bai, Y., Zhu, Z., Zhang, J., Zhang, J., Su, T.,\nLiu, J., Lv, C., Zhang, Y., Lei, J., Fu, Y., Sun, M., and\nHe, J. C-eval: A multi-level multi-discipline chinese\nevaluation suite for foundation models.\nIn Oh, A.,\nNaumann, T., Globerson, A., Saenko, K., Hardt, M.,\nand Levine, S. (eds.), Advances in Neural Information\nProcessing Systems 36: Annual Conference on Neu-\nral Information Processing Systems 2023, NeurIPS\n2023, New Orleans, LA, USA, December 10 - 16,\n2023,\n2023.\nURL http://papers.nips.cc/\npaper_files/paper/2023/hash/\nc6ec1844bec96d6d32ae95ae694e23d8-\nAbstract-Datasets_and_Benchmarks.html.",
        "title": "第11页-段落5",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_355",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.998189389705658,
        "probabilities": {
          "human": 0.001810574671253562,
          "aigc": 0.998189389705658
        },
        "text": "Gloeckle, F., Idrissi, B. Y., Rozière, B., Lopez-Paz, D.,\nand Synnaeve, G.\nBetter & faster large language\nmodels via multi-token prediction.\nIn Forty-first In-\nternational Conference on Machine Learning, ICML\n2024, Vienna, Austria, July 21-27, 2024. OpenRe-\nview.net, 2024. URL https://openreview.net/\nforum?id=pEWAcejiU2.",
        "title": "第11页-段落6",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_356",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7256894111633301,
        "probabilities": {
          "human": 0.7256894111633301,
          "aigc": 0.2743105888366699
        },
        "text": "Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C.,\nChaplot, D. S., Casas, D. d. l., Bressand, F., Lengyel, G.,\nLample, G., Saulnier, L., et al. Mistral 7b. ArXiv preprint,\nabs/2310.06825, 2023. URL https://arxiv.org/\nabs/2310.06825.",
        "title": "第11页-段落7",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_357",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9344375729560852,
        "probabilities": {
          "human": 0.06556237488985062,
          "aigc": 0.9344375729560852
        },
        "text": "He, Y., Chen, F., Liu, J., Shao, W., Zhou, H., Zhang, K.,\nand Zhuang, B. Zipvl: Efficient large vision-language\nmodels with dynamic token sparsification and kv cache\ncompression. ArXiv preprint, abs/2410.08584, 2024a.\nURL https://arxiv.org/abs/2410.08584.",
        "title": "第11页-段落8",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_358",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9096505045890808,
        "probabilities": {
          "human": 0.0903494730591774,
          "aigc": 0.9096505045890808
        },
        "text": "Jin, C., Zhang, Z., Jiang, X., Liu, F., Liu, X., Liu, X.,\nand Jin, X.\nRagcache: Efficient knowledge caching\nfor retrieval-augmented generation.\nArXiv preprint,\nabs/2404.12457, 2024. URL https://arxiv.org/\nabs/2404.12457.",
        "title": "第11页-段落9",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_359",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999472439289093,
        "probabilities": {
          "human": 0.0005275465664453804,
          "aigc": 0.999472439289093
        },
        "text": "He, Y., Zhang, L., Wu, W., Liu, J., Zhou, H., and Zhuang, B.\nZipcache: Accurate and efficient KV cache quantization\nwith salient token identification.\nIn Globersons, A.,\nMackey, L., Belgrave, D., Fan, A., Paquet, U., Tomczak,\nJ. M., and Zhang, C. (eds.), Advances in Neural Infor-\nmation Processing Systems 38: Annual Conference on\nNeural Information Processing Systems 2024, NeurIPS\n2024, Vancouver, BC, Canada, December 10 - 15,\n2024, 2024b.\nURL http://papers.nips.cc/\npaper_files/paper/2024/hash/\n7e57131fdeb815764434b65162c88895-\nAbstract-Conference.html.",
        "title": "第11页-段落10",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_360",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993645548820496,
        "probabilities": {
          "human": 0.00063544005388394,
          "aigc": 0.9993645548820496
        },
        "text": "Joshi, M., Choi, E., Weld, D., and Zettlemoyer, L. Trivi-\naQA: A large scale distantly supervised challenge dataset\nfor reading comprehension. In Barzilay, R. and Kan,\nM.-Y. (eds.), Proceedings of the 55th Annual Meet-\ning of the Association for Computational Linguistics\n(Volume 1: Long Papers), pp. 1601–1611, Vancouver,\nCanada, 2017. Association for Computational Linguis-\ntics.\ndoi: 10.18653/v1/P17-1147.\nURL https://\naclanthology.org/P17-1147.",
        "title": "第11页-段落11",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_361",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9976351261138916,
        "probabilities": {
          "human": 0.0023648524656891823,
          "aigc": 0.9976351261138916
        },
        "text": "Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika,\nM., Song, D., and Steinhardt, J.\nMeasuring mas-\nsive multitask language understanding. In 9th Interna-\ntional Conference on Learning Representations, ICLR\n2021, Virtual Event, Austria, May 3-7, 2021. OpenRe-\nview.net, 2021. URL https://openreview.net/\nforum?id=d7KBjmI3GmQ.",
        "title": "第11页-段落12",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_362",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5412858724594116,
        "probabilities": {
          "human": 0.458714097738266,
          "aigc": 0.5412858724594116
        },
        "text": "Kang, H., Bharadwaj, S., Hensman, J., Krishna, T., Ruhle,\nV., and Rajmohan, S. Turboattention: Efficient attention\napproximation for high throughputs llms. arXiv preprint\narXiv:2412.08585, 2024a.",
        "title": "第11页-段落13",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_363",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8856048583984375,
        "probabilities": {
          "human": 0.11439508944749832,
          "aigc": 0.8856048583984375
        },
        "text": "Kang, H., Zhang, Q., Kundu, S., Jeong, G., Liu, Z., Kr-\nishna, T., and Zhao, T. Gear: An efficient kv cache\ncompression recipefor near-lossless generative inference\nof llm. ArXiv preprint, abs/2403.05527, 2024b. URL\nhttps://arxiv.org/abs/2403.05527.",
        "title": "第11页-段落14",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_364",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9960298538208008,
        "probabilities": {
          "human": 0.003970140125602484,
          "aigc": 0.9960298538208008
        },
        "text": "Hooper, C., Kim, S., Mohammadzadeh, H., Mahoney,\nM. W., Shao, Y. S., Keutzer, K., and Gholami, A.\nKvquant:\nTowards 10 million context length LLM\ninference with KV cache quantization. In Globersons, A.,",
        "title": "第11页-段落15",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_365",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9970390796661377,
        "probabilities": {
          "human": 0.9970390796661377,
          "aigc": 0.0029609487392008305
        },
        "text": "11",
        "title": "第11页-段落16",
        "page_number": 11,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_366",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第12页-段落1",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_367",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5116855502128601,
        "probabilities": {
          "human": 0.5116855502128601,
          "aigc": 0.4883144497871399
        },
        "text": "compression and acceleration. Proceedings of Machine\nLearning and Systems, 6:87–100, 2024a.",
        "title": "第12页-段落2",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_368",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997461438179016,
        "probabilities": {
          "human": 0.0002538415719754994,
          "aigc": 0.9997461438179016
        },
        "text": "Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu,\nC. H., Gonzalez, J., Zhang, H., and Stoica, I. Efficient\nmemory management for large language model serving\nwith pagedattention. In Proceedings of the 29th Sym-\nposium on Operating Systems Principles, pp. 611–626,\n2023.",
        "title": "第12页-段落3",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_369",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996949434280396,
        "probabilities": {
          "human": 0.000305044261040166,
          "aigc": 0.9996949434280396
        },
        "text": "Lin, S., Hilton, J., and Evans, O. TruthfulQA: Measur-\ning how models mimic human falsehoods.\nIn Mure-\nsan, S., Nakov, P., and Villavicencio, A. (eds.), Pro-\nceedings of the 60th Annual Meeting of the Association\nfor Computational Linguistics (Volume 1: Long Papers),\npp. 3214–3252, Dublin, Ireland, 2022. Association for\nComputational Linguistics. doi: 10.18653/v1/2022.acl-\nlong.229.\nURL https://aclanthology.org/\n2022.acl-long.229.",
        "title": "第12页-段落4",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_370",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994876384735107,
        "probabilities": {
          "human": 0.0005123848677612841,
          "aigc": 0.9994876384735107
        },
        "text": "Lai, G., Xie, Q., Liu, H., Yang, Y., and Hovy, E. RACE:\nLarge-scale ReAding comprehension dataset from ex-\naminations.\nIn Palmer, M., Hwa, R., and Riedel, S.\n(eds.), Proceedings of the 2017 Conference on Empirical\nMethods in Natural Language Processing, pp. 785–794,\nCopenhagen, Denmark, 2017. Association for Compu-\ntational Linguistics. doi: 10.18653/v1/D17-1082. URL\nhttps://aclanthology.org/D17-1082.",
        "title": "第12页-段落5",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_371",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9808768630027771,
        "probabilities": {
          "human": 0.9808768630027771,
          "aigc": 0.019123146310448647
        },
        "text": "Lin, Y., Tang, H., Yang, S., Zhang, Z., Xiao, G., Gan, C.,\nand Han, S. Qserve: W4a8kv4 quantization and sys-\ntem co-design for efficient llm serving. ArXiv preprint,\nabs/2405.04532, 2024b. URL https://arxiv.org/\nabs/2405.04532.",
        "title": "第12页-段落6",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_372",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994474053382874,
        "probabilities": {
          "human": 0.0005526248132809997,
          "aigc": 0.9994474053382874
        },
        "text": "Lee, J., Park, S., Hong, S., Kim, M., Chang, D., and Choi,\nJ. Improving conversational abilities of quantized large\nlanguage models via direct preference alignment. In Ku,\nL., Martins, A., and Srikumar, V. (eds.), Proceedings of\nthe 62nd Annual Meeting of the Association for Com-\nputational Linguistics (Volume 1: Long Papers), ACL\n2024, Bangkok, Thailand, August 11-16, 2024, pp. 11346–\n11364. Association for Computational Linguistics, 2024a.\ndoi: 10.18653/V1/2024.ACL-LONG.612. URL https:\n//doi.org/10.18653/v1/2024.acl-long.612.",
        "title": "第12页-段落7",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_373",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9650959372520447,
        "probabilities": {
          "human": 0.9650959372520447,
          "aigc": 0.03490407392382622
        },
        "text": "Liu, A., Feng, B., Xue, B., Wang, B., Wu, B., Lu, C., Zhao,\nC., Deng, C., Zhang, C., Ruan, C., et al. Deepseek-v3\ntechnical report. ArXiv preprint, abs/2412.19437, 2024a.\nURL https://arxiv.org/abs/2412.19437.",
        "title": "第12页-段落8",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_374",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995174407958984,
        "probabilities": {
          "human": 0.00048259046161547303,
          "aigc": 0.9995174407958984
        },
        "text": "Liu, A., Liu, J., Pan, Z., He, Y., Haffari, R., and Zhuang, B.\nMinicache: KV cache compression in depth dimension\nfor large language models. In Globersons, A., Mackey,\nL., Belgrave, D., Fan, A., Paquet, U., Tomczak, J. M.,\nand Zhang, C. (eds.), Advances in Neural Information\nProcessing Systems 38: Annual Conference on Neu-\nral Information Processing Systems 2024, NeurIPS\n2024, Vancouver, BC, Canada, December 10 - 15,\n2024, 2024b.\nURL http://papers.nips.cc/\npaper_files/paper/2024/hash/\nfd0705710bf01b88a60a3d479ea341d9-\nAbstract-Conference.html.",
        "title": "第12页-段落9",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_375",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992477893829346,
        "probabilities": {
          "human": 0.0007522054365836084,
          "aigc": 0.9992477893829346
        },
        "text": "Lee, W., Lee, J., Seo, J., and Sim, J. {InfiniGen}: Effi-\ncient generative inference of large language models with\ndynamic {KV} cache management. In 18th USENIX\nSymposium on Operating Systems Design and Implemen-\ntation (OSDI 24), pp. 155–172, 2024b.",
        "title": "第12页-段落10",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_376",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9986956715583801,
        "probabilities": {
          "human": 0.0013043340295553207,
          "aigc": 0.9986956715583801
        },
        "text": "Li, Y., Huang, Y., Yang, B., Venkitesh, B., Locatelli, A., Ye,\nH., Cai, T., Lewis, P., and Chen, D. Snapkv: LLM knows\nwhat you are looking for before generation. In Glober-\nsons, A., Mackey, L., Belgrave, D., Fan, A., Paquet,\nU., Tomczak, J. M., and Zhang, C. (eds.), Advances in\nNeural Information Processing Systems 38: Annual Con-\nference on Neural Information Processing Systems 2024,\nNeurIPS 2024, Vancouver, BC, Canada, December 10 -\n15, 2024, 2024a. URL http://papers.nips.cc/\npaper_files/paper/2024/hash/\n28ab418242603e0f7323e54185d19bde-\nAbstract-Conference.html.",
        "title": "第12页-段落11",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_377",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996028542518616,
        "probabilities": {
          "human": 0.00039716524770483375,
          "aigc": 0.9996028542518616
        },
        "text": "Liu, R., Bai, H., Lin, H., Li, Y., Gao, H., Xu, Z., Hou, L.,\nYao, J., and Yuan, C. Intactkv: Improving large language\nmodel quantization by keeping pivot tokens intact. In\nKu, L., Martins, A., and Srikumar, V. (eds.), Findings\nof the Association for Computational Linguistics, ACL\n2024, Bangkok, Thailand and virtual meeting, August 11-\n16, 2024, pp. 7716–7741. Association for Computational\nLinguistics, 2024c. doi: 10.18653/V1/2024.FINDINGS-\nACL.460. URL https://doi.org/10.18653/v1/\n2024.findings-acl.460.",
        "title": "第12页-段落12",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_378",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9985062479972839,
        "probabilities": {
          "human": 0.001493713352829218,
          "aigc": 0.9985062479972839
        },
        "text": "Li, Y., Wei, F., Zhang, C., and Zhang, H.\nEAGLE:\nspeculative sampling requires rethinking feature uncer-\ntainty. In Forty-first International Conference on Ma-\nchine Learning, ICML 2024, Vienna, Austria, July 21-\n27, 2024. OpenReview.net, 2024b.\nURL https://\nopenreview.net/forum?id=1NdN7eXyb4.",
        "title": "第12页-段落13",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_379",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990912675857544,
        "probabilities": {
          "human": 0.0009087485377676785,
          "aigc": 0.9990912675857544
        },
        "text": "Liu, Y., Li, H., Cheng, Y., Ray, S., Huang, Y., Zhang, Q.,\nDu, K., Yao, J., Lu, S., Ananthanarayanan, G., et al.\nCachegen: Kv cache compression and streaming for fast\nlarge language model serving. In Proceedings of the ACM\nSIGCOMM 2024 Conference, pp. 38–56, 2024d.",
        "title": "第12页-段落14",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_380",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9971911311149597,
        "probabilities": {
          "human": 0.002808833261951804,
          "aigc": 0.9971911311149597
        },
        "text": "Lin, J., Tang, J., Tang, H., Yang, S., Chen, W.-M., Wang,\nW.-C., Xiao, G., Dang, X., Gan, C., and Han, S. Awq:\nActivation-aware weight quantization for on-device llm",
        "title": "第12页-段落15",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_381",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9982549548149109,
        "probabilities": {
          "human": 0.0017450408777222037,
          "aigc": 0.9982549548149109
        },
        "text": "Liu, Z., Desai, A., Liao, F., Wang, W., Xie, V., Xu,\nZ., Kyrillidis, A., and Shrivastava, A.\nScissorhands:\nExploiting the persistence of importance hypothesis",
        "title": "第12页-段落16",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_382",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9964134097099304,
        "probabilities": {
          "human": 0.9964134097099304,
          "aigc": 0.0035866431426256895
        },
        "text": "12",
        "title": "第12页-段落17",
        "page_number": 12,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_383",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第13页-段落1",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_384",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8791452646255493,
        "probabilities": {
          "human": 0.12085475772619247,
          "aigc": 0.8791452646255493
        },
        "text": "and Scarlett, J. (eds.), International Conference on Ma-\nchine Learning, ICML 2023, 23-29 July 2023, Honolulu,\nHawaii, USA, volume 202 of Proceedings of Machine\nLearning Research, pp. 31094–31116. PMLR, 2023.\nURL https://proceedings.mlr.press/v202/\nsheng23a.html.",
        "title": "第13页-段落2",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_385",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994656443595886,
        "probabilities": {
          "human": 0.0005343392840586603,
          "aigc": 0.9994656443595886
        },
        "text": "for LLM KV cache compression at test time. In Oh,\nA., Naumann, T., Globerson, A., Saenko, K., Hardt,\nM., and Levine, S. (eds.), Advances in Neural Infor-\nmation Processing Systems 36: Annual Conference on\nNeural Information Processing Systems 2023, NeurIPS\n2023, New Orleans, LA, USA, December 10 - 16,\n2023,\n2023.\nURL http://papers.nips.cc/\npaper_files/paper/2023/hash/\na452a7c6c463e4ae8fbdc614c6e983e6-\nAbstract-Conference.html.",
        "title": "第13页-段落3",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_386",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9551421999931335,
        "probabilities": {
          "human": 0.9551421999931335,
          "aigc": 0.04485781490802765
        },
        "text": "Shoeybi, M., Patwary, M., Puri, R., LeGresley, P., Casper,\nJ., and Catanzaro, B.\nMegatron-lm: Training multi-\nbillion parameter language models using model paral-\nlelism. ArXiv preprint, abs/1909.08053, 2019. URL\nhttps://arxiv.org/abs/1909.08053.",
        "title": "第13页-段落4",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_387",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9986716508865356,
        "probabilities": {
          "human": 0.001328355516307056,
          "aigc": 0.9986716508865356
        },
        "text": "Liu, Z., Yuan, J., Jin, H., Zhong, S., Xu, Z., Braver-\nman, V., Chen, B., and Hu, X. KIVI: A tuning-free\nasymmetric 2bit quantization for KV cache. In Forty-\nfirst International Conference on Machine Learning,\nICML 2024, Vienna, Austria, July 21-27, 2024. OpenRe-\nview.net, 2024e. URL https://openreview.net/\nforum?id=L057s2Rq8O.",
        "title": "第13页-段落5",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_388",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988685846328735,
        "probabilities": {
          "human": 0.9988685846328735,
          "aigc": 0.0011313888244330883
        },
        "text": "SoftAge-AI,\n2024.\nURL\nhttps://\nhuggingface.co/datasets/SoftAge-AI/\nmulti-turn_dataset.",
        "title": "第13页-段落6",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_389",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9982795715332031,
        "probabilities": {
          "human": 0.0017204422038048506,
          "aigc": 0.9982795715332031
        },
        "text": "Stern, M., Shazeer, N., and Uszkoreit, J.\nBlockwise\nparallel decoding for deep autoregressive models. In\nBengio, S., Wallach, H. M., Larochelle, H., Grau-\nman, K., Cesa-Bianchi, N., and Garnett, R. (eds.),\nAdvances in Neural Information Processing Systems\n31: Annual Conference on Neural Information Pro-\ncessing Systems 2018, NeurIPS 2018, December 3-8,\n2018, Montréal, Canada, pp. 10107–10116, 2018.\nURL\nhttps://proceedings.neurips.cc/\npaper/2018/hash/\nc4127b9194fe8562c64dc0f5bf2c93bc-\nAbstract.html.",
        "title": "第13页-段落7",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_390",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.570024847984314,
        "probabilities": {
          "human": 0.570024847984314,
          "aigc": 0.42997515201568604
        },
        "text": "Liu, Z., Zhao, C., Fedorov, I., Soran, B., Choudhary, D., Kr-\nishnamoorthi, R., Chandra, V., Tian, Y., and Blankevoort,\nT. Spinquant–llm quantization with learned rotations.\nArXiv preprint, abs/2405.16406, 2024f. URL https:\n//arxiv.org/abs/2405.16406.",
        "title": "第13页-段落8",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_391",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997509121894836,
        "probabilities": {
          "human": 0.0002491163613740355,
          "aigc": 0.9997509121894836
        },
        "text": "Ma, X., Fang, G., and Wang, X.\nLlm-pruner: On the\nstructural pruning of large language models.\nIn Oh,\nA., Naumann, T., Globerson, A., Saenko, K., Hardt,\nM., and Levine, S. (eds.), Advances in Neural Infor-\nmation Processing Systems 36: Annual Conference on\nNeural Information Processing Systems 2023, NeurIPS\n2023, New Orleans, LA, USA, December 10 - 16,\n2023,\n2023.\nURL http://papers.nips.cc/\npaper_files/paper/2023/hash/\n44956951349095f74492a5471128a7e0-\nAbstract-Conference.html.",
        "title": "第13页-段落9",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_392",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5616840124130249,
        "probabilities": {
          "human": 0.4383159577846527,
          "aigc": 0.5616840124130249
        },
        "text": "Sun, H., Chang, L.-W., Bao, W., Zheng, S., Zheng, N., Liu,\nX., Dong, H., Chi, Y., and Chen, B. Shadowkv: Kv\ncache in shadows for high-throughput long-context llm\ninference. ArXiv preprint, abs/2410.21465, 2024a. URL\nhttps://arxiv.org/abs/2410.21465.",
        "title": "第13页-段落10",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_393",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9729995727539062,
        "probabilities": {
          "human": 0.027000438421964645,
          "aigc": 0.9729995727539062
        },
        "text": "Sun, H., Chen, Z., Yang, X., Tian, Y., and Chen, B. Tri-\nforce: Lossless acceleration of long sequence generation\nwith hierarchical speculative decoding. ArXiv preprint,\nabs/2404.11912, 2024b. URL https://arxiv.org/\nabs/2404.11912.",
        "title": "第13页-段落11",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_394",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995498061180115,
        "probabilities": {
          "human": 0.9995498061180115,
          "aigc": 0.0004501718212850392
        },
        "text": "OpenAI, 2024. URL https://openai.com/index/\napi-prompt-caching/.",
        "title": "第13页-段落12",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_395",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8815295696258545,
        "probabilities": {
          "human": 0.8815295696258545,
          "aigc": 0.11847042292356491
        },
        "text": "Qin, R., Li, Z., He, W., Zhang, M., Wu, Y., Zheng,\nW., and Xu, X. Mooncake: A kvcache-centric disag-\ngregated architecture for llm serving. ArXiv preprint,\nabs/2407.00079, 2024. URL https://arxiv.org/\nabs/2407.00079.",
        "title": "第13页-段落13",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_396",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996529817581177,
        "probabilities": {
          "human": 0.0003470524097792804,
          "aigc": 0.9996529817581177
        },
        "text": "Tang, H., Lin, Y., Lin, J., Han, Q., Ke, D., Hong, S.,\nYao, Y., and Wang, G. Razorattention: Efficient KV\ncache compression through retrieval heads. In The Thir-\nteenth International Conference on Learning Representa-\ntions, ICLR 2025, Singapore, April 24-28, 2025. OpenRe-\nview.net, 2025. URL https://openreview.net/\nforum?id=tkiZQlL04w.",
        "title": "第13页-段落14",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_397",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6380662322044373,
        "probabilities": {
          "human": 0.36193373799324036,
          "aigc": 0.6380662322044373
        },
        "text": "Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang,\nR. Y., Dirani, J., Michael, J., and Bowman, S. R.\nGpqa: A graduate-level google-proof q&a benchmark.\nArXiv preprint, abs/2311.12022, 2023. URL https:\n//arxiv.org/abs/2311.12022.",
        "title": "第13页-段落15",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_398",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9986003041267395,
        "probabilities": {
          "human": 0.0013997303321957588,
          "aigc": 0.9986003041267395
        },
        "text": "Tang, J., Zhao, Y., Zhu, K., Xiao, G., Kasikci, B., and Han, S.\nQUEST: query-aware sparsity for efficient long-context\nLLM inference. In Forty-first International Conference\non Machine Learning, ICML 2024, Vienna, Austria, July\n21-27, 2024. OpenReview.net, 2024. URL https://\nopenreview.net/forum?id=KzACYw0MTV.",
        "title": "第13页-段落16",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_399",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993182420730591,
        "probabilities": {
          "human": 0.0006817789981141686,
          "aigc": 0.9993182420730591
        },
        "text": "Sheng, Y., Zheng, L., Yuan, B., Li, Z., Ryabinin, M.,\nChen, B., Liang, P., Ré, C., Stoica, I., and Zhang,\nC. Flexgen: High-throughput generative inference of\nlarge language models with a single GPU. In Krause,\nA., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S.,",
        "title": "第13页-段落17",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_400",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9971296191215515,
        "probabilities": {
          "human": 0.9971296191215515,
          "aigc": 0.002870396710932255
        },
        "text": "13",
        "title": "第13页-段落18",
        "page_number": 13,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_401",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第14页-段落1",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_402",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9192237257957458,
        "probabilities": {
          "human": 0.08077628165483475,
          "aigc": 0.9192237257957458
        },
        "text": "inference with retrieval and streaming heads. In The Thir-\nteenth International Conference on Learning Representa-\ntions, ICLR 2025, Singapore, April 24-28, 2025. OpenRe-\nview.net, 2025. URL https://openreview.net/\nforum?id=cFu7ze7xUm.",
        "title": "第14页-段落2",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_403",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994223117828369,
        "probabilities": {
          "human": 0.0005776761681772768,
          "aigc": 0.9994223117828369
        },
        "text": "Wan, Z., Wu, Z., Liu, C., Huang, J., Zhu, Z., Jin,\nP., Wang, L., and Yuan, L.\nLOOK-M: look-once\noptimization in KV cache for efficient multimodal\nlong-context inference.\nIn Al-Onaizan, Y., Bansal,\nM., and Chen, Y. (eds.), Findings of the Associa-\ntion for Computational Linguistics:\nEMNLP 2024,\nMiami, Florida, USA, November 12-16, 2024, pp.\n4065–4078. Association for Computational Linguis-\ntics, 2024.\nURL https://aclanthology.org/\n2024.findings-emnlp.235.",
        "title": "第14页-段落3",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_404",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7352178692817688,
        "probabilities": {
          "human": 0.7352178692817688,
          "aigc": 0.2647820711135864
        },
        "text": "Yang, A., Yang, B., Zhang, B., Hui, B., Zheng, B., Yu,\nB., Li, C., Liu, D., Huang, F., Wei, H., et al. Qwen2. 5\ntechnical report. ArXiv preprint, abs/2412.15115, 2024a.\nURL https://arxiv.org/abs/2412.15115.",
        "title": "第14页-段落4",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_405",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9437452554702759,
        "probabilities": {
          "human": 0.05625474825501442,
          "aigc": 0.9437452554702759
        },
        "text": "Yang, J. Y., Kim, B., Bae, J., Kwon, B., Park, G., Yang, E.,\nKwon, S. J., and Lee, D. No token left behind: Reliable kv\ncache compression via importance-aware mixed precision\nquantization. ArXiv preprint, abs/2402.18096, 2024b.\nURL https://arxiv.org/abs/2402.18096.",
        "title": "第14页-段落5",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_406",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9392813444137573,
        "probabilities": {
          "human": 0.060718659311532974,
          "aigc": 0.9392813444137573
        },
        "text": "Wang, Z., Jin, B., Yu, Z., and Zhang, M. Model tells you\nwhere to merge: Adaptive kv cache merging for llms on\nlong-context tasks. ArXiv preprint, abs/2407.08454, 2024.\nURL https://arxiv.org/abs/2407.08454.",
        "title": "第14页-段落6",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_407",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9489068388938904,
        "probabilities": {
          "human": 0.9489068388938904,
          "aigc": 0.05109311640262604
        },
        "text": "Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter,\nB., Xia, F., Chi, E., Le, Q., and Zhou, D. Chain-of-\nthought prompting elicits reasoning in large language\nmodels, 2023.\nURL https://arxiv.org/abs/\n2201.11903.",
        "title": "第14页-段落7",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_408",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994183778762817,
        "probabilities": {
          "human": 0.0005817007040604949,
          "aigc": 0.9994183778762817
        },
        "text": "Yuan, J., Liu, H., Zhong, S., Chuang, Y., Li, S., Wang,\nG., Le, D., Jin, H., Chaudhary, V., Xu, Z., Liu, Z.,\nand Hu, X. B.\nKV cache compression, but what\nmust we give in return? A comprehensive benchmark\nof long context capable approaches.\nIn Al-Onaizan,\nY., Bansal, M., and Chen, Y. (eds.), Findings of the\nAssociation for Computational Linguistics:\nEMNLP\n2024, Miami, Florida, USA, November 12-16, 2024,\npp. 4623–4648. Association for Computational Linguis-\ntics, 2024.\nURL https://aclanthology.org/\n2024.findings-emnlp.266.",
        "title": "第14页-段落8",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_409",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9863783121109009,
        "probabilities": {
          "human": 0.013621686957776546,
          "aigc": 0.9863783121109009
        },
        "text": "Wolf, T., Debut, L., Sanh, V., Chaumond, J., Delangue,\nC., Moi, A., Cistac, P., Rault, T., Louf, R., Funtow-\nicz, M., Davison, J., Shleifer, S., von Platen, P., Ma,\nC., Jernite, Y., Plu, J., Xu, C., Le Scao, T., Gugger,\nS., Drame, M., Lhoest, Q., and Rush, A. Transform-\ners: State-of-the-art natural language processing.\nIn\nLiu, Q. and Schlangen, D. (eds.), Proceedings of the\n2020 Conference on Empirical Methods in Natural Lan-\nguage Processing: System Demonstrations, pp. 38–45,\nOnline, 2020. Association for Computational Linguistics.\ndoi: 10.18653/v1/2020.emnlp-demos.6. URL https:\n//aclanthology.org/2020.emnlp-demos.6.",
        "title": "第14页-段落9",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_410",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6751101613044739,
        "probabilities": {
          "human": 0.3248898386955261,
          "aigc": 0.6751101613044739
        },
        "text": "Zeng, D., Du, N., Wang, T., Xu, Y., Lei, T., Chen, Z.,\nand Cui, C. Learning to skip for language modeling.\nArXiv preprint, abs/2311.15436, 2023. URL https:\n//arxiv.org/abs/2311.15436.",
        "title": "第14页-段落10",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_411",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9758308529853821,
        "probabilities": {
          "human": 0.9758308529853821,
          "aigc": 0.02416911907494068
        },
        "text": "Zhang, H., Ji, X., Chen, Y., Fu, F., Miao, X., Nie, X., Chen,\nW., and Cui, B. Pqcache: Product quantization-based\nkvcache for long context llm inference. ArXiv preprint,\nabs/2407.12820, 2024a. URL https://arxiv.org/\nabs/2407.12820.",
        "title": "第14页-段落11",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_412",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9990183115005493,
        "probabilities": {
          "human": 0.000981661956757307,
          "aigc": 0.9990183115005493
        },
        "text": "Xiao, G., Lin, J., Seznec, M., Wu, H., Demouth, J., and Han,\nS. Smoothquant: Accurate and efficient post-training\nquantization for large language models.\nIn Krause,\nA., Brunskill, E., Cho, K., Engelhardt, B., Sabato, S.,\nand Scarlett, J. (eds.), International Conference on Ma-\nchine Learning, ICML 2023, 23-29 July 2023, Honolulu,\nHawaii, USA, volume 202 of Proceedings of Machine\nLearning Research, pp. 38087–38099. PMLR, 2023.\nURL https://proceedings.mlr.press/v202/\nxiao23c.html.",
        "title": "第14页-段落12",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_413",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9865971207618713,
        "probabilities": {
          "human": 0.013402903452515602,
          "aigc": 0.9865971207618713
        },
        "text": "Zhang, Q. and Li, H. Moea/d: A multiobjective evolutionary\nalgorithm based on decomposition. IEEE Transactions\non evolutionary computation, 11(6):712–731, 2007.",
        "title": "第14页-段落13",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_414",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9991851449012756,
        "probabilities": {
          "human": 0.0008148273336701095,
          "aigc": 0.9991851449012756
        },
        "text": "Zhang, Y., Du, Y., Luo, G., Zhong, Y., Zhang, Z., Liu, S.,\nand Ji, R. Cam: Cache merging for memory-efficient\nllms inference. In Forty-first International Conference\non Machine Learning, ICML 2024, Vienna, Austria, July\n21-27, 2024. OpenReview.net, 2024b.\nURL https:\n//openreview.net/forum?id=LCTmppB165.",
        "title": "第14页-段落14",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_415",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993315935134888,
        "probabilities": {
          "human": 0.0006684857071377337,
          "aigc": 0.9993315935134888
        },
        "text": "Xiao, G., Tian, Y., Chen, B., Han, S., and Lewis, M. Ef-\nficient streaming language models with attention sinks.\nIn The Twelfth International Conference on Learning\nRepresentations, ICLR 2024, Vienna, Austria, May 7-\n11, 2024. OpenReview.net, 2024.\nURL https://\nopenreview.net/forum?id=NG7sS51zVF.",
        "title": "第14页-段落15",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_416",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992087483406067,
        "probabilities": {
          "human": 0.0007913344306871295,
          "aigc": 0.9992087483406067
        },
        "text": "Zhang, Z., Sheng, Y., Zhou, T., Chen, T., Zheng, L.,\nCai, R., Song, Z., Tian, Y., Ré, C., Barrett, C. W.,\nWang, Z., and Chen, B. H2O: heavy-hitter oracle for\nefficient generative inference of large language models.\nIn Oh, A., Naumann, T., Globerson, A., Saenko, K.,\nHardt, M., and Levine, S. (eds.), Advances in Neural",
        "title": "第14页-段落16",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_417",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9799174666404724,
        "probabilities": {
          "human": 0.020082518458366394,
          "aigc": 0.9799174666404724
        },
        "text": "Xiao, G., Tang, J., Zuo, J., Guo, J., Yang, S., Tang, H., Fu,\nY., and Han, S. Duoattention: Efficient long-context LLM",
        "title": "第14页-段落17",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_418",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9982300400733948,
        "probabilities": {
          "human": 0.9982300400733948,
          "aigc": 0.0017700234893709421
        },
        "text": "14",
        "title": "第14页-段落18",
        "page_number": 14,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_419",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第15页-段落1",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_420",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9784931540489197,
        "probabilities": {
          "human": 0.02150687389075756,
          "aigc": 0.9784931540489197
        },
        "text": "Information Processing Systems 36: Annual Conference\non Neural Information Processing Systems 2023,\nNeurIPS 2023, New Orleans, LA, USA, December 10 - 16,\n2023,\n2023.\nURL http://papers.nips.cc/\npaper_files/paper/2023/hash/\n6ceefa7b15572587b78ecfcebb2827f8-\nAbstract-Conference.html.",
        "title": "第15页-段落2",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_421",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9846764206886292,
        "probabilities": {
          "human": 0.015323590487241745,
          "aigc": 0.9846764206886292
        },
        "text": "Zhang, Z., Liu, S., Chen, R., Kailkhura, B., Chen, B., and\nWang, A. Q-hitter: A better token oracle for efficient llm\ninference via sparse-quantized kv cache. Proceedings of\nMachine Learning and Systems, 6:381–394, 2024c.",
        "title": "第15页-段落3",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_422",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994663596153259,
        "probabilities": {
          "human": 0.0005336981848813593,
          "aigc": 0.9994663596153259
        },
        "text": "Zhao, Y., Xie, Z., Liang, C., Zhuang, C., and Gu, J. Looka-\nhead: An inference acceleration framework for large\nlanguage model with lossless generation accuracy. In\nBaeza-Yates, R. and Bonchi, F. (eds.), Proceedings of\nthe 30th ACM SIGKDD Conference on Knowledge Dis-\ncovery and Data Mining, KDD 2024, Barcelona, Spain,\nAugust 25-29, 2024, pp. 6344–6355. ACM, 2024. doi:\n10.1145/3637528.3671614. URL https://doi.org/\n10.1145/3637528.3671614.",
        "title": "第15页-段落4",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_423",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993440508842468,
        "probabilities": {
          "human": 0.0006559022585861385,
          "aigc": 0.9993440508842468
        },
        "text": "Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H.,\nCao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Barrett,\nC. W., and Sheng, Y. Sglang: Efficient execution of\nstructured language model programs. In Globersons, A.,\nMackey, L., Belgrave, D., Fan, A., Paquet, U., Tomczak,\nJ. M., and Zhang, C. (eds.), Advances in Neural Infor-\nmation Processing Systems 38: Annual Conference on\nNeural Information Processing Systems 2024, NeurIPS\n2024, Vancouver, BC, Canada, December 10 - 15,\n2024,\n2024.\nURL http://papers.nips.cc/\npaper_files/paper/2024/hash/\n724be4472168f31ba1c9ac630f15dec8-\nAbstract-Conference.html.",
        "title": "第15页-段落5",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_424",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.996822714805603,
        "probabilities": {
          "human": 0.996822714805603,
          "aigc": 0.0031772947404533625
        },
        "text": "15",
        "title": "第15页-段落6",
        "page_number": 15,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_425",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第16页-段落1",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_426",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7010597586631775,
        "probabilities": {
          "human": 0.7010597586631775,
          "aigc": 0.2989402115345001
        },
        "text": "A. Proof of Lemma 1",
        "title": "第16页-段落2",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_427",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9980378746986389,
        "probabilities": {
          "human": 0.001962105045095086,
          "aigc": 0.9980378746986389
        },
        "text": "Lemma 1 claims that only attention heads with sparse and concentrated patterns demonstrate consistent robustness to\nlow-precision KV cache quantization. Its proof is below.",
        "title": "第16页-段落3",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_428",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9961298704147339,
        "probabilities": {
          "human": 0.0038700965233147144,
          "aigc": 0.9961298704147339
        },
        "text": "Proof. Given the query token q ∈R1×D and key cache K ∈RD×S, the attention score without errors is ai =\nexp(qKi)\nPS\nj=1 exp(qKj). The key asymmetric uniform quantization error ∆K ∈RS×D ∼N(0, σ2) follows normal distribu-",
        "title": "第16页-段落4",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_429",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7278575301170349,
        "probabilities": {
          "human": 0.7278575301170349,
          "aigc": 0.2721424996852875
        },
        "text": "tion, where σ = max(K)−min(K)",
        "title": "第16页-段落5",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_430",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9864098429679871,
        "probabilities": {
          "human": 0.013590190559625626,
          "aigc": 0.9864098429679871
        },
        "text": "2B−1\n. Therefore, low precision quantization leads to exponential larger quantization errors.\nThen, the i-th attention score with key errors is",
        "title": "第16页-段落6",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_431",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5116732716560364,
        "probabilities": {
          "human": 0.5116732716560364,
          "aigc": 0.48832669854164124
        },
        "text": "ˆai =\nexp(q(Ki + ∆Ki))\nPS\nj=1 exp(q(Kj + ∆Kj))\n=\nexp(qKi)exp(q∆Ki))\nPS\nj=1 exp(qKj)exp(q∆Kj)\n=\nexp(qKi))\nPS\nj=1 exp(qKj)exp(q∆Kj)",
        "title": "第16页-段落7",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_432",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.997215986251831,
        "probabilities": {
          "human": 0.997215986251831,
          "aigc": 0.0027840265538543463
        },
        "text": "exp(q∆Ki)\n.\n(5)",
        "title": "第16页-段落8",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_433",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993366599082947,
        "probabilities": {
          "human": 0.0006633346783928573,
          "aigc": 0.9993366599082947
        },
        "text": "If the key quantization error vector ∆Kj with low quantization precision B is noticeable, the inner product of query and\nerror vector q∆Kj is also not ignorable. There are two cases where ˆai equals to ai for all tokens. In other words, the\nattention distribution before and after key quantization are identical.",
        "title": "第16页-段落9",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_434",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992855191230774,
        "probabilities": {
          "human": 0.9992855191230774,
          "aigc": 0.0007145273848436773
        },
        "text": "Case 1) exp(q∆Kj)",
        "title": "第16页-段落10",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_435",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9672118425369263,
        "probabilities": {
          "human": 0.03278811275959015,
          "aigc": 0.9672118425369263
        },
        "text": "exp(q∆Ki) = 1, where each key token quantization errors have the same inner product result with the query token\nq∆Ki = q∆Kj which normally does not happen.",
        "title": "第16页-段落11",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_436",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.54985111951828,
        "probabilities": {
          "human": 0.45014891028404236,
          "aigc": 0.54985111951828
        },
        "text": "Case 2) There is a dominating key token i. If j ̸= i, exp(qKi) ≫exp(qKj) and exp(qKj)",
        "title": "第16页-段落12",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_437",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975529313087463,
        "probabilities": {
          "human": 0.9975529313087463,
          "aigc": 0.002447106409817934
        },
        "text": "exp(qKi) ≈0, then",
        "title": "第16页-段落13",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_438",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8912534713745117,
        "probabilities": {
          "human": 0.8912534713745117,
          "aigc": 0.10874645411968231
        },
        "text": "exp(qKi)\n≈exp(q∆Ki))",
        "title": "第16页-段落14",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_439",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8877034187316895,
        "probabilities": {
          "human": 0.8877034187316895,
          "aigc": 0.11229658871889114
        },
        "text": "ˆai =\nexp(q∆Ki))\nPS\nj=1 exp(q∆Kj)exp(qKj)",
        "title": "第16页-段落15",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_440",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.939123272895813,
        "probabilities": {
          "human": 0.939123272895813,
          "aigc": 0.060876719653606415
        },
        "text": "exp(q∆Ki)) = 1.\n(6)",
        "title": "第16页-段落16",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_441",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998676776885986,
        "probabilities": {
          "human": 0.0001322811731370166,
          "aigc": 0.9998676776885986
        },
        "text": "Other dominated key token thus has the attention score ˆaj = 0. The exactly identical attention distribution with a dominating\nkey token may be a special case, but it indicates that attention heads with a small amount of dominated key tokens, which\nhave highly attention scores and result in sparse and concentrated attention patterns, are consistently robust to low-precision\nKV cache quantization.",
        "title": "第16页-段落17",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_442",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9837275743484497,
        "probabilities": {
          "human": 0.016272468492388725,
          "aigc": 0.9837275743484497
        },
        "text": "B. Effects of KV Cache Quantization Mode and Precision",
        "title": "第16页-段落18",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_443",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997811913490295,
        "probabilities": {
          "human": 0.0002188094222219661,
          "aigc": 0.9997811913490295
        },
        "text": "In this section, we analyze the effects of KV cache quantization mode and precision. We collect the full precision query\ntensor in the decoding phase and KV cache in both prefilling and decoding stages of the Llama-3.1-8B-Instruct model when\nprocessing the first 20 mathematical GSM8K zero-shot prompts without KV cache quantization. After that, we quantize KV\ncache along the channel or token dimension with uniform precision to compute errors of KV cache and attention score and\noutput vectors of each self-attention layer as defined in Section 3.2, caused by KV cache quantization without any error\naccumulation. Finally, we average the simulated errors over different prompts and all layers in Table 9 to study the inherent\nsensitivity of KV cache to quantization mode and precision.",
        "title": "第16页-段落19",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_444",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993877410888672,
        "probabilities": {
          "human": 0.000612250529229641,
          "aigc": 0.9993877410888672
        },
        "text": "The non-accumulated relative attention output errors eo of INT8 KV cache quantization with the per-token-asym or per-\nchannel-asym are lower than 3%. Minor single-token errors may cause slight shifts in intermediate attention patterns and\nfinal output distributions, yet these shifts are typically insufficient to alter the generated output tokens. However, when\nimplementing extremely low-precision 2-bit KV2 cache quantization, the relative key quantization error ea increases to\n40.1% or 77.5%, which may lead to substantial attention distribution shift for non-sparse retrieval heads as demonstrated in\nFigure 4. eo increases dramatically to 81.4% with the per-channel-asym mode even 96.2% with the per-token-asym mode.\nThe noticeable errors may thus lead to noticeable token flipping and generation errors as in Table 1.",
        "title": "第16页-段落20",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_445",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8619976043701172,
        "probabilities": {
          "human": 0.1380023956298828,
          "aigc": 0.8619976043701172
        },
        "text": "The relative key error ek of the INT8 per-token-asym key quantization is 0.012280, which is 2.5× larger than the per-channel-\nasym counterpart 0.004869. Dynamically asymmetric quantization along the channel dimension leads to significantly\nsmaller error of both key cache and attention score compared with token dimension quantization, indicating that key cache\nis strongly sensitive to quantization dimensions. The phenomenon can be explained with the strong channel-wise outliers\nof key cache (Liu et al., 2024e; Hooper et al., 2024). While value cache can not benefit from switching the quantization\ndimension, as the relative value errors of the channel or token dimensions over different precision are quite close.",
        "title": "第16页-段落21",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_446",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9945027828216553,
        "probabilities": {
          "human": 0.9945027828216553,
          "aigc": 0.0054972218349576
        },
        "text": "16",
        "title": "第16页-段落22",
        "page_number": 16,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_447",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第17页-段落1",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_448",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993162155151367,
        "probabilities": {
          "human": 0.0006837512482888997,
          "aigc": 0.9993162155151367
        },
        "text": "Table 9: Key and value cache quantization relative error analysis of different precision and quantization methods. We collect\nBF16 KV cache of 20 prompts from the GSM8K zero-shot dataset with Llama-3.1-8B-Instruct and then perform offline\nquantization to compute the mean error between BF16 and dequantized KV cache.",
        "title": "第17页-段落2",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_449",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.607226550579071,
        "probabilities": {
          "human": 0.607226550579071,
          "aigc": 0.39277344942092896
        },
        "text": "KV cache precision\nKV quant mode\nRelative ek\nRelative ev\nea\nRelative eo",
        "title": "第17页-段落3",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_450",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996362924575806,
        "probabilities": {
          "human": 0.9996362924575806,
          "aigc": 0.000363746628863737
        },
        "text": "KV8\nper-channel-asym\n0.004869\n0.007754\n0.000013\n0.027686\nper-token-asym\n0.012280\n0.007865\n0.000018\n0.014589",
        "title": "第17页-段落4",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_451",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996919631958008,
        "probabilities": {
          "human": 0.9996919631958008,
          "aigc": 0.0003080498136114329
        },
        "text": "KV4\nper-channel-asym\n0.080991\n0.125457\n0.000172\n0.158429\nper-token-asym\n0.196476\n0.126894\n0.000251\n0.206909",
        "title": "第17页-段落5",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_452",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995255470275879,
        "probabilities": {
          "human": 0.9995255470275879,
          "aigc": 0.00047450046986341476
        },
        "text": "KV2\nper-channel-asym\n0.401151\n0.604678\n0.000868\n0.814023\nper-token-asym\n0.774668\n0.607898\n0.001166\n0.961792",
        "title": "第17页-段落6",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_453",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996504783630371,
        "probabilities": {
          "human": 0.0003495197161100805,
          "aigc": 0.9996504783630371
        },
        "text": "As shown in Figure 7, there are clear layer-wise diversities of KV quantization errors ek and eo with different quantization\nmodes including per-token-asym and per-channel-asym and different precision like INT8, INT4, and INT2. In addition,\nchanging the quantization dimension or mode can result in the significant distribution shift of layer-wise key quantization\nerror. For example, the most sensitive layer with the per-token-asym quantization mode is layer-29, while it changes to\nlayer-11 and layer-13 with the per-token-asym mode. Statically retaining the first or last several layers with more sparse\nbudgets (Tang et al., 2024) may not general well in KV cache quantization. Therefore, we need an automatic KV cache\nquantization tuning framework to adaptively adopt to these layer-wise differences and configuration modifications.",
        "title": "第17页-段落7",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_454",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5912659168243408,
        "probabilities": {
          "human": 0.40873411297798157,
          "aigc": 0.5912659168243408
        },
        "text": "C. Experimental Settings",
        "title": "第17页-段落8",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_455",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9986735582351685,
        "probabilities": {
          "human": 0.0013264479348435998,
          "aigc": 0.9986735582351685
        },
        "text": "KVTuner is an automatic KV cache quantization precision tuning framework and can be applied to any quantization mode.\nWe choose two representative and efficient KV cache quantization algorithms KIVI (Liu et al., 2024e) and per-token-asym\nwith uniform KV8, KV4, or KV2 precision pairs in all layers as baselines. Specifically, for the KIVI quantization method, we\nset the residual length to 32 and the group size to 32. KVTuner is currently implemented based on huggingface transformers,\nbut it can be applied to inference frameworks such as vLLM (Kwon et al., 2023), Megatron (Shoeybi et al., 2019), LMDeploy\n(Contributors, 2023), and SGLang (Zheng et al., 2024). To ensure compatibility, we integrate KV cache quantization\nmethods including KIVI, per-token-asym, and KVTuner within the lm-evaluation-harness (Gao et al., 2024), allowing for\nseamless adaptation and reproducibility of KVTuner.",
        "title": "第17页-段落9",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_456",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9727358222007751,
        "probabilities": {
          "human": 0.027264218777418137,
          "aigc": 0.9727358222007751
        },
        "text": "We select three popular and recently released LLMs series Llama3.1 (Dubey et al., 2024), Mistral-v0.3 (Jiang et al.,\n2023), and Qwen2.5 (Yang et al., 2024a). Among them, Llama-3.1-8B-Instruct, Mistral-7B-Instruct-v0.3, and Qwen2.5-\n7B-Instruct represent the most studied model size. To cover more LLMs application scenarios with different scales,\nQwen2.5-3B-Instuct and its quantized version Qwen2.5-3B-Instruct-AWQ are selected for personal devices with limited\nGPU memory, while Qwen2.5-{14B, 32B}-Instuct with larger model scale and better performance are also tested. We also\ntest Qwen2.5-Math-7B-Instruct for mathematical reasoning tasks.",
        "title": "第17页-段落10",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_457",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9842991828918457,
        "probabilities": {
          "human": 0.015700843185186386,
          "aigc": 0.9842991828918457
        },
        "text": "We cover 5 general AIGC and 2 mathematical reasoning tasks available in lm-evaluation-harness . 1) General tasks:\nCEVAL(Huang et al., 2023), MMLU (Hendrycks et al., 2021), TriviaQA (Joshi et al., 2017), RACE (Lai et al., 2017), and\nTruthfulQA (Lin et al., 2022). 2) Math, science, and logic tasks: GSM8K {0-shot, 4-shot, 8-shot, 16-shot} (Cobbe et al.,\n2021), GSM8K multi-round with lm-evaluation-harness (Gao et al., 2024), GPQA (Rein et al., 2023).",
        "title": "第17页-段落11",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_458",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.998695433139801,
        "probabilities": {
          "human": 0.0013046421809121966,
          "aigc": 0.998695433139801
        },
        "text": "For the final layer-wise KV cache quantization precision pair searching with multi-objective optimization, we use the\nopen-sourced and widely used Optuna framework (Akiba et al., 2019) and MOEA/D (Zhang & Li, 2007) algorithm. In\nwhich case, we treat the LLM inference accuracy under different layer-wise KV precision pairs and input prompts as\nblock-box. The intra-layer and inter-layer search space pruning only takes several minutes but significantly improves\nsampling efficiency of the downstream Optuna.",
        "title": "第17页-段落12",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_459",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998624324798584,
        "probabilities": {
          "human": 0.0001374929997837171,
          "aigc": 0.9998624324798584
        },
        "text": "We first preprocess the available quantization precision options for each layer group and store them in an array. The indices\nof this array are then treated as integer parameters, which are optimized by Optuna through multi-objective optimization.\nThe first objective is to maximize the accuracy on the first 200 samples of the GSM8K dataset, while the second objective\nis to minimize the equivalent quantization precision or memory usage of KV cache. For each combination of model and\nquantization mode, we set a soft constraint on the equivalent precision at 4-bit and 6-bit for optuna, conducting 200 search\niterations for each setting. The total time cost of offline KV cache precision pair tuning with Optuna mainly depends on the",
        "title": "第17页-段落13",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_460",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9935972690582275,
        "probabilities": {
          "human": 0.9935972690582275,
          "aigc": 0.006402762606739998
        },
        "text": "17",
        "title": "第17页-段落14",
        "page_number": 17,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_461",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第18页-段落1",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_462",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974150657653809,
        "probabilities": {
          "human": 0.9974150657653809,
          "aigc": 0.002584894187748432
        },
        "text": "0.26",
        "title": "第18页-段落2",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_463",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989280104637146,
        "probabilities": {
          "human": 0.9989280104637146,
          "aigc": 0.001071993145160377
        },
        "text": "0.85",
        "title": "第18页-段落3",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_464",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987271428108215,
        "probabilities": {
          "human": 0.9987271428108215,
          "aigc": 0.0012728179572150111
        },
        "text": "0.016",
        "title": "第18页-段落4",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_465",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988040924072266,
        "probabilities": {
          "human": 0.9988040924072266,
          "aigc": 0.0011958788381889462
        },
        "text": "0.24",
        "title": "第18页-段落5",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_466",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988351464271545,
        "probabilities": {
          "human": 0.9988351464271545,
          "aigc": 0.001164900604635477
        },
        "text": "0.80",
        "title": "第18页-段落6",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_467",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985718727111816,
        "probabilities": {
          "human": 0.9985718727111816,
          "aigc": 0.001428139046765864
        },
        "text": "0.22",
        "title": "第18页-段落7",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_468",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993630051612854,
        "probabilities": {
          "human": 0.9993630051612854,
          "aigc": 0.0006369950715452433
        },
        "text": "0.014",
        "title": "第18页-段落8",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_469",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落9",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_470",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落10",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_471",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落11",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_472",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第18页-段落12",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_473",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981498718261719,
        "probabilities": {
          "human": 0.9981498718261719,
          "aigc": 0.0018501300364732742
        },
        "text": "0.75",
        "title": "第18页-段落13",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_474",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993888139724731,
        "probabilities": {
          "human": 0.9993888139724731,
          "aigc": 0.0006111774710007012
        },
        "text": "0.012",
        "title": "第18页-段落14",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_475",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第18页-段落15",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_476",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980891346931458,
        "probabilities": {
          "human": 0.9980891346931458,
          "aigc": 0.0019108442356809974
        },
        "text": "0.70",
        "title": "第18页-段落16",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_477",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第18页-段落17",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_478",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991521835327148,
        "probabilities": {
          "human": 0.9991521835327148,
          "aigc": 0.0008478129166178405
        },
        "text": "0.010",
        "title": "第18页-段落18",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_479",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第18页-段落19",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_480",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第18页-段落20",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_481",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991113543510437,
        "probabilities": {
          "human": 0.9991113543510437,
          "aigc": 0.0008886076393537223
        },
        "text": "0.008",
        "title": "第18页-段落21",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_482",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第18页-段落22",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_483",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第18页-段落23",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_484",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落24",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_485",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落25",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_486",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落26",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_487",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.997934103012085,
        "probabilities": {
          "human": 0.997934103012085,
          "aigc": 0.002065925393253565
        },
        "text": "(a) K8 per-token-asym",
        "title": "第18页-段落27",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_488",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9972715973854065,
        "probabilities": {
          "human": 0.9972715973854065,
          "aigc": 0.002728401916101575
        },
        "text": "(b) K4 per-token-asym",
        "title": "第18页-段落28",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_489",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977352619171143,
        "probabilities": {
          "human": 0.9977352619171143,
          "aigc": 0.0022646873258054256
        },
        "text": "(c) K2 per-token-asym",
        "title": "第18页-段落29",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_490",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995232820510864,
        "probabilities": {
          "human": 0.9995232820510864,
          "aigc": 0.0004767571808770299
        },
        "text": "0.0060",
        "title": "第18页-段落30",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_491",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第18页-段落31",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_492",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996216297149658,
        "probabilities": {
          "human": 0.9996216297149658,
          "aigc": 0.0003783414722420275
        },
        "text": "0.0055",
        "title": "第18页-段落32",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_493",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977344274520874,
        "probabilities": {
          "human": 0.9977344274520874,
          "aigc": 0.002265507122501731
        },
        "text": "0.09",
        "title": "第18页-段落33",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_494",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996929168701172,
        "probabilities": {
          "human": 0.9996929168701172,
          "aigc": 0.0003071600804105401
        },
        "text": "0.0050",
        "title": "第18页-段落34",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_495",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第18页-段落35",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_496",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第18页-段落36",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_497",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落37",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_498",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落38",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_499",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8571334481239319,
        "probabilities": {
          "human": 0.1428665816783905,
          "aigc": 0.8571334481239319
        },
        "text": "Key relative error",
        "title": "第18页-段落39",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_500",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996751546859741,
        "probabilities": {
          "human": 0.9996751546859741,
          "aigc": 0.0003248961002100259
        },
        "text": "0.0045",
        "title": "第18页-段落40",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_501",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第18页-段落41",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_502",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959213733673096,
        "probabilities": {
          "human": 0.9959213733673096,
          "aigc": 0.004078585188835859
        },
        "text": "0.07",
        "title": "第18页-段落42",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_503",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997163414955139,
        "probabilities": {
          "human": 0.9997163414955139,
          "aigc": 0.00028363688034005463
        },
        "text": "0.0040",
        "title": "第18页-段落43",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_504",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第18页-段落44",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_505",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995730519294739,
        "probabilities": {
          "human": 0.9995730519294739,
          "aigc": 0.00042693447903729975
        },
        "text": "0.0035",
        "title": "第18页-段落45",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_506",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第18页-段落46",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_507",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995471835136414,
        "probabilities": {
          "human": 0.9995471835136414,
          "aigc": 0.00045278671314008534
        },
        "text": "0.0030",
        "title": "第18页-段落47",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_508",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第18页-段落48",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_509",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第18页-段落49",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_510",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995228052139282,
        "probabilities": {
          "human": 0.9995228052139282,
          "aigc": 0.0004772258980665356
        },
        "text": "0.0025",
        "title": "第18页-段落50",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_511",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落51",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_512",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落52",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_513",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落53",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_514",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987809062004089,
        "probabilities": {
          "human": 0.9987809062004089,
          "aigc": 0.0012190626002848148
        },
        "text": "(d) K8 per-channel-asym",
        "title": "第18页-段落54",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_515",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990600943565369,
        "probabilities": {
          "human": 0.9990600943565369,
          "aigc": 0.0009399662958458066
        },
        "text": "(e) K4 per-channel-asym",
        "title": "第18页-段落55",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_516",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985036849975586,
        "probabilities": {
          "human": 0.9985036849975586,
          "aigc": 0.0014963527210056782
        },
        "text": "(f) K2 per-channel-asym",
        "title": "第18页-段落56",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_517",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第18页-段落57",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_518",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9982811212539673,
        "probabilities": {
          "human": 0.9982811212539673,
          "aigc": 0.0017189476639032364
        },
        "text": "0.68",
        "title": "第18页-段落58",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_519",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994008541107178,
        "probabilities": {
          "human": 0.9994008541107178,
          "aigc": 0.0005991946090944111
        },
        "text": "0.011",
        "title": "第18页-段落59",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_520",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979159235954285,
        "probabilities": {
          "human": 0.9979159235954285,
          "aigc": 0.0020840386860072613
        },
        "text": "0.17",
        "title": "第18页-段落60",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_521",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9969866871833801,
        "probabilities": {
          "human": 0.9969866871833801,
          "aigc": 0.003013341687619686
        },
        "text": "0.66",
        "title": "第18页-段落61",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_522",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第18页-段落62",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_523",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984344840049744,
        "probabilities": {
          "human": 0.9984344840049744,
          "aigc": 0.0015655586030334234
        },
        "text": "0.64",
        "title": "第18页-段落63",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_524",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落64",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_525",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落65",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_526",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落66",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_527",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991521835327148,
        "probabilities": {
          "human": 0.9991521835327148,
          "aigc": 0.0008478129166178405
        },
        "text": "0.010",
        "title": "第18页-段落67",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_528",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第18页-段落68",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_529",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983893632888794,
        "probabilities": {
          "human": 0.9983893632888794,
          "aigc": 0.0016106871189549565
        },
        "text": "0.62",
        "title": "第18页-段落69",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_530",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992979764938354,
        "probabilities": {
          "human": 0.9992979764938354,
          "aigc": 0.0007019626209512353
        },
        "text": "0.009",
        "title": "第18页-段落70",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_531",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第18页-段落71",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_532",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第18页-段落72",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_533",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989718198776245,
        "probabilities": {
          "human": 0.9989718198776245,
          "aigc": 0.001028164871968329
        },
        "text": "0.58",
        "title": "第18页-段落73",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_534",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988124370574951,
        "probabilities": {
          "human": 0.9988124370574951,
          "aigc": 0.0011876254575327039
        },
        "text": "0.13",
        "title": "第18页-段落74",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_535",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991113543510437,
        "probabilities": {
          "human": 0.9991113543510437,
          "aigc": 0.0008886076393537223
        },
        "text": "0.008",
        "title": "第18页-段落75",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_536",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.998254120349884,
        "probabilities": {
          "human": 0.998254120349884,
          "aigc": 0.001745817600749433
        },
        "text": "0.56",
        "title": "第18页-段落76",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_537",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第18页-段落77",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_538",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985452890396118,
        "probabilities": {
          "human": 0.9985452890396118,
          "aigc": 0.0014547775499522686
        },
        "text": "0.007",
        "title": "第18页-段落78",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_539",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991564750671387,
        "probabilities": {
          "human": 0.9991564750671387,
          "aigc": 0.00084357347805053
        },
        "text": "0.54",
        "title": "第18页-段落79",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_540",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985042810440063,
        "probabilities": {
          "human": 0.9985042810440063,
          "aigc": 0.0014957457315176725
        },
        "text": "0.11",
        "title": "第18页-段落80",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_541",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落81",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_542",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落82",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_543",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落83",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_544",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9962771534919739,
        "probabilities": {
          "human": 0.9962771534919739,
          "aigc": 0.003722771303728223
        },
        "text": "(g) V8 per-token-asym",
        "title": "第18页-段落84",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_545",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9982389211654663,
        "probabilities": {
          "human": 0.9982389211654663,
          "aigc": 0.0017610873328521848
        },
        "text": "(h) V4 per-token-asym",
        "title": "第18页-段落85",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_546",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975692629814148,
        "probabilities": {
          "human": 0.9975692629814148,
          "aigc": 0.0024307440035045147
        },
        "text": "(i) V2 per-token-asym",
        "title": "第18页-段落86",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_547",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994008541107178,
        "probabilities": {
          "human": 0.9994008541107178,
          "aigc": 0.0005991946090944111
        },
        "text": "0.011",
        "title": "第18页-段落87",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_548",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979159235954285,
        "probabilities": {
          "human": 0.9979159235954285,
          "aigc": 0.0020840386860072613
        },
        "text": "0.17",
        "title": "第18页-段落88",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_549",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第18页-段落89",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_550",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第18页-段落90",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_551",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991521835327148,
        "probabilities": {
          "human": 0.9991521835327148,
          "aigc": 0.0008478129166178405
        },
        "text": "0.010",
        "title": "第18页-段落91",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_552",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第18页-段落92",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_553",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第18页-段落93",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_554",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落94",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_555",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落95",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_556",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5865786075592041,
        "probabilities": {
          "human": 0.5865786075592041,
          "aigc": 0.4134214222431183
        },
        "text": "Value relative error",
        "title": "第18页-段落96",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_557",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992979764938354,
        "probabilities": {
          "human": 0.9992979764938354,
          "aigc": 0.0007019626209512353
        },
        "text": "0.009",
        "title": "第18页-段落97",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_558",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第18页-段落98",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_559",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988124370574951,
        "probabilities": {
          "human": 0.9988124370574951,
          "aigc": 0.0011876254575327039
        },
        "text": "0.13",
        "title": "第18页-段落99",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_560",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第18页-段落100",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_561",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991113543510437,
        "probabilities": {
          "human": 0.9991113543510437,
          "aigc": 0.0008886076393537223
        },
        "text": "0.008",
        "title": "第18页-段落101",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_562",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第18页-段落102",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_563",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985452890396118,
        "probabilities": {
          "human": 0.9985452890396118,
          "aigc": 0.0014547775499522686
        },
        "text": "0.007",
        "title": "第18页-段落103",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_564",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985042810440063,
        "probabilities": {
          "human": 0.9985042810440063,
          "aigc": 0.0014957457315176725
        },
        "text": "0.11",
        "title": "第18页-段落104",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_565",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第18页-段落105",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_566",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第18页-段落106",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_567",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985707998275757,
        "probabilities": {
          "human": 0.9985707998275757,
          "aigc": 0.001429222640581429
        },
        "text": "0.006",
        "title": "第18页-段落107",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_568",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第18页-段落108",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_569",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977344274520874,
        "probabilities": {
          "human": 0.9977344274520874,
          "aigc": 0.002265507122501731
        },
        "text": "0.09",
        "title": "第18页-段落109",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_570",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落110",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_571",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落111",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_572",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第18页-段落112",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_573",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.998683512210846,
        "probabilities": {
          "human": 0.998683512210846,
          "aigc": 0.0013164299307391047
        },
        "text": "(j) V8 per-channel-asym",
        "title": "第18页-段落113",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_574",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990330934524536,
        "probabilities": {
          "human": 0.9990330934524536,
          "aigc": 0.0009668660932220519
        },
        "text": "(k) V4 per-channel-asym",
        "title": "第18页-段落114",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_575",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987524747848511,
        "probabilities": {
          "human": 0.9987524747848511,
          "aigc": 0.0012474890099838376
        },
        "text": "(l) V2 per-channel-asym",
        "title": "第18页-段落115",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_576",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9975034594535828,
        "probabilities": {
          "human": 0.002496560337021947,
          "aigc": 0.9975034594535828
        },
        "text": "Figure 7: Layer-wise relative key errors ek and value errors ev of Llama-3.1-8B-Instruct with the per-token-asym and\nper-channel-asym quantization modes, KV cache precision as 8, 4, and 2-bit, and the same settings in Table 9.",
        "title": "第18页-段落116",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_577",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.996033251285553,
        "probabilities": {
          "human": 0.996033251285553,
          "aigc": 0.003966748248785734
        },
        "text": "18",
        "title": "第18页-段落117",
        "page_number": 18,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_578",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第19页-段落1",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_579",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7879425883293152,
        "probabilities": {
          "human": 0.21205741167068481,
          "aigc": 0.7879425883293152
        },
        "text": "hardware and operator implementation efficiency.",
        "title": "第19页-段落2",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_580",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9700736403465271,
        "probabilities": {
          "human": 0.02992641180753708,
          "aigc": 0.9700736403465271
        },
        "text": "D. Search Space Pruning and Multi-objective Optimization results",
        "title": "第19页-段落3",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_581",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8195288777351379,
        "probabilities": {
          "human": 0.18047115206718445,
          "aigc": 0.8195288777351379
        },
        "text": "D.1. Intra-Layer and Inter-Layer Search Space Pruning Results",
        "title": "第19页-段落4",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_582",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9870592355728149,
        "probabilities": {
          "human": 0.9870592355728149,
          "aigc": 0.012940708547830582
        },
        "text": "D.1.1. INTRA-LAYER PARETO OPTIMAL KV CACHE PRECISION PAIR PRUNING",
        "title": "第19页-段落5",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_583",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997264742851257,
        "probabilities": {
          "human": 0.00027347306604497135,
          "aigc": 0.9997264742851257
        },
        "text": "The intra-layer KV cache quantization precision pair pruning based on Pareto frontier are available in Table 4. The calibration\ndataset is the first 20 prompts from the zeroshot GSM8K dataset. The Pareto optimal KV cache precision pairs in most layers\nare the key-first set {KV8, K8V4, KV4, K4V2, KV2}, indicating that the observation that key cache is more important than\nvalue cache holds.",
        "title": "第19页-段落6",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_584",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9954029321670532,
        "probabilities": {
          "human": 0.004597045946866274,
          "aigc": 0.9954029321670532
        },
        "text": "When both key and value cache are quantized along the token dimension, only the first layer in Llama-3.1-8B-Instruct and\nMistral-7B-Instruct-v0.3 prefers other KV precision pairs and all layers in Qwen2.5-{14B, 32B}-Instruct select the key-first\nset. In contrast, K8V2 outperforms KV4 in four important layers of Qwen2.5-{3B, 7B}-Instruct, indicating that uniform\n4-bit key quantization may lead to model accuracy degradation as in Table 13.",
        "title": "第19页-段落7",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_585",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9972010850906372,
        "probabilities": {
          "human": 0.0027989435475319624,
          "aigc": 0.9972010850906372
        },
        "text": "When utilizing the KIVI-like key per-channel-asym and value per-token-asym quantization mode, more layers show diverse\npreference of Pareto optimal KV cache quantization precision pairs. In these layers, K4V8 and K2V4 outperform K8V4 and\nK4V2, which means that lower precision key is better than lower precision value in terms of attention errors. It indicates\nthat per-channel key quantization can effectively reduce quantization errors.",
        "title": "第19页-段落8",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_586",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9744513034820557,
        "probabilities": {
          "human": 0.9744513034820557,
          "aigc": 0.02554865926504135
        },
        "text": "D.1.2. INTER-LAYER CLUSTERING BASED ON ATTENTION ERRORS",
        "title": "第19页-段落9",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_587",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992676377296448,
        "probabilities": {
          "human": 0.0007323187310248613,
          "aigc": 0.9992676377296448
        },
        "text": "After the intra-layer KV cache quantization precision pair pruning, we apply the inter-layer clustering among the layers with\nthe same precision pair set. The clustering algorithm is DBSCAN (Ester et al., 1996) with the hyper-parameter epsilon=0.05\nand min_samples=2. As demonstrated in Table 10, we successfully reduce the exponential component of search space size\nfrom the number of transformer layers L e.g. 28∼64 to the number of clustered layer groups G e.g. 4∼8. Utilizing the\ntwo-level search space pruning, the total number of combinations of candidate KV cache precision pairs is significantly\nreduced from 9L to 5G or 6G. In Llama-3.1-8B-Instruct, 9L = 932 ≈3.4 × 1030, while 5G = 56 = 15625.",
        "title": "第19页-段落10",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_588",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994449019432068,
        "probabilities": {
          "human": 0.0005550610367208719,
          "aigc": 0.9994449019432068
        },
        "text": "In the layer-wise relative attention output errors with per-token-asym KV cache quantization of Llama-3.1-8B-Instruct in\nFigure 13, the highly sensitive layers include layer-{0, 1, 2, 3, 4, 23, 24, 25, 27, 28, 29}, while the insensitive layers include\nlayer-{8, 9, 10, 11, 13, 14, 15, 20, 30}. Layers in these two classes are correctly clustered into different groups. Similar\nphenomenon can also be observed in Qwen2.5-7B-Instruct per-token-asym and KIVI-like quantization modes in Figure\n16 and 18, respectively. Therefore, we can conclude that the proposed multi-objective Pareto frontier based intra-layer\npruning and inter-layer clustering algorithms successfully reduce the search space by considering the inherent layer-wise\nsensitivities.",
        "title": "第19页-段落11",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_589",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9901118874549866,
        "probabilities": {
          "human": 0.9901118874549866,
          "aigc": 0.009888106025755405
        },
        "text": "D.2. Searched layer-wise KV precision pairs",
        "title": "第19页-段落12",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_590",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999799907207489,
        "probabilities": {
          "human": 0.0002001082757487893,
          "aigc": 0.999799907207489
        },
        "text": "The final searched layer-wise mixed precision KV cache quantization precision pairs of different LLMs and KV quantization\nmodes are available in Table 11. Some clustered layer groups in Table 10 choose the same KV cache quantization pairs under\nthe given memory consumption and/or accuracy degradation constraints. The number of utilized KV cache quantization\nprecision pairs is reduced from 6 ∼8 to 2 ∼5 in the tested Llama-3.1-8B-Instruct, Qwen2.5-3B-Instruct, and Qwen2.5-7B-\nInstruct models. In addition, the significantly diverse layer-wise KV precision pair distribution in Table 11 indicates that\nthere are not clear heuristic rules based on layer depths to identify layer importance and sensitivity to KV cache quantization.\nTherefore, we need to measure the model accuracies considering their complicated nonlinear dependencies to layer-wise KV\ncache precision pairs and utilize accuracies to distinguish the whole model level KV cache precision pair combinations.",
        "title": "第19页-段落13",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_591",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9761645793914795,
        "probabilities": {
          "human": 0.9761645793914795,
          "aigc": 0.023835444822907448
        },
        "text": "D.3. Pareto Frontier with the GSM8K Calibration Dataset",
        "title": "第19页-段落14",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_592",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9976219534873962,
        "probabilities": {
          "human": 0.0023780737537890673,
          "aigc": 0.9976219534873962
        },
        "text": "We use the open-sourced package optuna (Akiba et al., 2019) with the MOEA/D algorithm (Zhang & Li, 2007) for the final\nsearch with the model memory usage and inference accuracy of the first 200 4-shot GSM8K prompts. The multi-objective\nsearch of the Pareto optimal layer-wise KV cache quantization precision pairs of Llama-3.1-8B-Instruct, Mistral-7B-Instruct-\nv0.3, Qwen2.5-3B-Instruct, and Qwen2.5-7B-Instruct with the KIVI and per-token-asym quantization modes are available",
        "title": "第19页-段落15",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_593",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975010752677917,
        "probabilities": {
          "human": 0.9975010752677917,
          "aigc": 0.002498938934877515
        },
        "text": "19",
        "title": "第19页-段落16",
        "page_number": 19,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_594",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第20页-段落1",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_595",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998290538787842,
        "probabilities": {
          "human": 0.0001709350326564163,
          "aigc": 0.9998290538787842
        },
        "text": "Table 10: Inter-layer clustering results by clustering among the layers with the same pruned intra-layer KV cache quantization\nprecision pairs. For example, layers 14 and 20 demonstrate higher sensitivity than layers 3, 13, and 27 as visualized in\nFigure 16. They are clustered into different group, validating the effectiveness of our intra-layer pruning and inter-layer\nclustering.",
        "title": "第20页-段落2",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_596",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8827522993087769,
        "probabilities": {
          "human": 0.8827522993087769,
          "aigc": 0.11724772304296494
        },
        "text": "Model name\nL\nKey quant. mode\nG\nGrouped layer ids",
        "title": "第20页-段落3",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_597",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.723736584186554,
        "probabilities": {
          "human": 0.723736584186554,
          "aigc": 0.27626341581344604
        },
        "text": "Llama-3.1-8B-Instruct\n32\nper-token-asym\n6\n{0}, {1∼4, 7, 13, 18, 25, 27, 31}, {5, 6, 12, 21, 26, 28}, {8∼11, 14∼17, 20, 30},\n{19, 22}, {23, 24, 29}",
        "title": "第20页-段落4",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_598",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5013912320137024,
        "probabilities": {
          "human": 0.5013912320137024,
          "aigc": 0.49860879778862
        },
        "text": "per-channel-asym\n6\n{0}, {1∼3, 7, 29, 31}, {4, 25, 27}, {5, 21, 23, 24}, {6, 8∼12, 14∼16, 18∼20, 22,\n26, 28, 30}, {13, 17}",
        "title": "第20页-段落5",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_599",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7163418531417847,
        "probabilities": {
          "human": 0.7163418531417847,
          "aigc": 0.28365814685821533
        },
        "text": "per-token-asym\n5\n{0}, {1, 2}, {3, 4, 23, 31}, {5, 6}, {7∼22, 24∼30}",
        "title": "第20页-段落6",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_600",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6653205156326294,
        "probabilities": {
          "human": 0.3346794843673706,
          "aigc": 0.6653205156326294
        },
        "text": "per-channel-asym\n8\n{0, 1, 31}, {2∼4}, {6, 27, 29}, {7, 8, 10, 18}, {9, 14}, {5, 21∼26, 28, 30},\n{11∼13, 15, 17, 19, 20}, {16}",
        "title": "第20页-段落7",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_601",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997491240501404,
        "probabilities": {
          "human": 0.9997491240501404,
          "aigc": 0.00025086820824071765
        },
        "text": "Mistral-7B-Instruct-v0.3\n32",
        "title": "第20页-段落8",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_602",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8910624384880066,
        "probabilities": {
          "human": 0.10893752425909042,
          "aigc": 0.8910624384880066
        },
        "text": "Qwen2.5-3B-Instruct\n36\nper-token-asym\n8\n{0}, {1, 3∼6, 8, 9, 12, 13, 15, 20}, {2, 14, 23, 35}, {7, 11, 16, 25, 28, 32}, {10, 19,\n24, 26, 33}, {17, 30, 31, 34}, {21, 22}, {18, 27, 29}",
        "title": "第20页-段落9",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_603",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8973084092140198,
        "probabilities": {
          "human": 0.10269162058830261,
          "aigc": 0.8973084092140198
        },
        "text": "per-channel-asym\n8\n{0, 1}, {2, 4}, {34, 35}, {3, 6, 11, 13, 23}, {5, 7, 25, 32, 33}, {8, 16, 18, 21, 22,\n24, 26, 27, 30}, {9, 10, 14, 15, 17, 19, 20, 29, 31}, {12, 28}",
        "title": "第20页-段落10",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_604",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6985176801681519,
        "probabilities": {
          "human": 0.30148229002952576,
          "aigc": 0.6985176801681519
        },
        "text": "Qwen2.5-7B-Instruct\n28\nper-token-asym\n8\n{0}, {1, 2, 4, 5, 25}, {6, 19}, {7, 10, 11, 15, 23}, {8, 24}, {9, 12, 16∼18, 21, 22,\n26}, {14, 20}, {3, 13, 27}",
        "title": "第20页-段落11",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_605",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6221832633018494,
        "probabilities": {
          "human": 0.377816766500473,
          "aigc": 0.6221832633018494
        },
        "text": "per-channel-asym\n7\n{0, 2}, {1, 3}, {4, 5, 12, 22∼25}, {7, 9, 10, 13, 14, 16, 18∼21, 27}, {8, 26}, {11,\n15, 17}, {6}",
        "title": "第20页-段落12",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_606",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8745874166488647,
        "probabilities": {
          "human": 0.12541256844997406,
          "aigc": 0.8745874166488647
        },
        "text": "Qwen2.5-14B-Instruct\n48\nper-token-asym\n6\n{0∼2, 6, 11, 12, 19, 23∼25, 41}, {3∼5, 8}, {7, 10, 15}, {9, 13, 14, 31, 38, 39},\n{16∼18, 20, 21, 27, 28, 30, 32∼37, 40, 42∼44, 46, 47}, {22, 26, 29, 45}",
        "title": "第20页-段落13",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_607",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8437618613243103,
        "probabilities": {
          "human": 0.15623807907104492,
          "aigc": 0.8437618613243103
        },
        "text": "per-channel-asym\n7\n{0, 2}, {1, 3, 4}, {5, 6, 8, 9, 12}, {7, 10, 13, 15∼21, 23, 24, 26∼33, 35∼38,\n44∼47}, {11, 25, 41, 42}, {14, 39, 40, 43}, {22, 34}",
        "title": "第20页-段落14",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_608",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8860544562339783,
        "probabilities": {
          "human": 0.8860544562339783,
          "aigc": 0.11394558846950531
        },
        "text": "Qwen2.5-32B-Instruct\n64\nper-token-asym\n4\n{0, 2, 11, 12, 15, 33, 54, 57}, {1, 5, 7∼10, 13, 14, 17∼32, 34∼53, 55, 56, 58∼63},\n{3, 4}, {6, 16}",
        "title": "第20页-段落15",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_609",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7397207617759705,
        "probabilities": {
          "human": 0.7397207617759705,
          "aigc": 0.26027920842170715
        },
        "text": "per-channel-asym\n5\n{0∼4}, {11}, {5∼10, 12, 14, 16, 18∼23, 26∼28, 32}, {13, 15, 17, 22, 24, 25,\n29∼31, 33∼62}, {63}",
        "title": "第20页-段落16",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_610",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998204112052917,
        "probabilities": {
          "human": 0.00017964921426028013,
          "aigc": 0.9998204112052917
        },
        "text": "in Figure 8 and 9. In order to validate the effectiveness of the proposed two-stage intra-layer and inter-layer search space\npruning, we disable the pre-processing process and directly use the original full SL search space in Figure 10.",
        "title": "第20页-段落17",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_611",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9998692274093628,
        "probabilities": {
          "human": 0.0001307923812419176,
          "aigc": 0.9998692274093628
        },
        "text": "For each combination of model and quantization mode, we set a soft constraint on the equivalent precision at 4-bit and\n6-bit for optuna, conducting 200 search iterations for each setting. The search results are then merged for visualization. In\ncases where the two-stage intra-layer and inter-layer search space pruning is not applied, we set the maximum equivalent\nquantization precision to 6-bit and similarly perform 200 search iterations. Specifically, for the KIVI quantization method,\nwe set the residual length to 32 and the group size to 32.",
        "title": "第20页-段落18",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_612",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9986132383346558,
        "probabilities": {
          "human": 0.0013867749366909266,
          "aigc": 0.9986132383346558
        },
        "text": "Note that for Qwen-2.5-7B with the KIVI quantization mode, the result from 200 search iterations appeared abnormal.\nTherefore, we extended the search to 500 iterations to obtain the final result.",
        "title": "第20页-段落19",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_613",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9942230582237244,
        "probabilities": {
          "human": 0.005776972975581884,
          "aigc": 0.9942230582237244
        },
        "text": "E. Correlation of Model- and Layer-wise KV Cache Quantization Sensitivity with Attention\nPatterns",
        "title": "第20页-段落20",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_614",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997372031211853,
        "probabilities": {
          "human": 0.00026283605257049203,
          "aigc": 0.9997372031211853
        },
        "text": "According to the layer-wise attention score errors of Llama-3.1-8B-Instruct in Figure 3 and Qwen2.5-7B-Instruct in Figure\n16, we can observe the clear layer-wise difference in the same LLM. In this section, we try to explain the reason of the\ndifference from the attention pattern perspective as in Figure 11 and 12. In which, we visualize block level attention scores\nof the first 4 heads with block size 4 in the prefilling and decoding stages, and horizontal and vertical axes represent the\nkey and query dimensions respectively. Yellow, green, and purple points indicate high, medium, and low attention scores,\nrespectively. We find out that the more complex and dynamic attention patterns usually lead to larger attention score errors\nand sensitivity to KV cache quantization of intermediate transformer layers and the whole LLMs.",
        "title": "第20页-段落21",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_615",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997259974479675,
        "probabilities": {
          "human": 0.0002739595074672252,
          "aigc": 0.9997259974479675
        },
        "text": "Take Llama-3.1-8B-Instruct as an example, layer 12 and 13 are in the group with high attention score errors, while layer 0\nand 31 are in the medium error group and layer 2 and 23 are in the low error group. Analyzing the attention patterns of these\nlayer in the below Figure 11, we can conclude that heads in the layer 12 and 13 have dynamic and non-sparse attention\npatterns, which are called as retrieval heads (Tang et al., 2025; Xiao et al., 2025). In contrast, heads in layer 0, 2, 23 and 31\nhave more static attention patterns like attention sink and recent window, which are called as streaming heads (Xiao et al.,\n2025; 2024).",
        "title": "第20页-段落22",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_616",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9930093288421631,
        "probabilities": {
          "human": 0.9930093288421631,
          "aigc": 0.006990684662014246
        },
        "text": "20",
        "title": "第20页-段落23",
        "page_number": 20,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_617",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第21页-段落1",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_618",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第21页-段落2",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_619",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落3",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_620",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第21页-段落4",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_621",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落5",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_622",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落6",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_623",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落7",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_624",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落8",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_625",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落9",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_626",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落10",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_627",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落11",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_628",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落12",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_629",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落13",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_630",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落14",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_631",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落15",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_632",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落16",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_633",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落17",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_634",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落18",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_635",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落19",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_636",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落20",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_637",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落21",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_638",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落22",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_639",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落23",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_640",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落24",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_641",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落25",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_642",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落26",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_643",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997159838676453,
        "probabilities": {
          "human": 0.9997159838676453,
          "aigc": 0.00028400219161994755
        },
        "text": "(a) Llama-3.1-8B-Instruct",
        "title": "第21页-段落27",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_644",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988213181495667,
        "probabilities": {
          "human": 0.9988213181495667,
          "aigc": 0.0011786321410909295
        },
        "text": "(b) Mistral-7B-Instruct-v0.3",
        "title": "第21页-段落28",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_645",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落29",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_646",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第21页-段落30",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_647",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落31",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_648",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第21页-段落32",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_649",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落33",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_650",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落34",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_651",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落35",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_652",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落36",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_653",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落37",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_654",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落38",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_655",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落39",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_656",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落40",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_657",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落41",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_658",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落42",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_659",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落43",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_660",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落44",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_661",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落45",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_662",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落46",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_663",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落47",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_664",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落48",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_665",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落49",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_666",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落50",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_667",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落51",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_668",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落52",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_669",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落53",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_670",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落54",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_671",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996947050094604,
        "probabilities": {
          "human": 0.9996947050094604,
          "aigc": 0.0003053279942832887
        },
        "text": "(c) Qwen2.5-3B-Instruct",
        "title": "第21页-段落55",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_672",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996275901794434,
        "probabilities": {
          "human": 0.9996275901794434,
          "aigc": 0.0003723653207998723
        },
        "text": "(d) Qwen2.5-7B-Instruct",
        "title": "第21页-段落56",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_673",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9731631278991699,
        "probabilities": {
          "human": 0.026836883276700974,
          "aigc": 0.9731631278991699
        },
        "text": "Figure 8: Pareto frontier of different models with the KIVI quantization mode on the first 200 data slices of the 4-shot\nGSM8K dataset.",
        "title": "第21页-段落57",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_674",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第21页-段落58",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_675",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落59",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_676",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落60",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_677",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落61",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_678",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第21页-段落62",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_679",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落63",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_680",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落64",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_681",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落65",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_682",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落66",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_683",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落67",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_684",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落68",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_685",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落69",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_686",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落70",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_687",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落71",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_688",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落72",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_689",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落73",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_690",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落74",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_691",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落75",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_692",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落76",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_693",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落77",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_694",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落78",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_695",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落79",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_696",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落80",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_697",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落81",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_698",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落82",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_699",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997159838676453,
        "probabilities": {
          "human": 0.9997159838676453,
          "aigc": 0.00028400219161994755
        },
        "text": "(a) Llama-3.1-8B-Instruct",
        "title": "第21页-段落83",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_700",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988213181495667,
        "probabilities": {
          "human": 0.9988213181495667,
          "aigc": 0.0011786321410909295
        },
        "text": "(b) Mistral-7B-Instruct-v0.3",
        "title": "第21页-段落84",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_701",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落85",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_702",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第21页-段落86",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_703",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落87",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_704",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第21页-段落88",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_705",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第21页-段落89",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_706",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落90",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_707",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第21页-段落91",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_708",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落92",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_709",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第21页-段落93",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_710",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落94",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_711",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第21页-段落95",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_712",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落96",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_713",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第21页-段落97",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_714",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第21页-段落98",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_715",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落99",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_716",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第21页-段落100",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_717",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落101",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_718",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第21页-段落102",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_719",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落103",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_720",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第21页-段落104",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_721",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落105",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_722",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第21页-段落106",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_723",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落107",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_724",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第21页-段落108",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_725",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落109",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_726",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第21页-段落110",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_727",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996947050094604,
        "probabilities": {
          "human": 0.9996947050094604,
          "aigc": 0.0003053279942832887
        },
        "text": "(c) Qwen2.5-3B-Instruct",
        "title": "第21页-段落111",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_728",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996275901794434,
        "probabilities": {
          "human": 0.9996275901794434,
          "aigc": 0.0003723653207998723
        },
        "text": "(d) Qwen2.5-7B-Instruct",
        "title": "第21页-段落112",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_729",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9529578685760498,
        "probabilities": {
          "human": 0.047042157500982285,
          "aigc": 0.9529578685760498
        },
        "text": "Figure 9: Pareto frontier of different models with the per-token-asym quantization mode on the first 200 data slices of the\n4-shot GSM8K dataset.",
        "title": "第21页-段落113",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_730",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960412979125977,
        "probabilities": {
          "human": 0.9960412979125977,
          "aigc": 0.003958654589951038
        },
        "text": "21",
        "title": "第21页-段落114",
        "page_number": 21,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_731",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第22页-段落1",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_732",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9866440892219543,
        "probabilities": {
          "human": 0.013355852104723454,
          "aigc": 0.9866440892219543
        },
        "text": "Table 11: Detailed searched layer-wise KV cache quantization precision pairs of different LLMs and KV cache quantization\nmodes by KVTuner.",
        "title": "第22页-段落2",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_733",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9567951560020447,
        "probabilities": {
          "human": 0.043204762041568756,
          "aigc": 0.9567951560020447
        },
        "text": "Model name\nQuant. mode\nEquivalent precision\nQuant. precision\nLayer ids",
        "title": "第22页-段落3",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_734",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989911913871765,
        "probabilities": {
          "human": 0.9989911913871765,
          "aigc": 0.001008782652206719
        },
        "text": "per-token-asym\n3.59\nK4V8\n0\nKV4\n5, 6, 8–12, 14–17, 20, 21, 26, 28, 30\nK4V2\n1–4, 7, 13, 18, 19, 22–25, 27, 29, 31",
        "title": "第22页-段落4",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_735",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986769556999207,
        "probabilities": {
          "human": 0.9986769556999207,
          "aigc": 0.0013230470940470695
        },
        "text": "5.44\nK8V4\n1–4, 7–11, 13–18, 20, 23–25, 27, 29–31\nKV4\n0, 5, 6, 12, 19, 21, 22, 26, 28",
        "title": "第22页-段落5",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_736",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9908199906349182,
        "probabilities": {
          "human": 0.9908199906349182,
          "aigc": 0.009180069901049137
        },
        "text": "K8V4\n13, 17\nKV4\n1–3, 7, 29, 31\nK4V2\n5, 6, 8–12, 14–16, 18–24, 26, 28, 30\nKV2\n0, 4, 25, 27",
        "title": "第22页-段落6",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_737",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998956918716431,
        "probabilities": {
          "human": 0.9998956918716431,
          "aigc": 0.00010427953384350985
        },
        "text": "Llama-3.1-8B-Instruct",
        "title": "第22页-段落7",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_738",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984763264656067,
        "probabilities": {
          "human": 0.9984763264656067,
          "aigc": 0.0015236601466313004
        },
        "text": "3.25",
        "title": "第22页-段落8",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_739",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第22页-段落9",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_740",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898958206176758,
        "probabilities": {
          "human": 0.9898958206176758,
          "aigc": 0.010104170069098473
        },
        "text": "K8V4\n4, 6, 8–12, 14–16, 18–20, 22, 25–28, 30\nKV4\n1–3, 7, 29, 31\nK4V2\n5, 21, 23, 24\nK2V4\n0\nKV2\n13, 17",
        "title": "第22页-段落10",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_741",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988459348678589,
        "probabilities": {
          "human": 0.9988459348678589,
          "aigc": 0.0011540140258148313
        },
        "text": "4.90",
        "title": "第22页-段落11",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_742",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9610924124717712,
        "probabilities": {
          "human": 0.9610924124717712,
          "aigc": 0.038907524198293686
        },
        "text": "K8V4\n17, 18, 27, 29–31, 34\nK8V2\n0\nKV4\n7, 10, 11, 19, 21, 22, 24–26, 28, 32, 33\nK4V2\n1–6, 8, 9, 12, 13–16, 20, 23, 35",
        "title": "第22页-段落12",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_743",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9969154596328735,
        "probabilities": {
          "human": 0.9969154596328735,
          "aigc": 0.003084570402279496
        },
        "text": "4.00",
        "title": "第22页-段落13",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_744",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993643164634705,
        "probabilities": {
          "human": 0.9993643164634705,
          "aigc": 0.0006357330130413175
        },
        "text": "per-token-asym",
        "title": "第22页-段落14",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_745",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975718855857849,
        "probabilities": {
          "human": 0.9975718855857849,
          "aigc": 0.0024281046353280544
        },
        "text": "5.06\nKV8\n0\nK8V4\n1, 3–6, 8–10, 12, 13, 15, 17–20, 24, 26, 27, 29–31, 33, 34\nK4V2\n2, 7, 11, 14, 16, 21–23, 25, 28, 32, 35",
        "title": "第22页-段落15",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_746",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9915786981582642,
        "probabilities": {
          "human": 0.9915786981582642,
          "aigc": 0.00842136051505804
        },
        "text": "K4V8\n0–1\nK4V2\n3, 5–11, 13–27, 29–33\nKV4\n34–35\nK2V4\n2, 4\nKV2\n12, 28",
        "title": "第22页-段落16",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_747",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998051524162292,
        "probabilities": {
          "human": 0.9998051524162292,
          "aigc": 0.00019489694386720657
        },
        "text": "Qwen2.5-3B-Instruct",
        "title": "第22页-段落17",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_748",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983561635017395,
        "probabilities": {
          "human": 0.9983561635017395,
          "aigc": 0.0016438420861959457
        },
        "text": "3.17",
        "title": "第22页-段落18",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_749",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第22页-段落19",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_750",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9849842190742493,
        "probabilities": {
          "human": 0.9849842190742493,
          "aigc": 0.015015784651041031
        },
        "text": "KV8\n0–1\nKV4\n3, 5–7, 11, 13, 23, 25, 32, 33\nK4V2\n8–10, 14–22, 24, 26, 27, 29–31\nK2V4\n34–35\nKV2\n2, 4, 12, 28",
        "title": "第22页-段落20",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_751",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990167617797852,
        "probabilities": {
          "human": 0.9990167617797852,
          "aigc": 0.0009831846691668034
        },
        "text": "3.44",
        "title": "第22页-段落21",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_752",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9748742580413818,
        "probabilities": {
          "human": 0.9748742580413818,
          "aigc": 0.025125738233327866
        },
        "text": "KV8\n0\nK8V2\n3, 13, 27\nKV4\n6, 7, 9–12, 14–23, 26\nK4V2\n1, 2, 4, 5, 8, 24, 25",
        "title": "第22页-段落22",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_753",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9969154596328735,
        "probabilities": {
          "human": 0.9969154596328735,
          "aigc": 0.003084570402279496
        },
        "text": "4.00",
        "title": "第22页-段落23",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_754",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993643164634705,
        "probabilities": {
          "human": 0.9993643164634705,
          "aigc": 0.0006357330130413175
        },
        "text": "per-token-asym",
        "title": "第22页-段落24",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_755",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979142546653748,
        "probabilities": {
          "human": 0.9979142546653748,
          "aigc": 0.0020857341587543488
        },
        "text": "5.00\nK8V4\n8, 9, 12, 14, 16–18, 20–22, 24, 26\nK8V2\n0, 3, 13, 27\nKV4\n1, 2, 4–7, 10, 11, 15, 19, 23, 25",
        "title": "第22页-段落25",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_756",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997767806053162,
        "probabilities": {
          "human": 0.9997767806053162,
          "aigc": 0.00022326793987303972
        },
        "text": "Qwen2.5-7B-Instruct",
        "title": "第22页-段落26",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_757",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979771971702576,
        "probabilities": {
          "human": 0.9979771971702576,
          "aigc": 0.0020228184293955564
        },
        "text": "3.92\nKV8\n0, 2, 6, 11, 15, 17\nKV4\n4, 5, 8, 12, 22–26\nKV2\n1, 3, 7, 9, 10, 13, 14, 16, 18–21, 27",
        "title": "第22页-段落27",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_758",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.965864896774292,
        "probabilities": {
          "human": 0.965864896774292,
          "aigc": 0.03413510322570801
        },
        "text": "KV8\n0, 2, 7, 9, 10, 13, 14, 16, 18–21, 27\nK8V4\n4, 5, 12, 22, 23, 24, 25\nK4V2\n11, 15, 17\nK2V4\n1, 3\nKV2\n6, 8, 26",
        "title": "第22页-段落28",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_759",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第22页-段落29",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_760",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984229803085327,
        "probabilities": {
          "human": 0.9984229803085327,
          "aigc": 0.0015770881436765194
        },
        "text": "5.96",
        "title": "第22页-段落30",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_761",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993776679039001,
        "probabilities": {
          "human": 0.0006223022355698049,
          "aigc": 0.9993776679039001
        },
        "text": "Compared with Llama-3.1-8B-Instruct which has the high ratio of heads with static attention patterns, Qwen2.5-7B-Instruct\nconsists of many heads with mixture of dynamic retrieval heads and other static patterns. It may explain why Qwen2.5-7B-\nInstruct is more unstable to KV cache quantization as in Table 2. Layer 5, 12, 21, and 27 have similar attention patterns,\nbut the relative strength of retrieval and streaming heads leads to the difference of layer-wise sensitivity to KV cache\nquantization.",
        "title": "第22页-段落31",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_762",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997820258140564,
        "probabilities": {
          "human": 0.00021801452385261655,
          "aigc": 0.9997820258140564
        },
        "text": "However, the sensitivity to KV cache quantization is the inherent model property which can be learned offline. Therefore, it\nis necessary to apply layer-wise mixed precision KV cache quantization and maintain high precision of key cache than value\ncache with multi-objective optimization KV precision pair tuning as proposed in this work. KVTuner thus makes equivalent\n4-bit and even lower KV cache quantization nearly lossless in the sensitive models like Qwen2.5-7B-Instruct.",
        "title": "第22页-段落32",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_763",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9908952713012695,
        "probabilities": {
          "human": 0.009104710072278976,
          "aigc": 0.9908952713012695
        },
        "text": "E.1. More KV Cache Quantization Results on General and Mathematical Reasoning Datasets",
        "title": "第22页-段落33",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_764",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999286949634552,
        "probabilities": {
          "human": 0.0007130606682039797,
          "aigc": 0.999286949634552
        },
        "text": "The experimental results of the selected 5 LLMs on the general and mathematical reasoning datasets with uniform KV\ncache quantization precision pairs are available in Table 12 and 13. To simulate the Openai o1 like long CoT reasoning\nprocess, the few-shot CoTs in the GSM8K dataset are treated as a multi-turn conversation, which is enabled with the flags",
        "title": "第22页-段落34",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_765",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9942863583564758,
        "probabilities": {
          "human": 0.9942863583564758,
          "aigc": 0.005713701713830233
        },
        "text": "22",
        "title": "第22页-段落35",
        "page_number": 22,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_766",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第23页-段落1",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_767",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第23页-段落2",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_768",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第23页-段落3",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_769",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第23页-段落4",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_770",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5493924021720886,
        "probabilities": {
          "human": 0.45060762763023376,
          "aigc": 0.5493924021720886
        },
        "text": "Trials\nPareto frontier\nUnified precision",
        "title": "第23页-段落5",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_771",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第23页-段落6",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_772",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第23页-段落7",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_773",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第23页-段落8",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_774",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第23页-段落9",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_775",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第23页-段落10",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_776",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第23页-段落11",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_777",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第23页-段落12",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_778",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第23页-段落13",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_779",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9879277348518372,
        "probabilities": {
          "human": 0.9879277348518372,
          "aigc": 0.012072299607098103
        },
        "text": "Accuracy",
        "title": "第23页-段落14",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_780",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第23页-段落15",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_781",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第23页-段落16",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_782",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第23页-段落17",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_783",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第23页-段落18",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_784",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第23页-段落19",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_785",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第23页-段落20",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_786",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99623042345047,
        "probabilities": {
          "human": 0.99623042345047,
          "aigc": 0.003769563976675272
        },
        "text": "0.1",
        "title": "第23页-段落21",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_787",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第23页-段落22",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_788",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9917709827423096,
        "probabilities": {
          "human": 0.9917709827423096,
          "aigc": 0.008229011669754982
        },
        "text": "0.0",
        "title": "第23页-段落23",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_789",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第23页-段落24",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_790",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.5554552674293518,
        "probabilities": {
          "human": 0.4445447325706482,
          "aigc": 0.5554552674293518
        },
        "text": "2\n3\n4\n5\n6\n7\n8",
        "title": "第23页-段落25",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_791",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第23页-段落26",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_792",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858165979385376,
        "probabilities": {
          "human": 0.9858165979385376,
          "aigc": 0.014183443039655685
        },
        "text": "Equivalent KV cache bits",
        "title": "第23页-段落27",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_793",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997159838676453,
        "probabilities": {
          "human": 0.9997159838676453,
          "aigc": 0.00028400219161994755
        },
        "text": "(a) Llama-3.1-8B-Instruct",
        "title": "第23页-段落28",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_794",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996123909950256,
        "probabilities": {
          "human": 0.9996123909950256,
          "aigc": 0.00038760947063565254
        },
        "text": "(b) Qwen2.5-3B-Instruct",
        "title": "第23页-段落29",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_795",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9979877471923828,
        "probabilities": {
          "human": 0.0020122698042541742,
          "aigc": 0.9979877471923828
        },
        "text": "Figure 10: Pareto frontier of different models with the per-token-asym quantization model on the first 200 data slices of the\n4-shot GSM8K dataset without intra-layer and inter-layer search space pruning.",
        "title": "第23页-段落30",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_796",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997255206108093,
        "probabilities": {
          "human": 0.00027448791661299765,
          "aigc": 0.9997255206108093
        },
        "text": "fewshot_as_multiturn and apply_chat_template in lm-evaluation-harness. In which cases, questions are provided as user\ncontent and answers are provided as assistant responses instead of directly using the given standard answers. Table 14\nsummarizes the results of 8 LLMs including Qwen2.5-{14, 32B}-Instruct under the fewshot_as_multiturn setting.",
        "title": "第23页-段落31",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_797",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996533393859863,
        "probabilities": {
          "human": 0.00034664961276575923,
          "aigc": 0.9996533393859863
        },
        "text": "There are limited long output mathematical reasoning datasets in lm-evaluation-harness (Gao et al., 2024) and the evaluation\nof the long context generation is an open question. Therefore, we enable KV cache quantization in both the prefilling and\ndecoding stages to amplify the effects to final generation results caused by KV cache quantization error accumulation, which\nmakes distinguishing different quantization methods easier. For the KIVI quantization mode, we utilize the HQQ quantizer\nfrom HuggingFace’s implementation, with both the residual length and group size set to 32.",
        "title": "第23页-段落32",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_798",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9971024394035339,
        "probabilities": {
          "human": 0.0028974872548133135,
          "aigc": 0.9971024394035339
        },
        "text": "According to Table 12, 13, and 14, most LLMs, including Llama-3.1-8B-Instruct, Mistral-7B-Instruct-v0.3, Qwen2.5-{14B,\n32B}-Instruct, are robust to low-bit KV cache quantization. Although error accumulation caused by KV cache quantization\nstarts from the prefilling stage, the high KV cache quantization precision pair KV8 with KIVI or per-token-asym quantization\nmode are still generally lossless, except Qwen2.5-Math-7B-Instruct. The uniform KV cache quantization precision pairs\nKV4 or even K4V2 with the KIVI quantization mode can achieve nearly lossless 4× or even 5.3× KV cache compression,\nrespectively. KV4 with the simple per-token-asym mode also results in negligible accuracy loss in Llama-3.1-8B-Instruct\nand Mistral-7B-Instruct-v0.3 as shown in Table 12. KIVI does outperform the per-token-asym quantization mode in the\nlow-precision settings such as KV4, K4V2, and KV2, especially in Qwen2.5-3B-Instruct-AWQ and Qwen2.5-7B-Instruct as\ndemonstrated in Figure 13.",
        "title": "第23页-段落33",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_799",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9980912804603577,
        "probabilities": {
          "human": 0.001908725593239069,
          "aigc": 0.9980912804603577
        },
        "text": "As shown in Figure 14, the larger Qwen2.5-{14B,32B}-Instruct models are robust than the smaller Qwen2.5-{3B, 7B,\nMath-7B}-Instruct and the weight quantized Qwen2.5-3B-Instruct-AWQ models. In addition, comparing Qwen2.5-3B-\nInstruct-AWQ and Qwen2.5-3B-Instruct, we can conclude that model weight quantization with AWQ does not affect the\nmodel-level sensitivity to KV cache quantization. The increasing GSM8K accuracy with the longer CoTs under the half\nprecision BF16 KV cache setting indicates that most Qwen2.5 models benefit from longer CoTs. We also obverse that\n16-shot CoTs with K4V2 KV cache precision outperforms the 4-shot CoTs with BF16 KV cache precision on the larger\nQwen2.5-{14B,32B}-Instruct models. It indicates that longer CoT with lower and mixed precision KV cache outperforms\nuniform precision counterparts as in Section 6.2. In other words, mixed precision key cache quantization with higher\nprecision key can achieve both memory usage and inference accuracy improvement than equal precision key and value\ncache quantization.",
        "title": "第23页-段落34",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_800",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.996189296245575,
        "probabilities": {
          "human": 0.996189296245575,
          "aigc": 0.003810708876699209
        },
        "text": "23",
        "title": "第23页-段落35",
        "page_number": 23,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_801",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第24页-段落1",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_802",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落2",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_803",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落3",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_804",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落4",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_805",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落5",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_806",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落6",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_807",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落7",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_808",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落8",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_809",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落9",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_810",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落10",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_811",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落11",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_812",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落12",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_813",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落13",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_814",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落14",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_815",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落15",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_816",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落16",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_817",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落17",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_818",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落18",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_819",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9806114435195923,
        "probabilities": {
          "human": 0.019388573244214058,
          "aigc": 0.9806114435195923
        },
        "text": "(a) Layer-0 with recent attention patterns (medium attention score errors)",
        "title": "第24页-段落19",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_820",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落20",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_821",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落21",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_822",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落22",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_823",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落23",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_824",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落24",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_825",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落25",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_826",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落26",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_827",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落27",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_828",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落28",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_829",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落29",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_830",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落30",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_831",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落31",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_832",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落32",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_833",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落33",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_834",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落34",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_835",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落35",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_836",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落36",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_837",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.951318085193634,
        "probabilities": {
          "human": 0.048681940883398056,
          "aigc": 0.951318085193634
        },
        "text": "(b) Layer-2 with attention sinks (low attention score errors)",
        "title": "第24页-段落37",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_838",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落38",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_839",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落39",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_840",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落40",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_841",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落41",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_842",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落42",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_843",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落43",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_844",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落44",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_845",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落45",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_846",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落46",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_847",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落47",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_848",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落48",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_849",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落49",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_850",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落50",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_851",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落51",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_852",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落52",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_853",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落53",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_854",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落54",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_855",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8831467032432556,
        "probabilities": {
          "human": 0.1168532520532608,
          "aigc": 0.8831467032432556
        },
        "text": "(c) Layer-12 with retrieval heads (high attention score errors)",
        "title": "第24页-段落55",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_856",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落56",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_857",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落57",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_858",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落58",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_859",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落59",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_860",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落60",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_861",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落61",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_862",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落62",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_863",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落63",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_864",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落64",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_865",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落65",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_866",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落66",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_867",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落67",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_868",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落68",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_869",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落69",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_870",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落70",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_871",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落71",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_872",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落72",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_873",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9404995441436768,
        "probabilities": {
          "human": 0.059500496834516525,
          "aigc": 0.9404995441436768
        },
        "text": "(d) Layer-13 with retrieval heads (high attention score errors)",
        "title": "第24页-段落73",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_874",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落74",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_875",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落75",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_876",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落76",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_877",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落77",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_878",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落78",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_879",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落79",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_880",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落80",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_881",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落81",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_882",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落82",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_883",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落83",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_884",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落84",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_885",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落85",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_886",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落86",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_887",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落87",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_888",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落88",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_889",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落89",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_890",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落90",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_891",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.903145432472229,
        "probabilities": {
          "human": 0.09685458242893219,
          "aigc": 0.903145432472229
        },
        "text": "(e) Layer-23 with attention sink (low attention score errors)",
        "title": "第24页-段落91",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_892",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第24页-段落92",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_893",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第24页-段落93",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_894",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第24页-段落94",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_895",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第24页-段落95",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_896",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第24页-段落96",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_897",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第24页-段落97",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_898",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第24页-段落98",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_899",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落99",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_900",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落100",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_901",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落101",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_902",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第24页-段落102",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_903",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第24页-段落103",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_904",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第24页-段落104",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_905",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落105",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_906",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落106",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_907",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落107",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_908",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第24页-段落108",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_909",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9909850358963013,
        "probabilities": {
          "human": 0.009014918468892574,
          "aigc": 0.9909850358963013
        },
        "text": "(f) Layer-31 with mixture of retrieval and streaming heads (medium attention\nscore errors)",
        "title": "第24页-段落109",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_910",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995023012161255,
        "probabilities": {
          "human": 0.0004976845812052488,
          "aigc": 0.9995023012161255
        },
        "text": "Figure 11: Selected layer-wise attention patterns of Llama-3.1-8B-Instruct model and the first prompt in the 0-shot\nGSM8K dataset. Many layers and heads of Llama-3.1-8B-Instruct have simple and streaming attention patterns which\nhighly concentrated and sparse attention scores. As a result, the attention score errors in these layers are medium or low.\nIn contrast, layers with retrieval or mixed attention patterns, whose attention scores are non-sparse, normally show high\nattention score errors. We also observe that the attention patterns of query heads in the same group and sharing the same\nkey cache are highly similar, which may indicate that we can apply attention head group-wise KV cache management for\nbetter accuracy.",
        "title": "第24页-段落110",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_911",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99733966588974,
        "probabilities": {
          "human": 0.99733966588974,
          "aigc": 0.0026603268925100565
        },
        "text": "24",
        "title": "第24页-段落111",
        "page_number": 24,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_912",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第25页-段落1",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_913",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落2",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_914",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落3",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_915",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落4",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_916",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落5",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_917",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落6",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_918",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落7",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_919",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落8",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_920",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落9",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_921",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落10",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_922",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落11",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_923",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落12",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_924",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落13",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_925",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落14",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_926",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落15",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_927",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落16",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_928",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落17",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_929",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落18",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_930",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9951584935188293,
        "probabilities": {
          "human": 0.004841444548219442,
          "aigc": 0.9951584935188293
        },
        "text": "(a) Layer-0 with mixture of recent window, re-access, and retrieval heads\n(high attention score errors)",
        "title": "第25页-段落19",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_931",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落20",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_932",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落21",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_933",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落22",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_934",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落23",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_935",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落24",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_936",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落25",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_937",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落26",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_938",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落27",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_939",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落28",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_940",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落29",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_941",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落30",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_942",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落31",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_943",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落32",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_944",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落33",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_945",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落34",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_946",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落35",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_947",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落36",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_948",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9952556490898132,
        "probabilities": {
          "human": 0.0047443462535738945,
          "aigc": 0.9952556490898132
        },
        "text": "(b) Layer-1 with mixture of recent window and re-access patterns (medium\nattention score errors)",
        "title": "第25页-段落37",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_949",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落38",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_950",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落39",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_951",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落40",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_952",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落41",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_953",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落42",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_954",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落43",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_955",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落44",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_956",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落45",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_957",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落46",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_958",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落47",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_959",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落48",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_960",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落49",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_961",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落50",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_962",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落51",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_963",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落52",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_964",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落53",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_965",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落54",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_966",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9861255288124084,
        "probabilities": {
          "human": 0.013874487951397896,
          "aigc": 0.9861255288124084
        },
        "text": "(c) Layer-5 with mixture of retrieval and streaming heads (low attention\nscore errors)",
        "title": "第25页-段落55",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_967",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落56",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_968",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落57",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_969",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落58",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_970",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落59",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_971",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落60",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_972",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落61",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_973",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落62",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_974",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落63",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_975",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落64",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_976",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落65",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_977",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落66",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_978",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落67",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_979",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落68",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_980",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落69",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_981",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落70",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_982",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落71",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_983",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落72",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_984",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9909817576408386,
        "probabilities": {
          "human": 0.009018276818096638,
          "aigc": 0.9909817576408386
        },
        "text": "(d) Layer-12 with mixture of retrieval and streaming heads (medium\nattention score errors)",
        "title": "第25页-段落73",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_985",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落74",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_986",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落75",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_987",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落76",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_988",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落77",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_989",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落78",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_990",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落79",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_991",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落80",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_992",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落81",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_993",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落82",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_994",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落83",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_995",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落84",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_996",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落85",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_997",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落86",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_998",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落87",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_999",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落88",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1000",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落89",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1001",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落90",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1002",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9861147403717041,
        "probabilities": {
          "human": 0.01388524379581213,
          "aigc": 0.9861147403717041
        },
        "text": "(e) Layer-21 with mixture of retrieval heads and attention sinks (medium\nattention score errors)",
        "title": "第25页-段落91",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1003",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.925349235534668,
        "probabilities": {
          "human": 0.925349235534668,
          "aigc": 0.07465074956417084
        },
        "text": "Head 0",
        "title": "第25页-段落92",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1004",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9747528433799744,
        "probabilities": {
          "human": 0.9747528433799744,
          "aigc": 0.025247154757380486
        },
        "text": "Head 1",
        "title": "第25页-段落93",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1005",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9337968230247498,
        "probabilities": {
          "human": 0.9337968230247498,
          "aigc": 0.06620314717292786
        },
        "text": "Head 2",
        "title": "第25页-段落94",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1006",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9377502202987671,
        "probabilities": {
          "human": 0.9377502202987671,
          "aigc": 0.06224982440471649
        },
        "text": "Head 3",
        "title": "第25页-段落95",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1007",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第25页-段落96",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1008",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第25页-段落97",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1009",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第25页-段落98",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1010",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落99",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1011",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落100",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1012",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落101",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1013",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9117214679718018,
        "probabilities": {
          "human": 0.9117214679718018,
          "aigc": 0.08827854692935944
        },
        "text": "Query Position",
        "title": "第25页-段落102",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1014",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第25页-段落103",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1015",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第25页-段落104",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1016",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落105",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1017",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落106",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1018",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落107",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1019",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7453110218048096,
        "probabilities": {
          "human": 0.7453110218048096,
          "aigc": 0.2546890377998352
        },
        "text": "Key Position",
        "title": "第25页-段落108",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1020",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9906863570213318,
        "probabilities": {
          "human": 0.009313656017184258,
          "aigc": 0.9906863570213318
        },
        "text": "(f) Layer-27 with mixture of retrieval heads and attention sinks (high atten-\ntion score errors)",
        "title": "第25页-段落109",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1021",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993852376937866,
        "probabilities": {
          "human": 0.0006146997911855578,
          "aigc": 0.9993852376937866
        },
        "text": "Figure 12: Selected layer-wise attention patterns of Qwen2.5-7B-Instruct model and the first prompt in the 0-shot GSM8K\ndataset. Most layers and heads of Qwen2.5-7B-Instruct have complex attention patterns, such as retrieval, and mixture of\nretrieval and recent or attention sink patterns. These non-sparse and non-concentrated attention patterns result in the high\nsensitivity of Qwen2.5-7B-Instruct to KV cache compression including low-precision quantization and even model weight\nand activation quantization.",
        "title": "第25页-段落110",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1022",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9957656860351562,
        "probabilities": {
          "human": 0.9957656860351562,
          "aigc": 0.004234286490827799
        },
        "text": "25",
        "title": "第25页-段落111",
        "page_number": 25,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1023",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第26页-段落1",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1024",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996479749679565,
        "probabilities": {
          "human": 0.00035201365244574845,
          "aigc": 0.9996479749679565
        },
        "text": "Table 12: Final generation accuracy comparison of different KV cache quantization modes and precisions and Llama-3.1-\n8B-Instruct and Mistral-7B-Instruct-v0.3 on the AIGC and mathematical datasets. KV cache quantization is enabled during\nboth prefilling and decoding stages to amplify the effects of error accumulation.",
        "title": "第26页-段落2",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1025",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9082520008087158,
        "probabilities": {
          "human": 0.9082520008087158,
          "aigc": 0.09174799174070358
        },
        "text": "Quant. method\nPrecision\nCEVAL\nMMLU\nTriviaQA\nRACE\nTruthfulQA\nGSM8K\nAverage\n0-shot\n4-shot\n8-shot\n16-shot\nLlama-3.1-8B-Instruct\nBF16\nBF16\n0.5386\n0.6802\n0.5161\n0.4469\n0.6267\n0.2866\n0.7635\n0.7741\n0.7854\n0.6020",
        "title": "第26页-段落3",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1026",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9847709536552429,
        "probabilities": {
          "human": 0.9847709536552429,
          "aigc": 0.01522900816053152
        },
        "text": "KV8\n0.5416\n0.6798\n0.5162\n0.4469\n0.6304\n0.2752\n0.7597\n0.7657\n0.7809\n0.5996\nK8V4\n0.5394\n0.6792\n0.5138\n0.4498\n0.6450\n0.2858\n0.7695\n0.7794\n0.7923\n0.6060\nK8V2\n0.4807\n0.6381\n0.4989\n0.4383\n0.6499\n0.2358\n0.7074\n0.7036\n0.7195\n0.5636\nK4V8\n0.5327\n0.6694\n0.5144\n0.4488\n0.5851\n0.2623\n0.7566\n0.7566\n0.7710\n0.5885\nKV4\n0.5245\n0.6689\n0.5135\n0.4498\n0.6132\n0.2782\n0.746\n0.7589\n0.7680\n0.5912\nK4V2\n0.4703\n0.6236\n0.5016\n0.4450\n0.5373\n0.2464\n0.6694\n0.6694\n0.6854\n0.5387\nK2V4\n0.3247\n0.4628\n0.4761\n0.3675\n0.4639\n0.0978\n0.1122\n0.1054\n0.0842\n0.2772\nKV2\n0.2771\n0.3600\n0.4584\n0.3301\n0.3182\n0.0508\n0.0432\n0.0318\n0.0250\n0.2105",
        "title": "第26页-段落4",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1027",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第26页-段落5",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1028",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9858501553535461,
        "probabilities": {
          "human": 0.9858501553535461,
          "aigc": 0.014149799011647701
        },
        "text": "KV8\n0.5342\n0.6800\n0.5175\n0.4459\n0.6206\n0.2805\n0.7657\n0.7809\n0.7801\n0.6006\nK8V4\n0.5386\n0.6776\n0.4709\n0.4450\n0.6169\n0.3154\n0.7733\n0.7688\n0.7847\n0.5990\nK8V2\n0.4792\n0.6183\n0.4984\n0.4239\n0.5887\n0.1501\n0.6391\n0.6262\n0.6550\n0.5199\nK4V8\n0.5163\n0.6579\n0.5123\n0.4411\n0.6781\n0.2517\n0.7180\n0.7293\n0.7240\n0.5810\nKV4\n0.5141\n0.6570\n0.4849\n0.4325\n0.6340\n0.2782\n0.7240\n0.7202\n0.7157\n0.5734\nK4V2\n0.4413\n0.5910\n0.4779\n0.4306\n0.5447\n0.1289\n0.5709\n0.5633\n0.5519\n0.4778\nK2V4\n0.2400\n0.2350\n0.0249\n0.2593\n0.3268\n0.0212\n0.0159\n0.0296\n0.0212\n0.1304\nKV2\n0.2444\n0.2338\n0.0052\n0.2478\n0.2277\n0.0227\n0.0174\n0.0197\n0.0273\n0.1162\nMistral-7B-v0.3\nBF16\nBF16\n0.3923\n0.5911\n0.6081\n0.4057\n0.4296\n0.0766\n0.3389\n0.3753\n0.3601\n0.3975",
        "title": "第26页-段落6",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1029",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第26页-段落7",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1030",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.988014280796051,
        "probabilities": {
          "human": 0.988014280796051,
          "aigc": 0.011985727585852146
        },
        "text": "KV8\n0.3945\n0.5901\n0.6072\n0.4115\n0.4259\n0.0735\n0.3412\n0.3639\n0.3624\n0.3967\nK8V4\n0.3945\n0.5909\n0.6068\n0.4067\n0.4394\n0.0781\n0.3457\n0.3723\n0.3669\n0.4001\nK8V2\n0.3819\n0.5776\n0.6042\n0.4086\n0.4370\n0.0675\n0.3404\n0.3518\n0.3609\n0.3922\nK4V8\n0.3990\n0.5875\n0.6069\n0.4048\n0.4308\n0.0697\n0.3442\n0.3563\n0.3738\n0.3970\nKV4\n0.3945\n0.5886\n0.6074\n0.4105\n0.4455\n0.0751\n0.3434\n0.3662\n0.3586\n0.3989\nK4V2\n0.3752\n0.5753\n0.6035\n0.4000\n0.4223\n0.0705\n0.3434\n0.3397\n0.3616\n0.3879\nK2V4\n0.3128\n0.4926\n0.5982\n0.3847\n0.3917\n0.0637\n0.0978\n0.0910\n0.0773\n0.2789\nKV2\n0.2905\n0.4571\n0.5920\n0.3885\n0.4688\n0.0478\n0.0766\n0.0644\n0.0516\n0.2708",
        "title": "第26页-段落8",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1031",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第26页-段落9",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1032",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9839555621147156,
        "probabilities": {
          "human": 0.9839555621147156,
          "aigc": 0.01604444533586502
        },
        "text": "KV8\n0.3900\n0.5892\n0.6071\n0.4067\n0.4284\n0.072\n0.3419\n0.3745\n0.3571\n0.3963\nK8V4\n0.3967\n0.5897\n0.6040\n0.4057\n0.4357\n0.0751\n0.3533\n0.3715\n0.3707\n0.4003\nK8V2\n0.3692\n0.5760\n0.5797\n0.4029\n0.3929\n0.0675\n0.3328\n0.3381\n0.3548\n0.3793\nK4V8\n0.3871\n0.5862\n0.6070\n0.4077\n0.4259\n0.0629\n0.3450\n0.3578\n0.3692\n0.3943\nKV4\n0.3871\n0.5865\n0.5994\n0.4048\n0.4321\n0.072\n0.3450\n0.3556\n0.3685\n0.3946\nK4V2\n0.3618\n0.5672\n0.5774\n0.4086\n0.3623\n0.0599\n0.3048\n0.3389\n0.3571\n0.3709\nK2V4\n0.2786\n0.4360\n0.4688\n0.3914\n0.3268\n0.0303\n0.0334\n0.0281\n0.0212\n0.2238\nKV2\n0.2741\n0.3926\n0.4045\n0.4019\n0.2999\n0.0281\n0.0265\n0.0167\n0.0220\n0.2074",
        "title": "第26页-段落10",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1033",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第26页-段落11",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1034",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992646336555481,
        "probabilities": {
          "human": 0.992646336555481,
          "aigc": 0.00735362246632576
        },
        "text": "26",
        "title": "第26页-段落12",
        "page_number": 26,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1035",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第27页-段落1",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1036",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9997665286064148,
        "probabilities": {
          "human": 0.00023353476717602462,
          "aigc": 0.9997665286064148
        },
        "text": "Table 13: Final generation accuracy comparison of different KV cache quantization modes and precisions and Qwen2.5\nLLMs on the AIGC and mathematical datasets. KV cache quantization is enabled during both prefilling and decoding stages\nto amplify the effects of error accumulation.",
        "title": "第27页-段落2",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1037",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9681202173233032,
        "probabilities": {
          "human": 0.9681202173233032,
          "aigc": 0.03187970444560051
        },
        "text": "Quant. method\nPrecision\nCEVAL\nMMLU\nTriviaQA\nRACE\nTruthfulQA\nGSM8K\nAverage\n0-shot\n4-shot\n8-shot\n16-shot\nQwen2.5-3B-Instruct-AWQ\nBF16\nBF16\n0.7125\n0.6382\n0.2299\n0.3904\n0.4700\n0.4867\n0.5815\n0.6353\n0.6861\n0.5367",
        "title": "第27页-段落3",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1038",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9840294718742371,
        "probabilities": {
          "human": 0.9840294718742371,
          "aigc": 0.015970515087246895
        },
        "text": "KV8\n0.7073\n0.6389\n0.2283\n0.3885\n0.4761\n0.4882\n0.5762\n0.6361\n0.6816\n0.5357\nK8V4\n0.7080\n0.6388\n0.2321\n0.3895\n0.4871\n0.4852\n0.5625\n0.6315\n0.6823\n0.5352\nK8V2\n0.6872\n0.6204\n0.2225\n0.3856\n0.4847\n0.4928\n0.5368\n0.6058\n0.6641\n0.5222\nK4V8\n0.7125\n0.6275\n0.2326\n0.3923\n0.4761\n0.4814\n0.5580\n0.6096\n0.6550\n0.5272\nKV4\n0.7013\n0.6249\n0.2322\n0.4048\n0.4627\n0.4761\n0.5474\n0.6240\n0.6368\n0.5234\nK4V2\n0.6709\n0.6038\n0.2216\n0.3885\n0.4700\n0.4519\n0.5284\n0.5732\n0.6171\n0.5028\nK2V4\n0.3566\n0.3626\n0.1986\n0.2995\n0.4186\n0.0197\n0.0099\n0.0099\n0.0091\n0.1872\nKV2\n0.3507\n0.3203\n0.1983\n0.2727\n0.4308\n0.0136\n0.0144\n0.0144\n0.0136\n0.1810",
        "title": "第27页-段落4",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1039",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第27页-段落5",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1040",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9848290085792542,
        "probabilities": {
          "human": 0.9848290085792542,
          "aigc": 0.015170970000326633
        },
        "text": "KV8\n0.7043\n0.6379\n0.2248\n0.3866\n0.4798\n0.4913\n0.5823\n0.6331\n0.6740\n0.5349\nK8V4\n0.6969\n0.6364\n0.2402\n0.3837\n0.4676\n0.4784\n0.5671\n0.6209\n0.6717\n0.5292\nK8V2\n0.4926\n0.4979\n0.0100\n0.3732\n0.4749\n0.3616\n0.3798\n0.4200\n0.4640\n0.3860\nK4V8\n0.2489\n0.2306\n0.0000\n0.2258\n0.1591\n0.0008\n0\n0\n0.0008\n0.0962\nKV4\n0.2377\n0.2325\n0.0000\n0.2220\n0.1469\n0\n0\n0.0015\n0.0015\n0.0936\nK4V2\n0.2600\n0.2323\n0.0000\n0.2258\n0.0979\n0.0038\n0\n0\n0\n0.0911\nK2V4\n0.2318\n0.2335\n0.0001\n0.2201\n0.1677\n0.0023\n0.0083\n0.0045\n0.0099\n0.0976\nKV2\n0.2489\n0.2372\n0.0000\n0.2249\n0.1310\n0.0023\n0.0053\n0.0106\n0.0061\n0.0963\nQwen2.5-7B-Instruct\nBF16\nBF16\n0.7949\n0.7178\n0.3239\n0.4612\n0.5104\n0.7233\n0.8059\n0.8287\n0.8218\n0.6653",
        "title": "第27页-段落6",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1041",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第27页-段落7",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1042",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.988804280757904,
        "probabilities": {
          "human": 0.988804280757904,
          "aigc": 0.011195770464837551
        },
        "text": "KV8\n0.7949\n0.7174\n0.3235\n0.4603\n0.5092\n0.721\n0.7915\n0.8249\n0.8302\n0.6637\nK8V4\n0.7979\n0.7174\n0.3222\n0.4651\n0.5104\n0.7119\n0.7915\n0.8180\n0.8226\n0.6619\nK8V2\n0.7734\n0.7035\n0.3165\n0.4459\n0.4994\n0.6581\n0.7832\n0.8059\n0.8105\n0.6440\nK4V8\n0.5780\n0.5024\n0.2757\n0.3311\n0.3660\n0.0136\n0.0076\n0.0038\n0.003\n0.2312\nKV4\n0.5802\n0.5028\n0.2761\n0.3206\n0.3758\n0.0182\n0.0068\n0.0038\n0.003\n0.2319\nK4V2\n0.5245\n0.4704\n0.2754\n0.3167\n0.3745\n0.0152\n0.0099\n0.0053\n0.0038\n0.2217\nK2V4\n0.2719\n0.2645\n0.2742\n0.2507\n0.2399\n0.0053\n0.0015\n0.0008\n0.0008\n0.1455\nKV2\n0.2756\n0.2568\n0.2741\n0.2632\n0.2338\n0.0099\n0.0038\n0.0023\n0\n0.1466",
        "title": "第27页-段落8",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1043",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第27页-段落9",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1044",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9876480102539062,
        "probabilities": {
          "human": 0.9876480102539062,
          "aigc": 0.012352030724287033
        },
        "text": "KV8\n0.7883\n0.7119\n0.3192\n0.4593\n0.4957\n0.7149\n0.8044\n0.8052\n0.8203\n0.6577\nK8V4\n0.7920\n0.7117\n0.2978\n0.4545\n0.5018\n0.7111\n0.7847\n0.8044\n0.8067\n0.6516\nK8V2\n0.7169\n0.6757\n0.1127\n0.4488\n0.4957\n0.577\n0.7233\n0.7453\n0.7513\n0.5830\nK4V8\n0.2192\n0.2305\n0.0000\n0.2220\n0.0318\n0\n0\n0\n0\n0.0782\nKV4\n0.2400\n0.2327\n0.0000\n0.2115\n0.0171\n0.0008\n0.0015\n0\n0\n0.0782\nK4V2\n0.2400\n0.2301\n0.0001\n0.2172\n0.0245\n0.0023\n0.0008\n0\n0\n0.0794\nK2V4\n0.2273\n0.2347\n0.0001\n0.2077\n0.0575\n0.0061\n0.0068\n0.0015\n0.0015\n0.0826\nKV2\n0.2489\n0.2376\n0.0000\n0.2230\n0.1346\n0.0045\n0.003\n0.0076\n0.0015\n0.0956\nQwen2.5-Math-7B-Instruct\nBF16\nBF16\n0.4881\n0.5383\n0.0074\n0.3464\n0.4015\n0.4109\n0.8863\n0.8870\n0.8840\n0.5389",
        "title": "第27页-段落10",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1045",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第27页-段落11",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1046",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9787028431892395,
        "probabilities": {
          "human": 0.9787028431892395,
          "aigc": 0.021297108381986618
        },
        "text": "KV8\n0.4844\n0.5379\n0.0072\n0.3397\n0.3966\n0.4041\n0.8878\n0.8878\n0.8772\n0.5359\nK8V4\n0.4874\n0.5361\n0.0071\n0.3445\n0.4002\n0.4102\n0.8886\n0.8870\n0.8840\n0.5383\nK8V2\n0.4606\n0.5291\n0.0071\n0.3426\n0.4162\n0.4139\n0.8779\n0.8802\n0.8696\n0.5330\nK4V8\n0.4428\n0.5061\n0.0073\n0.2660\n0.4100\n0.0834\n0.1501\n0.2024\n0.1259\n0.2438\nKV4\n0.4368\n0.5070\n0.0074\n0.2718\n0.4284\n0.0879\n0.1516\n0.1895\n0.1236\n0.2449\nK4V2\n0.4294\n0.4862\n0.0069\n0.2699\n0.4100\n0.0819\n0.1145\n0.1433\n0.1024\n0.2272\nK2V4\n0.2712\n0.2780\n0.0059\n0.2230\n0.3941\n0.0152\n0.0061\n0.0023\n0.0008\n0.1330\nKV2\n0.2741\n0.2757\n0.0057\n0.2220\n0.3501\n0.0167\n0.0023\n0.003\n0\n0.1277",
        "title": "第27页-段落12",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1047",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990634322166443,
        "probabilities": {
          "human": 0.9990634322166443,
          "aigc": 0.0009365920559503138
        },
        "text": "KIVI",
        "title": "第27页-段落13",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1048",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9831874966621399,
        "probabilities": {
          "human": 0.9831874966621399,
          "aigc": 0.016812527552247047
        },
        "text": "KV8\n0.3975\n0.5905\n0.6064\n0.4038\n0.4308\n0.0728\n0.3457\n0.3685\n0.3571\n0.3970\nK8V4\n0.3878\n0.5891\n0.6035\n0.4010\n0.4443\n0.0735\n0.3450\n0.3616\n0.3632\n0.3966\nK8V2\n0.3522\n0.5590\n0.5452\n0.3971\n0.3452\n0.0462\n0.3116\n0.3397\n0.3359\n0.3591\nK4V8\n0.3804\n0.5822\n0.6016\n0.4010\n0.3831\n0.0667\n0.3252\n0.351\n0.3381\n0.3810\nKV4\n0.3767\n0.5803\n0.5967\n0.4038\n0.3953\n0.0622\n0.3093\n0.3146\n0.3404\n0.3755\nK4V2\n0.3470\n0.5463\n0.5372\n0.3943\n0.4211\n0.0462\n0.2631\n0.2752\n0.2911\n0.3468\nK2V4\n0.2429\n0.2401\n0.0262\n0.2900\n0.2693\n0.0121\n0.0038\n0.0045\n0.0083\n0.1219\nKV2\n0.2363\n0.2351\n0.0110\n0.2766\n0.1787\n0.0121\n0.0061\n0.0091\n0.0091\n0.1082",
        "title": "第27页-段落14",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1049",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995796084403992,
        "probabilities": {
          "human": 0.9995796084403992,
          "aigc": 0.00042040584958158433
        },
        "text": "Per-token-asym",
        "title": "第27页-段落15",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1050",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9920410513877869,
        "probabilities": {
          "human": 0.9920410513877869,
          "aigc": 0.00795889925211668
        },
        "text": "27",
        "title": "第27页-段落16",
        "page_number": 27,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1051",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第28页-段落1",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1052",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996386766433716,
        "probabilities": {
          "human": 0.9996386766433716,
          "aigc": 0.00036133950925432146
        },
        "text": "0.0250",
        "title": "第28页-段落2",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1053",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第28页-段落3",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1054",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第28页-段落4",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1055",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995239973068237,
        "probabilities": {
          "human": 0.9995239973068237,
          "aigc": 0.00047601762344129384
        },
        "text": "0.0225",
        "title": "第28页-段落5",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1056",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第28页-段落6",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1057",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落7",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1058",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落8",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1059",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落9",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1060",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993957281112671,
        "probabilities": {
          "human": 0.9993957281112671,
          "aigc": 0.0006042672321200371
        },
        "text": "0.0200",
        "title": "第28页-段落10",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1061",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第28页-段落11",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1062",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第28页-段落12",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1063",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995777010917664,
        "probabilities": {
          "human": 0.9995777010917664,
          "aigc": 0.00042231963016092777
        },
        "text": "0.0175",
        "title": "第28页-段落13",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1064",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第28页-段落14",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1065",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第28页-段落15",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1066",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997106194496155,
        "probabilities": {
          "human": 0.9997106194496155,
          "aigc": 0.00028935197042301297
        },
        "text": "0.0150",
        "title": "第28页-段落16",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1067",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第28页-段落17",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1068",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996048808097839,
        "probabilities": {
          "human": 0.9996048808097839,
          "aigc": 0.0003951281832996756
        },
        "text": "0.0125",
        "title": "第28页-段落18",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1069",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第28页-段落19",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1070",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第28页-段落20",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1071",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994840621948242,
        "probabilities": {
          "human": 0.9994840621948242,
          "aigc": 0.0005159316351637244
        },
        "text": "0.0100",
        "title": "第28页-段落21",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1072",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第28页-段落22",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1073",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第28页-段落23",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1074",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994761347770691,
        "probabilities": {
          "human": 0.9994761347770691,
          "aigc": 0.0005239242454990745
        },
        "text": "0.0075",
        "title": "第28页-段落24",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1075",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落25",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1076",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落26",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1077",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落27",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1078",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979648590087891,
        "probabilities": {
          "human": 0.9979648590087891,
          "aigc": 0.00203514052554965
        },
        "text": "(a) KV8 eo: 0.014",
        "title": "第28页-段落28",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1079",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978267550468445,
        "probabilities": {
          "human": 0.9978267550468445,
          "aigc": 0.0021732146851718426
        },
        "text": "(b) K8V4 eo: 0.100",
        "title": "第28页-段落29",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1080",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987049102783203,
        "probabilities": {
          "human": 0.9987049102783203,
          "aigc": 0.001295082038268447
        },
        "text": "(c) K8V2 eo: 0.401",
        "title": "第28页-段落30",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1081",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第28页-段落31",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1082",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第28页-段落32",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1083",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第28页-段落33",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1084",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落34",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1085",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落35",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1086",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落36",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1087",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第28页-段落37",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1088",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第28页-段落38",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1089",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第28页-段落39",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1090",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第28页-段落40",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1091",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第28页-段落41",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1092",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第28页-段落42",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1093",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第28页-段落43",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1094",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第28页-段落44",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1095",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第28页-段落45",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1096",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第28页-段落46",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1097",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第28页-段落47",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1098",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第28页-段落48",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1099",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第28页-段落49",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1100",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第28页-段落50",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1101",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落51",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1102",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落52",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1103",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落53",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1104",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983349442481995,
        "probabilities": {
          "human": 0.9983349442481995,
          "aigc": 0.0016650597099214792
        },
        "text": "(d) K4V8 eo: 0.168",
        "title": "第28页-段落54",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1105",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975057244300842,
        "probabilities": {
          "human": 0.9975057244300842,
          "aigc": 0.0024942741729319096
        },
        "text": "(e) KV4 eo: 0.207",
        "title": "第28页-段落55",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1106",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9973577857017517,
        "probabilities": {
          "human": 0.9973577857017517,
          "aigc": 0.002642157720401883
        },
        "text": "(f) K4V2 eo: 0.453",
        "title": "第28页-段落56",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1107",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第28页-段落57",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1108",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979649782180786,
        "probabilities": {
          "human": 0.9979649782180786,
          "aigc": 0.002035070676356554
        },
        "text": "2.00",
        "title": "第28页-段落58",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1109",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979649782180786,
        "probabilities": {
          "human": 0.9979649782180786,
          "aigc": 0.002035070676356554
        },
        "text": "2.00",
        "title": "第28页-段落59",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1110",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976504445075989,
        "probabilities": {
          "human": 0.9976504445075989,
          "aigc": 0.00234958971850574
        },
        "text": "1.8",
        "title": "第28页-段落60",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1111",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落61",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1112",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落62",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1113",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第28页-段落63",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1114",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990814924240112,
        "probabilities": {
          "human": 0.9990814924240112,
          "aigc": 0.000918444711714983
        },
        "text": "1.75",
        "title": "第28页-段落64",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1115",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990814924240112,
        "probabilities": {
          "human": 0.9990814924240112,
          "aigc": 0.000918444711714983
        },
        "text": "1.75",
        "title": "第28页-段落65",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1116",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第28页-段落66",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1117",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993925094604492,
        "probabilities": {
          "human": 0.9993925094604492,
          "aigc": 0.0006075210403650999
        },
        "text": "1.50",
        "title": "第28页-段落67",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1118",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993925094604492,
        "probabilities": {
          "human": 0.9993925094604492,
          "aigc": 0.0006075210403650999
        },
        "text": "1.50",
        "title": "第28页-段落68",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1119",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第28页-段落69",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1120",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999306321144104,
        "probabilities": {
          "human": 0.999306321144104,
          "aigc": 0.0006937168654985726
        },
        "text": "1.25",
        "title": "第28页-段落70",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1121",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999306321144104,
        "probabilities": {
          "human": 0.999306321144104,
          "aigc": 0.0006937168654985726
        },
        "text": "1.25",
        "title": "第28页-段落71",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1122",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第28页-段落72",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1123",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980506896972656,
        "probabilities": {
          "human": 0.9980506896972656,
          "aigc": 0.0019493576837703586
        },
        "text": "1.00",
        "title": "第28页-段落73",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1124",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980506896972656,
        "probabilities": {
          "human": 0.9980506896972656,
          "aigc": 0.0019493576837703586
        },
        "text": "1.00",
        "title": "第28页-段落74",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1125",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第28页-段落75",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1126",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981498718261719,
        "probabilities": {
          "human": 0.9981498718261719,
          "aigc": 0.0018501300364732742
        },
        "text": "0.75",
        "title": "第28页-段落76",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1127",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981498718261719,
        "probabilities": {
          "human": 0.9981498718261719,
          "aigc": 0.0018501300364732742
        },
        "text": "0.75",
        "title": "第28页-段落77",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1128",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第28页-段落78",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1129",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第28页-段落79",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1130",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第28页-段落80",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1131",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第28页-段落81",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1132",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第28页-段落82",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1133",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第28页-段落83",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1134",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落84",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1135",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落85",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1136",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第28页-段落86",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1137",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986704587936401,
        "probabilities": {
          "human": 0.9986704587936401,
          "aigc": 0.0013295402750372887
        },
        "text": "(g) K2V8 eo: 0.882",
        "title": "第28页-段落87",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1138",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992603659629822,
        "probabilities": {
          "human": 0.9992603659629822,
          "aigc": 0.0007396223372779787
        },
        "text": "(h) K2V4 eo: 0.892",
        "title": "第28页-段落88",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1139",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983207583427429,
        "probabilities": {
          "human": 0.9983207583427429,
          "aigc": 0.00167921744287014
        },
        "text": "(i) KV2 eo: 0.962",
        "title": "第28页-段落89",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1140",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994577765464783,
        "probabilities": {
          "human": 0.0005421846872195601,
          "aigc": 0.9994577765464783
        },
        "text": "Figure 13: Layer-wise relative attention output error eo of per-token-asym KV cache quantization with simulated offline\nquantization and dequantization (without error accumulation) of the Llama-3.1-8B-Instruct model and the first 20 prompts\nin the 0-shot GSM8K dataset. When the key quantization precision decreases to 2-bit, the layer-wise relative attention\noutput error distribution significantly shifts. Especially, the errors of layer-3 and layer-1 are significantly larger than other\nlayers.",
        "title": "第28页-段落90",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1141",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9823302030563354,
        "probabilities": {
          "human": 0.01766982302069664,
          "aigc": 0.9823302030563354
        },
        "text": "F. Layer-wise Attention Score and Relative Output Error",
        "title": "第28页-段落91",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1142",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995850920677185,
        "probabilities": {
          "human": 0.0004149416054133326,
          "aigc": 0.9995850920677185
        },
        "text": "In this section, we visualize more layer-wise attention errors with KV cache quantization covering different LLMs, datasets,\nand KV cache quantization mode and precision. We select the first 20 prompts from the mathematical reasoning dataset\nGSM8K (Cobbe et al., 2021) and the AIGC multi-turn conversation dataset multiturn-softage (SoftAge-AI, 2024). Tested\nLLMs include Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct, and Mistral-7B-Instruct-v0.3. The layer-wise sensitivity to KV\ncache quantization of different LLMs are consistent to different prompts and datasets. Key cache quantization generally\nleads to the layer-wiser attention output error distribution shift. When the layer-wise attention error distribution significantly\nchanges, the final model accuracy also dramatically degrades. For example, the perplexity and final generation accuracy of\nQwen2.5-7B-Instruct dramatically degrades when the key quantization precision decreases to 4-bit and 2-bit with the KIVI\nor per-token-asym quantization mode as demonstrated in Table 2, 5, and 6. The attention distribution of it also significantly\nshifts as shown in Figure 16, 17, and 18. The most",
        "title": "第28页-段落92",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1143",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993120431900024,
        "probabilities": {
          "human": 0.0006880104774609208,
          "aigc": 0.9993120431900024
        },
        "text": "As visualized in Figure 12, most layers of Qwen2.5-7B-Instruct have a high ratio of non-sparse retrieval heads, which are\nsensitive to low-precision key cache quantization as analyzed in Section 4.4. As a result, 4-bit or 2-bit key quantization\nleads to noticeable errors of attention score and critical KV identification in these layers with medium attention errors such\nas layer-1, 12, and 21.",
        "title": "第28页-段落93",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1144",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955418705940247,
        "probabilities": {
          "human": 0.9955418705940247,
          "aigc": 0.004458144772797823
        },
        "text": "28",
        "title": "第28页-段落94",
        "page_number": 28,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1145",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第29页-段落1",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1146",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9172338247299194,
        "probabilities": {
          "human": 0.9172338247299194,
          "aigc": 0.08276616781949997
        },
        "text": "1e\n5",
        "title": "第29页-段落2",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1147",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999840259552002,
        "probabilities": {
          "human": 0.999840259552002,
          "aigc": 0.00015970940876286477
        },
        "text": "0.000225",
        "title": "第29页-段落3",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1148",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995049238204956,
        "probabilities": {
          "human": 0.9995049238204956,
          "aigc": 0.0004950642469339073
        },
        "text": "0.0008",
        "title": "第29页-段落4",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1149",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第29页-段落5",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1150",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998229146003723,
        "probabilities": {
          "human": 0.9998229146003723,
          "aigc": 0.00017709888925310224
        },
        "text": "0.000200",
        "title": "第29页-段落6",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1151",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991782307624817,
        "probabilities": {
          "human": 0.9991782307624817,
          "aigc": 0.0008217679569497705
        },
        "text": "0.0007",
        "title": "第29页-段落7",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1152",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998437166213989,
        "probabilities": {
          "human": 0.9998437166213989,
          "aigc": 0.0001562075485708192
        },
        "text": "0.000175",
        "title": "第29页-段落8",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1153",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第29页-段落9",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1154",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第29页-段落10",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1155",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第29页-段落11",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1156",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第29页-段落12",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1157",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998910427093506,
        "probabilities": {
          "human": 0.9998910427093506,
          "aigc": 0.00010899156040977687
        },
        "text": "0.000150",
        "title": "第29页-段落13",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1158",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992005228996277,
        "probabilities": {
          "human": 0.9992005228996277,
          "aigc": 0.0007995329797267914
        },
        "text": "0.0006",
        "title": "第29页-段落14",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1159",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第29页-段落15",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1160",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998809099197388,
        "probabilities": {
          "human": 0.9998809099197388,
          "aigc": 0.00011907103180419654
        },
        "text": "0.000125",
        "title": "第29页-段落16",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1161",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995079040527344,
        "probabilities": {
          "human": 0.9995079040527344,
          "aigc": 0.0004921150975860655
        },
        "text": "0.0005",
        "title": "第29页-段落17",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1162",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第29页-段落18",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1163",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998341798782349,
        "probabilities": {
          "human": 0.9998341798782349,
          "aigc": 0.0001657559332670644
        },
        "text": "0.000100",
        "title": "第29页-段落19",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1164",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995656609535217,
        "probabilities": {
          "human": 0.9995656609535217,
          "aigc": 0.0004343086911831051
        },
        "text": "0.0004",
        "title": "第29页-段落20",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1165",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第29页-段落21",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1166",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997759461402893,
        "probabilities": {
          "human": 0.9997759461402893,
          "aigc": 0.00022404265473596752
        },
        "text": "0.000075",
        "title": "第29页-段落22",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1167",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994980096817017,
        "probabilities": {
          "human": 0.9994980096817017,
          "aigc": 0.0005019403761252761
        },
        "text": "0.0003",
        "title": "第29页-段落23",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1168",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第29页-段落24",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1169",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998210072517395,
        "probabilities": {
          "human": 0.9998210072517395,
          "aigc": 0.00017903394473250955
        },
        "text": "0.000050",
        "title": "第29页-段落25",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1170",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996066689491272,
        "probabilities": {
          "human": 0.9996066689491272,
          "aigc": 0.0003933655098080635
        },
        "text": "0.0002",
        "title": "第29页-段落26",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1171",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第29页-段落27",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1172",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998383522033691,
        "probabilities": {
          "human": 0.9998383522033691,
          "aigc": 0.00016165118722710758
        },
        "text": "0.000025",
        "title": "第29页-段落28",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1173",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落29",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1174",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落30",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1175",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落31",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1176",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.974494457244873,
        "probabilities": {
          "human": 0.974494457244873,
          "aigc": 0.025505561381578445
        },
        "text": "(a) K8 ea: 5.0 × 10−6",
        "title": "第29页-段落32",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1177",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.970710039138794,
        "probabilities": {
          "human": 0.970710039138794,
          "aigc": 0.02928994596004486
        },
        "text": "(b) K4 ea: 6.7 × 10−5",
        "title": "第29页-段落33",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1178",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9873560667037964,
        "probabilities": {
          "human": 0.9873560667037964,
          "aigc": 0.012643907219171524
        },
        "text": "(c) K2 ea: 3.26 × 10−4",
        "title": "第29页-段落34",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1179",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第29页-段落35",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1180",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第29页-段落36",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1181",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996386766433716,
        "probabilities": {
          "human": 0.9996386766433716,
          "aigc": 0.00036133950925432146
        },
        "text": "0.0250",
        "title": "第29页-段落37",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1182",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第29页-段落38",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1183",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落39",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1184",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落40",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1185",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落41",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1186",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第29页-段落42",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1187",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995239973068237,
        "probabilities": {
          "human": 0.9995239973068237,
          "aigc": 0.00047601762344129384
        },
        "text": "0.0225",
        "title": "第29页-段落43",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1188",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第29页-段落44",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1189",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第29页-段落45",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1190",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993957281112671,
        "probabilities": {
          "human": 0.9993957281112671,
          "aigc": 0.0006042672321200371
        },
        "text": "0.0200",
        "title": "第29页-段落46",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1191",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第29页-段落47",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1192",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第29页-段落48",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1193",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995777010917664,
        "probabilities": {
          "human": 0.9995777010917664,
          "aigc": 0.00042231963016092777
        },
        "text": "0.0175",
        "title": "第29页-段落49",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1194",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第29页-段落50",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1195",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第29页-段落51",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1196",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997106194496155,
        "probabilities": {
          "human": 0.9997106194496155,
          "aigc": 0.00028935197042301297
        },
        "text": "0.0150",
        "title": "第29页-段落52",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1197",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第29页-段落53",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1198",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第29页-段落54",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1199",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996048808097839,
        "probabilities": {
          "human": 0.9996048808097839,
          "aigc": 0.0003951281832996756
        },
        "text": "0.0125",
        "title": "第29页-段落55",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1200",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第29页-段落56",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1201",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994840621948242,
        "probabilities": {
          "human": 0.9994840621948242,
          "aigc": 0.0005159316351637244
        },
        "text": "0.0100",
        "title": "第29页-段落57",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1202",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第29页-段落58",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1203",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第29页-段落59",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1204",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落60",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1205",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落61",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1206",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落62",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1207",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9967407584190369,
        "probabilities": {
          "human": 0.9967407584190369,
          "aigc": 0.003259270917624235
        },
        "text": "(d) KV8 eo: 0.017",
        "title": "第29页-段落63",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1208",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984521865844727,
        "probabilities": {
          "human": 0.9984521865844727,
          "aigc": 0.0015477407723665237
        },
        "text": "(e) K8V4 eo: 0.110",
        "title": "第29页-段落64",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1209",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981374740600586,
        "probabilities": {
          "human": 0.9981374740600586,
          "aigc": 0.0018624885706230998
        },
        "text": "(f) K8V2 eo: 0.418",
        "title": "第29页-段落65",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1210",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980891346931458,
        "probabilities": {
          "human": 0.9980891346931458,
          "aigc": 0.0019108442356809974
        },
        "text": "0.70",
        "title": "第29页-段落66",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1211",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第29页-段落67",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1212",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第29页-段落68",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1213",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第29页-段落69",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1214",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第29页-段落70",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1215",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落71",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1216",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落72",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1217",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落73",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1218",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第29页-段落74",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1219",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第29页-段落75",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1220",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第29页-段落76",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1221",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第29页-段落77",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1222",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第29页-段落78",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1223",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第29页-段落79",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1224",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第29页-段落80",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1225",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第29页-段落81",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1226",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第29页-段落82",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1227",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第29页-段落83",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1228",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第29页-段落84",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1229",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第29页-段落85",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1230",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第29页-段落86",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1231",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第29页-段落87",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1232",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第29页-段落88",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1233",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第29页-段落89",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1234",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落90",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1235",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落91",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1236",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落92",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1237",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999150276184082,
        "probabilities": {
          "human": 0.999150276184082,
          "aigc": 0.0008497110684402287
        },
        "text": "(g) K4V8 eo: 0.199",
        "title": "第29页-段落93",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1238",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987607002258301,
        "probabilities": {
          "human": 0.9987607002258301,
          "aigc": 0.0012392888311296701
        },
        "text": "(h) KV4 eo: 0.240",
        "title": "第29页-段落94",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1239",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.998828113079071,
        "probabilities": {
          "human": 0.998828113079071,
          "aigc": 0.0011718499008566141
        },
        "text": "(i) K4V2 eo: 0.484",
        "title": "第29页-段落95",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1240",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991512298583984,
        "probabilities": {
          "human": 0.9991512298583984,
          "aigc": 0.0008487764280289412
        },
        "text": "2.50",
        "title": "第29页-段落96",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1241",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991512298583984,
        "probabilities": {
          "human": 0.9991512298583984,
          "aigc": 0.0008487764280289412
        },
        "text": "2.50",
        "title": "第29页-段落97",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1242",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995267927646637,
        "probabilities": {
          "human": 0.995267927646637,
          "aigc": 0.004732014611363411
        },
        "text": "2.2",
        "title": "第29页-段落98",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1243",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987431168556213,
        "probabilities": {
          "human": 0.9987431168556213,
          "aigc": 0.0012568652164191008
        },
        "text": "2.25",
        "title": "第29页-段落99",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1244",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987431168556213,
        "probabilities": {
          "human": 0.9987431168556213,
          "aigc": 0.0012568652164191008
        },
        "text": "2.25",
        "title": "第29页-段落100",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1245",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第29页-段落101",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1246",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落102",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1247",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落103",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1248",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第29页-段落104",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1249",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979649782180786,
        "probabilities": {
          "human": 0.9979649782180786,
          "aigc": 0.002035070676356554
        },
        "text": "2.00",
        "title": "第29页-段落105",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1250",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979649782180786,
        "probabilities": {
          "human": 0.9979649782180786,
          "aigc": 0.002035070676356554
        },
        "text": "2.00",
        "title": "第29页-段落106",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1251",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976504445075989,
        "probabilities": {
          "human": 0.9976504445075989,
          "aigc": 0.00234958971850574
        },
        "text": "1.8",
        "title": "第29页-段落107",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1252",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990814924240112,
        "probabilities": {
          "human": 0.9990814924240112,
          "aigc": 0.000918444711714983
        },
        "text": "1.75",
        "title": "第29页-段落108",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1253",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990814924240112,
        "probabilities": {
          "human": 0.9990814924240112,
          "aigc": 0.000918444711714983
        },
        "text": "1.75",
        "title": "第29页-段落109",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1254",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第29页-段落110",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1255",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993925094604492,
        "probabilities": {
          "human": 0.9993925094604492,
          "aigc": 0.0006075210403650999
        },
        "text": "1.50",
        "title": "第29页-段落111",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1256",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第29页-段落112",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1257",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993925094604492,
        "probabilities": {
          "human": 0.9993925094604492,
          "aigc": 0.0006075210403650999
        },
        "text": "1.50",
        "title": "第29页-段落113",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1258",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999306321144104,
        "probabilities": {
          "human": 0.999306321144104,
          "aigc": 0.0006937168654985726
        },
        "text": "1.25",
        "title": "第29页-段落114",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1259",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第29页-段落115",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1260",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999306321144104,
        "probabilities": {
          "human": 0.999306321144104,
          "aigc": 0.0006937168654985726
        },
        "text": "1.25",
        "title": "第29页-段落116",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1261",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980506896972656,
        "probabilities": {
          "human": 0.9980506896972656,
          "aigc": 0.0019493576837703586
        },
        "text": "1.00",
        "title": "第29页-段落117",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1262",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第29页-段落118",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1263",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980506896972656,
        "probabilities": {
          "human": 0.9980506896972656,
          "aigc": 0.0019493576837703586
        },
        "text": "1.00",
        "title": "第29页-段落119",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1264",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第29页-段落120",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1265",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981498718261719,
        "probabilities": {
          "human": 0.9981498718261719,
          "aigc": 0.0018501300364732742
        },
        "text": "0.75",
        "title": "第29页-段落121",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1266",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981498718261719,
        "probabilities": {
          "human": 0.9981498718261719,
          "aigc": 0.0018501300364732742
        },
        "text": "0.75",
        "title": "第29页-段落122",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1267",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落123",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1268",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落124",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1269",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第29页-段落125",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1270",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992485642433167,
        "probabilities": {
          "human": 0.9992485642433167,
          "aigc": 0.0007514596218243241
        },
        "text": "(j) K2V8 eo: 1.092",
        "title": "第29页-段落126",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1271",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991965889930725,
        "probabilities": {
          "human": 0.9991965889930725,
          "aigc": 0.0008033958147279918
        },
        "text": "(k) K2V4 eo: 1.103",
        "title": "第29页-段落127",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1272",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990984201431274,
        "probabilities": {
          "human": 0.9990984201431274,
          "aigc": 0.0009016323601827025
        },
        "text": "(l) K2V2 eo: 1.148",
        "title": "第29页-段落128",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1273",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9995368719100952,
        "probabilities": {
          "human": 0.0004632087948266417,
          "aigc": 0.9995368719100952
        },
        "text": "Figure 14: Layer-wise attention score errors ea and relative attention output error eo of per-token-asym KV cache\nquantization with simulated offline quantization and dequantization (without error accumulation) of the Llama-3.1-8B-\nInstruct model and the first 20 prompts in the AIGC multiturn softage dataset. When the key quantization precision\ndecreases to 2-bit, the layer-wise relative attention output error distribution significantly shifts. Especially, the errors of\nlayer-3, layer-1, and layer-27 are significantly larger than other layers.",
        "title": "第29页-段落129",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1274",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9966631531715393,
        "probabilities": {
          "human": 0.9966631531715393,
          "aigc": 0.0033368612639606
        },
        "text": "29",
        "title": "第29页-段落130",
        "page_number": 29,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1275",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第30页-段落1",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1276",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9172338247299194,
        "probabilities": {
          "human": 0.9172338247299194,
          "aigc": 0.08276616781949997
        },
        "text": "1e\n5",
        "title": "第30页-段落2",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1277",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998113512992859,
        "probabilities": {
          "human": 0.9998113512992859,
          "aigc": 0.00018868966435547918
        },
        "text": "0.00014",
        "title": "第30页-段落3",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1278",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991782307624817,
        "probabilities": {
          "human": 0.9991782307624817,
          "aigc": 0.0008217679569497705
        },
        "text": "0.0007",
        "title": "第30页-段落4",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1279",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第30页-段落5",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1280",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999826967716217,
        "probabilities": {
          "human": 0.999826967716217,
          "aigc": 0.0001730725052766502
        },
        "text": "0.00012",
        "title": "第30页-段落6",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1281",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992005228996277,
        "probabilities": {
          "human": 0.9992005228996277,
          "aigc": 0.0007995329797267914
        },
        "text": "0.0006",
        "title": "第30页-段落7",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1282",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第30页-段落8",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1283",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第30页-段落9",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1284",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第30页-段落10",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1285",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997902512550354,
        "probabilities": {
          "human": 0.9997902512550354,
          "aigc": 0.00020982028217986226
        },
        "text": "0.00010",
        "title": "第30页-段落11",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1286",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第30页-段落12",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1287",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995079040527344,
        "probabilities": {
          "human": 0.9995079040527344,
          "aigc": 0.0004921150975860655
        },
        "text": "0.0005",
        "title": "第30页-段落13",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1288",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996917247772217,
        "probabilities": {
          "human": 0.9996917247772217,
          "aigc": 0.0003082668990828097
        },
        "text": "0.00008",
        "title": "第30页-段落14",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1289",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995656609535217,
        "probabilities": {
          "human": 0.9995656609535217,
          "aigc": 0.0004343086911831051
        },
        "text": "0.0004",
        "title": "第30页-段落15",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1290",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第30页-段落16",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1291",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995431900024414,
        "probabilities": {
          "human": 0.9995431900024414,
          "aigc": 0.00045683298958465457
        },
        "text": "0.00006",
        "title": "第30页-段落17",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1292",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994980096817017,
        "probabilities": {
          "human": 0.9994980096817017,
          "aigc": 0.0005019403761252761
        },
        "text": "0.0003",
        "title": "第30页-段落18",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1293",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第30页-段落19",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1294",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99972003698349,
        "probabilities": {
          "human": 0.99972003698349,
          "aigc": 0.00027998187579214573
        },
        "text": "0.00004",
        "title": "第30页-段落20",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1295",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996066689491272,
        "probabilities": {
          "human": 0.9996066689491272,
          "aigc": 0.0003933655098080635
        },
        "text": "0.0002",
        "title": "第30页-段落21",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1296",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第30页-段落22",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1297",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997484087944031,
        "probabilities": {
          "human": 0.9997484087944031,
          "aigc": 0.00025155252660624683
        },
        "text": "0.00002",
        "title": "第30页-段落23",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1298",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996529817581177,
        "probabilities": {
          "human": 0.9996529817581177,
          "aigc": 0.00034700107062235475
        },
        "text": "0.0001",
        "title": "第30页-段落24",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1299",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落25",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1300",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落26",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1301",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落27",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1302",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9756382703781128,
        "probabilities": {
          "human": 0.9756382703781128,
          "aigc": 0.02436169981956482
        },
        "text": "(a) K8 ea: 4.0 × 10−6",
        "title": "第30页-段落28",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1303",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.970710039138794,
        "probabilities": {
          "human": 0.970710039138794,
          "aigc": 0.02928994596004486
        },
        "text": "(b) K4 ea: 6.7 × 10−5",
        "title": "第30页-段落29",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1304",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9873560667037964,
        "probabilities": {
          "human": 0.9873560667037964,
          "aigc": 0.012643907219171524
        },
        "text": "(c) K2 ea: 3.26 × 10−4",
        "title": "第30页-段落30",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1305",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第30页-段落31",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1306",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第30页-段落32",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1307",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989742040634155,
        "probabilities": {
          "human": 0.9989742040634155,
          "aigc": 0.0010258157271891832
        },
        "text": "0.020",
        "title": "第30页-段落33",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1308",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第30页-段落34",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1309",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落35",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1310",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落36",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1311",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落37",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1312",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第30页-段落38",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1313",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992164373397827,
        "probabilities": {
          "human": 0.9992164373397827,
          "aigc": 0.00078356615267694
        },
        "text": "0.018",
        "title": "第30页-段落39",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1314",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第30页-段落40",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1315",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第30页-段落41",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1316",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第30页-段落42",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1317",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987271428108215,
        "probabilities": {
          "human": 0.9987271428108215,
          "aigc": 0.0012728179572150111
        },
        "text": "0.016",
        "title": "第30页-段落43",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1318",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第30页-段落44",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1319",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第30页-段落45",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1320",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993630051612854,
        "probabilities": {
          "human": 0.9993630051612854,
          "aigc": 0.0006369950715452433
        },
        "text": "0.014",
        "title": "第30页-段落46",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1321",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第30页-段落47",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1322",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第30页-段落48",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1323",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993888139724731,
        "probabilities": {
          "human": 0.9993888139724731,
          "aigc": 0.0006111774710007012
        },
        "text": "0.012",
        "title": "第30页-段落49",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1324",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第30页-段落50",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1325",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第30页-段落51",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1326",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991521835327148,
        "probabilities": {
          "human": 0.9991521835327148,
          "aigc": 0.0008478129166178405
        },
        "text": "0.010",
        "title": "第30页-段落52",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1327",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第30页-段落53",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1328",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第30页-段落54",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1329",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落55",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1330",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落56",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1331",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落57",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1332",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9964345693588257,
        "probabilities": {
          "human": 0.9964345693588257,
          "aigc": 0.0035654078237712383
        },
        "text": "(d) KV8 eo: 0.008",
        "title": "第30页-段落58",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1333",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984521865844727,
        "probabilities": {
          "human": 0.9984521865844727,
          "aigc": 0.0015477407723665237
        },
        "text": "(e) K8V4 eo: 0.110",
        "title": "第30页-段落59",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1334",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981374740600586,
        "probabilities": {
          "human": 0.9981374740600586,
          "aigc": 0.0018624885706230998
        },
        "text": "(f) K8V2 eo: 0.418",
        "title": "第30页-段落60",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1335",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第30页-段落61",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1336",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991347193717957,
        "probabilities": {
          "human": 0.9991347193717957,
          "aigc": 0.0008652835967950523
        },
        "text": "0.300",
        "title": "第30页-段落62",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1337",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985718727111816,
        "probabilities": {
          "human": 0.9985718727111816,
          "aigc": 0.001428139046765864
        },
        "text": "0.22",
        "title": "第30页-段落63",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1338",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第30页-段落64",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1339",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992924928665161,
        "probabilities": {
          "human": 0.9992924928665161,
          "aigc": 0.0007074420573189855
        },
        "text": "0.275",
        "title": "第30页-段落65",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1340",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第30页-段落66",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1341",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落67",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1342",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落68",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1343",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落69",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1344",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第30页-段落70",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1345",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第30页-段落71",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1346",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996182918548584,
        "probabilities": {
          "human": 0.9996182918548584,
          "aigc": 0.0003816639364231378
        },
        "text": "0.250",
        "title": "第30页-段落72",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1347",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第30页-段落73",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1348",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第30页-段落74",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1349",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994695782661438,
        "probabilities": {
          "human": 0.9994695782661438,
          "aigc": 0.0005304827354848385
        },
        "text": "0.225",
        "title": "第30页-段落75",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1350",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第30页-段落76",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1351",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第30页-段落77",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1352",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999346911907196,
        "probabilities": {
          "human": 0.999346911907196,
          "aigc": 0.0006531361141242087
        },
        "text": "0.200",
        "title": "第30页-段落78",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1353",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第30页-段落79",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1354",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第30页-段落80",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1355",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994631409645081,
        "probabilities": {
          "human": 0.9994631409645081,
          "aigc": 0.0005368837155401707
        },
        "text": "0.175",
        "title": "第30页-段落81",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1356",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第30页-段落82",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1357",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第30页-段落83",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1358",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996342658996582,
        "probabilities": {
          "human": 0.9996342658996582,
          "aigc": 0.0003657276974990964
        },
        "text": "0.150",
        "title": "第30页-段落84",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1359",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第30页-段落85",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1360",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第30页-段落86",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1361",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995495676994324,
        "probabilities": {
          "human": 0.9995495676994324,
          "aigc": 0.00045040101394988596
        },
        "text": "0.125",
        "title": "第30页-段落87",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1362",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第30页-段落88",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1363",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落89",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1364",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落90",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1365",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落91",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1366",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985645413398743,
        "probabilities": {
          "human": 0.9985645413398743,
          "aigc": 0.001435537007637322
        },
        "text": "(g) K4V8 eo: 0.138",
        "title": "第30页-段落92",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1367",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985985159873962,
        "probabilities": {
          "human": 0.9985985159873962,
          "aigc": 0.001401450950652361
        },
        "text": "(h) KV4 eo: 0.187",
        "title": "第30页-段落93",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1368",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.998828113079071,
        "probabilities": {
          "human": 0.998828113079071,
          "aigc": 0.0011718499008566141
        },
        "text": "(i) K4V2 eo: 0.484",
        "title": "第30页-段落94",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1369",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9952840209007263,
        "probabilities": {
          "human": 0.9952840209007263,
          "aigc": 0.004716022871434689
        },
        "text": "3.5",
        "title": "第30页-段落95",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1370",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9952840209007263,
        "probabilities": {
          "human": 0.9952840209007263,
          "aigc": 0.004716022871434689
        },
        "text": "3.5",
        "title": "第30页-段落96",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1371",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898854494094849,
        "probabilities": {
          "human": 0.9898854494094849,
          "aigc": 0.010114525444805622
        },
        "text": "3.0",
        "title": "第30页-段落97",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1372",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898854494094849,
        "probabilities": {
          "human": 0.9898854494094849,
          "aigc": 0.010114525444805622
        },
        "text": "3.0",
        "title": "第30页-段落98",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1373",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898854494094849,
        "probabilities": {
          "human": 0.9898854494094849,
          "aigc": 0.010114525444805622
        },
        "text": "3.0",
        "title": "第30页-段落99",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1374",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落100",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1375",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落101",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1376",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第30页-段落102",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1377",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第30页-段落103",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1378",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第30页-段落104",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1379",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第30页-段落105",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1380",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第30页-段落106",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1381",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第30页-段落107",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1382",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第30页-段落108",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1383",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第30页-段落109",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1384",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第30页-段落110",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1385",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第30页-段落111",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1386",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第30页-段落112",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1387",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第30页-段落113",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1388",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第30页-段落114",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1389",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第30页-段落115",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1390",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第30页-段落116",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1391",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第30页-段落117",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1392",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落118",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1393",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落119",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1394",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第30页-段落120",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1395",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992485642433167,
        "probabilities": {
          "human": 0.9992485642433167,
          "aigc": 0.0007514596218243241
        },
        "text": "(j) K2V8 eo: 1.092",
        "title": "第30页-段落121",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1396",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991965889930725,
        "probabilities": {
          "human": 0.9991965889930725,
          "aigc": 0.0008033958147279918
        },
        "text": "(k) K2V4 eo: 1.103",
        "title": "第30页-段落122",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1397",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990984201431274,
        "probabilities": {
          "human": 0.9990984201431274,
          "aigc": 0.0009016323601827025
        },
        "text": "(l) K2V2 eo: 1.148",
        "title": "第30页-段落123",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1398",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994206428527832,
        "probabilities": {
          "human": 0.000579367857426405,
          "aigc": 0.9994206428527832
        },
        "text": "Figure 15: Layer-wise attention score errors ea and relative attention output error eo of key per-channel-asym and value\nper-token-asym quantization with simulated offline quantization and dequantization (without error accumulation) of the\nLlama-3.1-8B-Instruct model and the first 20 prompts in the AIGC multiturn softage dataset. When the key quantization\nprecision decreases to 2-bit, the layer-wise relative attention output error distribution significantly shifts. Especially, the\nerrors of layer-2 and 27 are significantly larger than other layers.",
        "title": "第30页-段落124",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1399",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9936368465423584,
        "probabilities": {
          "human": 0.9936368465423584,
          "aigc": 0.006363114807754755
        },
        "text": "30",
        "title": "第30页-段落125",
        "page_number": 30,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1400",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第31页-段落1",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1401",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995730519294739,
        "probabilities": {
          "human": 0.9995730519294739,
          "aigc": 0.00042693447903729975
        },
        "text": "0.0035",
        "title": "第31页-段落2",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1402",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995777010917664,
        "probabilities": {
          "human": 0.9995777010917664,
          "aigc": 0.00042231963016092777
        },
        "text": "0.0175",
        "title": "第31页-段落3",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1403",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995777010917664,
        "probabilities": {
          "human": 0.9995777010917664,
          "aigc": 0.00042231963016092777
        },
        "text": "0.0175",
        "title": "第31页-段落4",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1404",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995471835136414,
        "probabilities": {
          "human": 0.9995471835136414,
          "aigc": 0.00045278671314008534
        },
        "text": "0.0030",
        "title": "第31页-段落5",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1405",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997106194496155,
        "probabilities": {
          "human": 0.9997106194496155,
          "aigc": 0.00028935197042301297
        },
        "text": "0.0150",
        "title": "第31页-段落6",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1406",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997106194496155,
        "probabilities": {
          "human": 0.9997106194496155,
          "aigc": 0.00028935197042301297
        },
        "text": "0.0150",
        "title": "第31页-段落7",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1407",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995228052139282,
        "probabilities": {
          "human": 0.9995228052139282,
          "aigc": 0.0004772258980665356
        },
        "text": "0.0025",
        "title": "第31页-段落8",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1408",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第31页-段落9",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1409",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第31页-段落10",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1410",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第31页-段落11",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1411",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996048808097839,
        "probabilities": {
          "human": 0.9996048808097839,
          "aigc": 0.0003951281832996756
        },
        "text": "0.0125",
        "title": "第31页-段落12",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1412",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996048808097839,
        "probabilities": {
          "human": 0.9996048808097839,
          "aigc": 0.0003951281832996756
        },
        "text": "0.0125",
        "title": "第31页-段落13",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1413",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995154142379761,
        "probabilities": {
          "human": 0.9995154142379761,
          "aigc": 0.0004845462099183351
        },
        "text": "0.0020",
        "title": "第31页-段落14",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1414",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994840621948242,
        "probabilities": {
          "human": 0.9994840621948242,
          "aigc": 0.0005159316351637244
        },
        "text": "0.0100",
        "title": "第31页-段落15",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1415",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994840621948242,
        "probabilities": {
          "human": 0.9994840621948242,
          "aigc": 0.0005159316351637244
        },
        "text": "0.0100",
        "title": "第31页-段落16",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1416",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996101260185242,
        "probabilities": {
          "human": 0.9996101260185242,
          "aigc": 0.000389878056012094
        },
        "text": "0.0015",
        "title": "第31页-段落17",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1417",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994761347770691,
        "probabilities": {
          "human": 0.9994761347770691,
          "aigc": 0.0005239242454990745
        },
        "text": "0.0075",
        "title": "第31页-段落18",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1418",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994761347770691,
        "probabilities": {
          "human": 0.9994761347770691,
          "aigc": 0.0005239242454990745
        },
        "text": "0.0075",
        "title": "第31页-段落19",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1419",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996285438537598,
        "probabilities": {
          "human": 0.9996285438537598,
          "aigc": 0.00037139817140996456
        },
        "text": "0.0010",
        "title": "第31页-段落20",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1420",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996929168701172,
        "probabilities": {
          "human": 0.9996929168701172,
          "aigc": 0.0003071600804105401
        },
        "text": "0.0050",
        "title": "第31页-段落21",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1421",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996929168701172,
        "probabilities": {
          "human": 0.9996929168701172,
          "aigc": 0.0003071600804105401
        },
        "text": "0.0050",
        "title": "第31页-段落22",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1422",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995079040527344,
        "probabilities": {
          "human": 0.9995079040527344,
          "aigc": 0.0004921150975860655
        },
        "text": "0.0005",
        "title": "第31页-段落23",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1423",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995228052139282,
        "probabilities": {
          "human": 0.9995228052139282,
          "aigc": 0.0004772258980665356
        },
        "text": "0.0025",
        "title": "第31页-段落24",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1424",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995228052139282,
        "probabilities": {
          "human": 0.9995228052139282,
          "aigc": 0.0004772258980665356
        },
        "text": "0.0025",
        "title": "第31页-段落25",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1425",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993269443511963,
        "probabilities": {
          "human": 0.9993269443511963,
          "aigc": 0.0006731341127306223
        },
        "text": "0.0000",
        "title": "第31页-段落26",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1426",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993269443511963,
        "probabilities": {
          "human": 0.9993269443511963,
          "aigc": 0.0006731341127306223
        },
        "text": "0.0000",
        "title": "第31页-段落27",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1427",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落28",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1428",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落29",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1429",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落30",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1430",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9885401129722595,
        "probabilities": {
          "human": 0.9885401129722595,
          "aigc": 0.01145986933261156
        },
        "text": "(a) K8 ea: 1.74 × 10−4",
        "title": "第31页-段落31",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1431",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9786379933357239,
        "probabilities": {
          "human": 0.9786379933357239,
          "aigc": 0.021362029016017914
        },
        "text": "(b) K4 ea: 1.54 × 10−3",
        "title": "第31页-段落32",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1432",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9889003038406372,
        "probabilities": {
          "human": 0.9889003038406372,
          "aigc": 0.01109967939555645
        },
        "text": "(c) K2 ea: 4.68 × 10−3",
        "title": "第31页-段落33",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1433",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第31页-段落34",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1434",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第31页-段落35",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1435",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第31页-段落36",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1436",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第31页-段落37",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1437",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第31页-段落38",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1438",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落39",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1439",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落40",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1440",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落41",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1441",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落42",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1442",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第31页-段落43",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1443",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第31页-段落44",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1444",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第31页-段落45",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1445",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第31页-段落46",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1446",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第31页-段落47",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1447",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第31页-段落48",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1448",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第31页-段落49",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1449",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第31页-段落50",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1450",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第31页-段落51",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1451",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9948169589042664,
        "probabilities": {
          "human": 0.9948169589042664,
          "aigc": 0.005183043424040079
        },
        "text": "0.3",
        "title": "第31页-段落52",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1452",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落53",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1453",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落54",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1454",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落55",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1455",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9972621202468872,
        "probabilities": {
          "human": 0.9972621202468872,
          "aigc": 0.0027378243394196033
        },
        "text": "(d) KV8 eo: 0.033",
        "title": "第31页-段落56",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1456",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985081553459167,
        "probabilities": {
          "human": 0.9985081553459167,
          "aigc": 0.0014917878434062004
        },
        "text": "(e) K8V4 eo: 0.117",
        "title": "第31页-段落57",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1457",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978063702583313,
        "probabilities": {
          "human": 0.9978063702583313,
          "aigc": 0.002193673513829708
        },
        "text": "(f) K8V2 eo: 0.446",
        "title": "第31页-段落58",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1458",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第31页-段落59",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1459",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第31页-段落60",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1460",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落61",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1461",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落62",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1462",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落63",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1463",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落64",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1464",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落65",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1465",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落66",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1466",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落67",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1467",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落68",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1468",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落69",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1469",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落70",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1470",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落71",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1471",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落72",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1472",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落73",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1473",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落74",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1474",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落75",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1475",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落76",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1476",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落77",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1477",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落78",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1478",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第31页-段落79",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1479",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第31页-段落80",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1480",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第31页-段落81",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1481",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第31页-段落82",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1482",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第31页-段落83",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1483",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落84",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1484",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落85",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1485",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落86",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1486",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.99892657995224,
        "probabilities": {
          "human": 0.99892657995224,
          "aigc": 0.0010734556708484888
        },
        "text": "(g) K4V8 eo: 0.292",
        "title": "第31页-段落87",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1487",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986727237701416,
        "probabilities": {
          "human": 0.9986727237701416,
          "aigc": 0.001327261095866561
        },
        "text": "(h) KV4 eo: 0.324",
        "title": "第31页-段落88",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1488",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983807802200317,
        "probabilities": {
          "human": 0.9983807802200317,
          "aigc": 0.0016192079056054354
        },
        "text": "(i) K4V2 eo: 0.557",
        "title": "第31页-段落89",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1489",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第31页-段落90",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1490",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第31页-段落91",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1491",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第31页-段落92",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1492",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第31页-段落93",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1493",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落94",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1494",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落95",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1495",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第31页-段落96",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1496",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落97",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1497",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落98",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1498",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第31页-段落99",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1499",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9968721270561218,
        "probabilities": {
          "human": 0.9968721270561218,
          "aigc": 0.0031278475653380156
        },
        "text": "1.3",
        "title": "第31页-段落100",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1500",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落101",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1501",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落102",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1502",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第31页-段落103",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1503",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979656934738159,
        "probabilities": {
          "human": 0.9979656934738159,
          "aigc": 0.0020343291107565165
        },
        "text": "1.1",
        "title": "第31页-段落104",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1504",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落105",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1505",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落106",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1506",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第31页-段落107",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1507",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第31页-段落108",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1508",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落109",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1509",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落110",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1510",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第31页-段落111",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1511",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落112",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1512",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第31页-段落113",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1513",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落114",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1514",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落115",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1515",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第31页-段落116",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1516",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989681243896484,
        "probabilities": {
          "human": 0.9989681243896484,
          "aigc": 0.0010319179855287075
        },
        "text": "(j) K2V8 eo: 0.948",
        "title": "第31页-段落117",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1517",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990429282188416,
        "probabilities": {
          "human": 0.9990429282188416,
          "aigc": 0.0009570185211487114
        },
        "text": "(k) K2V4 eo: 0.958",
        "title": "第31页-段落118",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1518",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986816048622131,
        "probabilities": {
          "human": 0.9986816048622131,
          "aigc": 0.0013184387935325503
        },
        "text": "(l) KV2 eo: 1.038",
        "title": "第31页-段落119",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1519",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993042945861816,
        "probabilities": {
          "human": 0.0006956387078389525,
          "aigc": 0.9993042945861816
        },
        "text": "Figure 16: Layer-wise attention score ea and relative attention output error eo of per-token-asym KV cache quantization\nwith simulated offline quantization and dequantization (without error accumulation) of the Qwen2.5-7B-Instruct model and\nthe first 20 prompts in the 0-shot GSM8K dataset. When the key quantization precision decreases to 4-bit or 2-bit, the\nlayer-wise relative attention output error distribution significantly shifts. It also explains the performance degradation of\nQwen2.5-7B-Instruct in the wikitext and other datasets. Especially, the errors of layer-3 and 13 are significantly larger than\nother layers. Note that in the 8-bit key cache quantization precision, only the first layer-0 and last layer-27 show significantly\nhigh errors, while in the 4-bit and 2-bit key cache quantization precision, the attention output errors of layer-3, 7, 10, 13, and\n23 become noticeable compared with the first and last layers. Although these layers have relative simpler attention patterns\nas demonstrated in Figure 12, the low-precision 4-bit and 2-bit key cache quantization results in significantly token-level\nattention distribution shift.",
        "title": "第31页-段落120",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1520",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9963461756706238,
        "probabilities": {
          "human": 0.9963461756706238,
          "aigc": 0.0036537968553602695
        },
        "text": "31",
        "title": "第31页-段落121",
        "page_number": 31,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1521",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第32页-段落1",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1522",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997621178627014,
        "probabilities": {
          "human": 0.9997621178627014,
          "aigc": 0.00023789575789123774
        },
        "text": "0.00200",
        "title": "第32页-段落2",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1523",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997504353523254,
        "probabilities": {
          "human": 0.9997504353523254,
          "aigc": 0.0002496192173566669
        },
        "text": "0.00035",
        "title": "第32页-段落3",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1524",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997723698616028,
        "probabilities": {
          "human": 0.9997723698616028,
          "aigc": 0.0002276668237755075
        },
        "text": "0.00175",
        "title": "第32页-段落4",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1525",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997723698616028,
        "probabilities": {
          "human": 0.9997723698616028,
          "aigc": 0.0002276668237755075
        },
        "text": "0.00175",
        "title": "第32页-段落5",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1526",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997326731681824,
        "probabilities": {
          "human": 0.9997326731681824,
          "aigc": 0.0002673604467418045
        },
        "text": "0.00030",
        "title": "第32页-段落6",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1527",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998586177825928,
        "probabilities": {
          "human": 0.9998586177825928,
          "aigc": 0.00014136242680251598
        },
        "text": "0.00150",
        "title": "第32页-段落7",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1528",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998586177825928,
        "probabilities": {
          "human": 0.9998586177825928,
          "aigc": 0.00014136242680251598
        },
        "text": "0.00150",
        "title": "第32页-段落8",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1529",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997716546058655,
        "probabilities": {
          "human": 0.9997716546058655,
          "aigc": 0.00022837534197606146
        },
        "text": "0.00025",
        "title": "第32页-段落9",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1530",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第32页-段落10",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1531",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第32页-段落11",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1532",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第32页-段落12",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1533",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998278617858887,
        "probabilities": {
          "human": 0.9998278617858887,
          "aigc": 0.00017205892072524875
        },
        "text": "0.00125",
        "title": "第32页-段落13",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1534",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998278617858887,
        "probabilities": {
          "human": 0.9998278617858887,
          "aigc": 0.00017205892072524875
        },
        "text": "0.00125",
        "title": "第32页-段落14",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1535",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997771382331848,
        "probabilities": {
          "human": 0.9997771382331848,
          "aigc": 0.00022288701438810676
        },
        "text": "0.00020",
        "title": "第32页-段落15",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1536",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997891783714294,
        "probabilities": {
          "human": 0.9997891783714294,
          "aigc": 0.00021078312420286238
        },
        "text": "0.00100",
        "title": "第32页-段落16",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1537",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997891783714294,
        "probabilities": {
          "human": 0.9997891783714294,
          "aigc": 0.00021078312420286238
        },
        "text": "0.00100",
        "title": "第32页-段落17",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1538",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997890591621399,
        "probabilities": {
          "human": 0.9997890591621399,
          "aigc": 0.00021090918744448572
        },
        "text": "0.00015",
        "title": "第32页-段落18",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1539",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996861219406128,
        "probabilities": {
          "human": 0.9996861219406128,
          "aigc": 0.0003139515465591103
        },
        "text": "0.00075",
        "title": "第32页-段落19",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1540",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996861219406128,
        "probabilities": {
          "human": 0.9996861219406128,
          "aigc": 0.0003139515465591103
        },
        "text": "0.00075",
        "title": "第32页-段落20",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1541",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997902512550354,
        "probabilities": {
          "human": 0.9997902512550354,
          "aigc": 0.00020982028217986226
        },
        "text": "0.00010",
        "title": "第32页-段落21",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1542",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998056292533875,
        "probabilities": {
          "human": 0.9998056292533875,
          "aigc": 0.00019443512428551912
        },
        "text": "0.00050",
        "title": "第32页-段落22",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1543",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998056292533875,
        "probabilities": {
          "human": 0.9998056292533875,
          "aigc": 0.00019443512428551912
        },
        "text": "0.00050",
        "title": "第32页-段落23",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1544",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996898174285889,
        "probabilities": {
          "human": 0.9996898174285889,
          "aigc": 0.000310188508592546
        },
        "text": "0.00005",
        "title": "第32页-段落24",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1545",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997716546058655,
        "probabilities": {
          "human": 0.9997716546058655,
          "aigc": 0.00022837534197606146
        },
        "text": "0.00025",
        "title": "第32页-段落25",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1546",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997716546058655,
        "probabilities": {
          "human": 0.9997716546058655,
          "aigc": 0.00022837534197606146
        },
        "text": "0.00025",
        "title": "第32页-段落26",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1547",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995447993278503,
        "probabilities": {
          "human": 0.9995447993278503,
          "aigc": 0.0004551542515400797
        },
        "text": "0.00000",
        "title": "第32页-段落27",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1548",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995447993278503,
        "probabilities": {
          "human": 0.9995447993278503,
          "aigc": 0.0004551542515400797
        },
        "text": "0.00000",
        "title": "第32页-段落28",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1549",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落29",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1550",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落30",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1551",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落31",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1552",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9769185185432434,
        "probabilities": {
          "human": 0.9769185185432434,
          "aigc": 0.02308148518204689
        },
        "text": "(a) K8 ea: 1.8 × 10−5",
        "title": "第32页-段落32",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1553",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9842211008071899,
        "probabilities": {
          "human": 0.9842211008071899,
          "aigc": 0.01577891781926155
        },
        "text": "(b) K4 ea: 1.68 × 10−4",
        "title": "第32页-段落33",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1554",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9833161234855652,
        "probabilities": {
          "human": 0.9833161234855652,
          "aigc": 0.01668381877243519
        },
        "text": "(c) K2 ea: 5.00 × 10−3",
        "title": "第32页-段落34",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1555",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980891346931458,
        "probabilities": {
          "human": 0.9980891346931458,
          "aigc": 0.0019108442356809974
        },
        "text": "0.70",
        "title": "第32页-段落35",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1556",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第32页-段落36",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1557",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第32页-段落37",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1558",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第32页-段落38",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1559",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落39",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1560",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落40",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1561",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落41",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1562",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第32页-段落42",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1563",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第32页-段落43",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1564",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第32页-段落44",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1565",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第32页-段落45",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1566",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第32页-段落46",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1567",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第32页-段落47",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1568",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第32页-段落48",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1569",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第32页-段落49",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1570",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第32页-段落50",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1571",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第32页-段落51",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1572",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第32页-段落52",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1573",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第32页-段落53",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1574",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第32页-段落54",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1575",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第32页-段落55",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1576",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落56",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1577",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落57",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1578",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落58",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1579",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976006150245667,
        "probabilities": {
          "human": 0.9976006150245667,
          "aigc": 0.0023993980139493942
        },
        "text": "(d) KV8 eo: 0.031",
        "title": "第32页-段落59",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1580",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984521865844727,
        "probabilities": {
          "human": 0.9984521865844727,
          "aigc": 0.0015477407723665237
        },
        "text": "(e) K8V4 eo: 0.110",
        "title": "第32页-段落60",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1581",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977152347564697,
        "probabilities": {
          "human": 0.9977152347564697,
          "aigc": 0.0022847498767077923
        },
        "text": "(f) K8V2 eo: 0.427",
        "title": "第32页-段落61",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1582",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落62",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1583",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落63",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1584",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落64",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1585",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落65",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1586",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落66",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1587",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落67",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1588",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落68",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1589",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落69",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1590",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落70",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1591",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落71",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1592",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落72",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1593",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落73",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1594",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第32页-段落74",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1595",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第32页-段落75",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1596",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第32页-段落76",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1597",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第32页-段落77",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1598",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第32页-段落78",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1599",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第32页-段落79",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1600",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第32页-段落80",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1601",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955794215202332,
        "probabilities": {
          "human": 0.9955794215202332,
          "aigc": 0.004420551937073469
        },
        "text": "0.2",
        "title": "第32页-段落81",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1602",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落82",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1603",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落83",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1604",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落84",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1605",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985156655311584,
        "probabilities": {
          "human": 0.9985156655311584,
          "aigc": 0.001484319451265037
        },
        "text": "(g) K4V8 eo: 0.280",
        "title": "第32页-段落85",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1606",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985243678092957,
        "probabilities": {
          "human": 0.9985243678092957,
          "aigc": 0.0014756296295672655
        },
        "text": "(h) KV4 eo: 0.310",
        "title": "第32页-段落86",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1607",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988401532173157,
        "probabilities": {
          "human": 0.9988401532173157,
          "aigc": 0.001159842824563384
        },
        "text": "(i) K4V2 eo: 0.531",
        "title": "第32页-段落87",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1608",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第32页-段落88",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1609",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第32页-段落89",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1610",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9968721270561218,
        "probabilities": {
          "human": 0.9968721270561218,
          "aigc": 0.0031278475653380156
        },
        "text": "1.3",
        "title": "第32页-段落90",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1611",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9968721270561218,
        "probabilities": {
          "human": 0.9968721270561218,
          "aigc": 0.0031278475653380156
        },
        "text": "1.3",
        "title": "第32页-段落91",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1612",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9968721270561218,
        "probabilities": {
          "human": 0.9968721270561218,
          "aigc": 0.0031278475653380156
        },
        "text": "1.3",
        "title": "第32页-段落92",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1613",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落93",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1614",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落94",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1615",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第32页-段落95",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1616",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落96",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1617",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落97",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1618",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第32页-段落98",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1619",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979656934738159,
        "probabilities": {
          "human": 0.9979656934738159,
          "aigc": 0.0020343291107565165
        },
        "text": "1.1",
        "title": "第32页-段落99",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1620",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979656934738159,
        "probabilities": {
          "human": 0.9979656934738159,
          "aigc": 0.0020343291107565165
        },
        "text": "1.1",
        "title": "第32页-段落100",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1621",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979656934738159,
        "probabilities": {
          "human": 0.9979656934738159,
          "aigc": 0.0020343291107565165
        },
        "text": "1.1",
        "title": "第32页-段落101",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1622",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落102",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1623",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落103",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1624",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第32页-段落104",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1625",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第32页-段落105",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1626",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第32页-段落106",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1627",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995112955570221,
        "probabilities": {
          "human": 0.995112955570221,
          "aigc": 0.0048871031031012535
        },
        "text": "0.9",
        "title": "第32页-段落107",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1628",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落108",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1629",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落109",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1630",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第32页-段落110",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1631",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第32页-段落111",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1632",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第32页-段落112",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1633",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9929452538490295,
        "probabilities": {
          "human": 0.9929452538490295,
          "aigc": 0.007054754067212343
        },
        "text": "0.7",
        "title": "第32页-段落113",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1634",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第32页-段落114",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1635",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第32页-段落115",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1636",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落116",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1637",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落117",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1638",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第32页-段落118",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1639",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989336133003235,
        "probabilities": {
          "human": 0.9989336133003235,
          "aigc": 0.0010663657449185848
        },
        "text": "(j) K2V8 eo: 0.901",
        "title": "第32页-段落119",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1640",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989927411079407,
        "probabilities": {
          "human": 0.9989927411079407,
          "aigc": 0.0010072625009343028
        },
        "text": "(k) K2V4 eo: 0.909",
        "title": "第32页-段落120",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1641",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986566305160522,
        "probabilities": {
          "human": 0.9986566305160522,
          "aigc": 0.001343333744443953
        },
        "text": "(l) K2V2 eo: 0.961",
        "title": "第32页-段落121",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1642",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9993083477020264,
        "probabilities": {
          "human": 0.0006916282000020146,
          "aigc": 0.9993083477020264
        },
        "text": "Figure 17: Layer-wise attention score ea and relative attention output error eo of per-token-asym KV cache quantization\nwith simulated offline quantization and dequantization (without error accumulation) of the Qwen2.5-7B-Instruct model and\nthe first 20 prompts in the AIGC multiturn softage dataset. The layer-wise attention error shift is similar to Figure 16,\nindicating that the layer-wise sensitivity to KV cache quantization is independent of the input prompts and even domains.",
        "title": "第32页-段落122",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1643",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9943813681602478,
        "probabilities": {
          "human": 0.9943813681602478,
          "aigc": 0.005618650931864977
        },
        "text": "32",
        "title": "第32页-段落123",
        "page_number": 32,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1644",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第33页-段落1",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1645",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9172338247299194,
        "probabilities": {
          "human": 0.9172338247299194,
          "aigc": 0.08276616781949997
        },
        "text": "1e\n5",
        "title": "第33页-段落2",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1646",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9290469288825989,
        "probabilities": {
          "human": 0.9290469288825989,
          "aigc": 0.07095304131507874
        },
        "text": "6",
        "title": "第33页-段落3",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1647",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997007846832275,
        "probabilities": {
          "human": 0.9997007846832275,
          "aigc": 0.0002992149966303259
        },
        "text": "0.0012",
        "title": "第33页-段落4",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1648",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997716546058655,
        "probabilities": {
          "human": 0.9997716546058655,
          "aigc": 0.00022837534197606146
        },
        "text": "0.00025",
        "title": "第33页-段落5",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1649",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9590485692024231,
        "probabilities": {
          "human": 0.9590485692024231,
          "aigc": 0.04095141589641571
        },
        "text": "5",
        "title": "第33页-段落6",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1650",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996285438537598,
        "probabilities": {
          "human": 0.9996285438537598,
          "aigc": 0.00037139817140996456
        },
        "text": "0.0010",
        "title": "第33页-段落7",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1651",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第33页-段落8",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1652",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第33页-段落9",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1653",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997771382331848,
        "probabilities": {
          "human": 0.9997771382331848,
          "aigc": 0.00022288701438810676
        },
        "text": "0.00020",
        "title": "第33页-段落10",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1654",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第33页-段落11",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1655",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9662643074989319,
        "probabilities": {
          "human": 0.9662643074989319,
          "aigc": 0.0337357223033905
        },
        "text": "4",
        "title": "第33页-段落12",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1656",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995049238204956,
        "probabilities": {
          "human": 0.9995049238204956,
          "aigc": 0.0004950642469339073
        },
        "text": "0.0008",
        "title": "第33页-段落13",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1657",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997890591621399,
        "probabilities": {
          "human": 0.9997890591621399,
          "aigc": 0.00021090918744448572
        },
        "text": "0.00015",
        "title": "第33页-段落14",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1658",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9549646377563477,
        "probabilities": {
          "human": 0.9549646377563477,
          "aigc": 0.04503533989191055
        },
        "text": "3",
        "title": "第33页-段落15",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1659",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992005228996277,
        "probabilities": {
          "human": 0.9992005228996277,
          "aigc": 0.0007995329797267914
        },
        "text": "0.0006",
        "title": "第33页-段落16",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1660",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9529740214347839,
        "probabilities": {
          "human": 0.9529740214347839,
          "aigc": 0.04702598601579666
        },
        "text": "2",
        "title": "第33页-段落17",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1661",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997902512550354,
        "probabilities": {
          "human": 0.9997902512550354,
          "aigc": 0.00020982028217986226
        },
        "text": "0.00010",
        "title": "第33页-段落18",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1662",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995656609535217,
        "probabilities": {
          "human": 0.9995656609535217,
          "aigc": 0.0004343086911831051
        },
        "text": "0.0004",
        "title": "第33页-段落19",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1663",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9798263311386108,
        "probabilities": {
          "human": 0.9798263311386108,
          "aigc": 0.020173681899905205
        },
        "text": "1",
        "title": "第33页-段落20",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1664",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996898174285889,
        "probabilities": {
          "human": 0.9996898174285889,
          "aigc": 0.000310188508592546
        },
        "text": "0.00005",
        "title": "第33页-段落21",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1665",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996066689491272,
        "probabilities": {
          "human": 0.9996066689491272,
          "aigc": 0.0003933655098080635
        },
        "text": "0.0002",
        "title": "第33页-段落22",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1666",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.914262592792511,
        "probabilities": {
          "human": 0.914262592792511,
          "aigc": 0.08573737740516663
        },
        "text": "0",
        "title": "第33页-段落23",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1667",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落24",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1668",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落25",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1669",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落26",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1670",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9806893467903137,
        "probabilities": {
          "human": 0.9806893467903137,
          "aigc": 0.0193106047809124
        },
        "text": "(a) K8 ea: 8.0 × 10−6",
        "title": "第33页-段落27",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1671",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.974237859249115,
        "probabilities": {
          "human": 0.974237859249115,
          "aigc": 0.0257621631026268
        },
        "text": "(b) K4 ea: 8.3 × 10−5",
        "title": "第33页-段落28",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1672",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9884776473045349,
        "probabilities": {
          "human": 0.9884776473045349,
          "aigc": 0.011522375978529453
        },
        "text": "(c) K2 ea: 3.92 × 10−4",
        "title": "第33页-段落29",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1673",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第33页-段落30",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1674",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第33页-段落31",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1675",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第33页-段落32",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1676",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第33页-段落33",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1677",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959213733673096,
        "probabilities": {
          "human": 0.9959213733673096,
          "aigc": 0.004078585188835859
        },
        "text": "0.07",
        "title": "第33页-段落34",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1678",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落35",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1679",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落36",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1680",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落37",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1681",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第33页-段落38",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1682",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第33页-段落39",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1683",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第33页-段落40",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1684",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第33页-段落41",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1685",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第33页-段落42",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1686",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974861145019531,
        "probabilities": {
          "human": 0.9974861145019531,
          "aigc": 0.0025139269419014454
        },
        "text": "0.05",
        "title": "第33页-段落43",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1687",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第33页-段落44",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1688",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第33页-段落45",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1689",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9979687333106995,
        "probabilities": {
          "human": 0.9979687333106995,
          "aigc": 0.002031297655776143
        },
        "text": "0.04",
        "title": "第33页-段落46",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1690",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第33页-段落47",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1691",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第33页-段落48",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1692",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9973485469818115,
        "probabilities": {
          "human": 0.9973485469818115,
          "aigc": 0.0026514967903494835
        },
        "text": "0.03",
        "title": "第33页-段落49",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1693",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第33页-段落50",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1694",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977206587791443,
        "probabilities": {
          "human": 0.9977206587791443,
          "aigc": 0.00227933912537992
        },
        "text": "0.02",
        "title": "第33页-段落51",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1695",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第33页-段落52",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1696",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976287484169006,
        "probabilities": {
          "human": 0.9976287484169006,
          "aigc": 0.0023712553083896637
        },
        "text": "0.01",
        "title": "第33页-段落53",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1697",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第33页-段落54",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1698",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第33页-段落55",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1699",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落56",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1700",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落57",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1701",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落58",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1702",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9967407584190369,
        "probabilities": {
          "human": 0.9967407584190369,
          "aigc": 0.003259270917624235
        },
        "text": "(d) KV8 eo: 0.017",
        "title": "第33页-段落59",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1703",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986938834190369,
        "probabilities": {
          "human": 0.9986938834190369,
          "aigc": 0.001306084799580276
        },
        "text": "(e) K8V4 eo: 0.101",
        "title": "第33页-段落60",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1704",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980646967887878,
        "probabilities": {
          "human": 0.9980646967887878,
          "aigc": 0.0019353254465386271
        },
        "text": "(f) K8V2 eo: 0.424",
        "title": "第33页-段落61",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1705",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996182918548584,
        "probabilities": {
          "human": 0.9996182918548584,
          "aigc": 0.0003816639364231378
        },
        "text": "0.250",
        "title": "第33页-段落62",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1706",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第33页-段落63",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1707",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992924928665161,
        "probabilities": {
          "human": 0.9992924928665161,
          "aigc": 0.0007074420573189855
        },
        "text": "0.275",
        "title": "第33页-段落64",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1708",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994695782661438,
        "probabilities": {
          "human": 0.9994695782661438,
          "aigc": 0.0005304827354848385
        },
        "text": "0.225",
        "title": "第33页-段落65",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1709",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第33页-段落66",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1710",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落67",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1711",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落68",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1712",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996182918548584,
        "probabilities": {
          "human": 0.9996182918548584,
          "aigc": 0.0003816639364231378
        },
        "text": "0.250",
        "title": "第33页-段落69",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1713",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落70",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1714",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999346911907196,
        "probabilities": {
          "human": 0.999346911907196,
          "aigc": 0.0006531361141242087
        },
        "text": "0.200",
        "title": "第33页-段落71",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1715",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第33页-段落72",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1716",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994695782661438,
        "probabilities": {
          "human": 0.9994695782661438,
          "aigc": 0.0005304827354848385
        },
        "text": "0.225",
        "title": "第33页-段落73",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1717",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994631409645081,
        "probabilities": {
          "human": 0.9994631409645081,
          "aigc": 0.0005368837155401707
        },
        "text": "0.175",
        "title": "第33页-段落74",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1718",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第33页-段落75",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1719",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999346911907196,
        "probabilities": {
          "human": 0.999346911907196,
          "aigc": 0.0006531361141242087
        },
        "text": "0.200",
        "title": "第33页-段落76",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1720",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996342658996582,
        "probabilities": {
          "human": 0.9996342658996582,
          "aigc": 0.0003657276974990964
        },
        "text": "0.150",
        "title": "第33页-段落77",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1721",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第33页-段落78",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1722",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994631409645081,
        "probabilities": {
          "human": 0.9994631409645081,
          "aigc": 0.0005368837155401707
        },
        "text": "0.175",
        "title": "第33页-段落79",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1723",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995495676994324,
        "probabilities": {
          "human": 0.9995495676994324,
          "aigc": 0.00045040101394988596
        },
        "text": "0.125",
        "title": "第33页-段落80",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1724",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第33页-段落81",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1725",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996342658996582,
        "probabilities": {
          "human": 0.9996342658996582,
          "aigc": 0.0003657276974990964
        },
        "text": "0.150",
        "title": "第33页-段落82",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1726",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992352724075317,
        "probabilities": {
          "human": 0.9992352724075317,
          "aigc": 0.0007647418533451855
        },
        "text": "0.100",
        "title": "第33页-段落83",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1727",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第33页-段落84",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1728",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995495676994324,
        "probabilities": {
          "human": 0.9995495676994324,
          "aigc": 0.00045040101394988596
        },
        "text": "0.125",
        "title": "第33页-段落85",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1729",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991389513015747,
        "probabilities": {
          "human": 0.9991389513015747,
          "aigc": 0.0008610335062257946
        },
        "text": "0.075",
        "title": "第33页-段落86",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1730",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落87",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1731",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落88",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1732",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落89",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1733",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987785220146179,
        "probabilities": {
          "human": 0.9987785220146179,
          "aigc": 0.0012214978924021125
        },
        "text": "(g) K4V8 eo: 0.131",
        "title": "第33页-段落90",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1734",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986055493354797,
        "probabilities": {
          "human": 0.9986055493354797,
          "aigc": 0.0013944774400442839
        },
        "text": "(h) KV4 eo: 0.174",
        "title": "第33页-段落91",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1735",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987719655036926,
        "probabilities": {
          "human": 0.9987719655036926,
          "aigc": 0.001228046021424234
        },
        "text": "(i) K4V2 eo: 0.454",
        "title": "第33页-段落92",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1736",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9959024786949158,
        "probabilities": {
          "human": 0.9959024786949158,
          "aigc": 0.004097583703696728
        },
        "text": "1.6",
        "title": "第33页-段落93",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1737",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第33页-段落94",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1738",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第33页-段落95",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1739",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9977601766586304,
        "probabilities": {
          "human": 0.9977601766586304,
          "aigc": 0.0022397860884666443
        },
        "text": "1.4",
        "title": "第33页-段落96",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1740",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落97",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1741",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落98",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1742",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第33页-段落99",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1743",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第33页-段落100",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1744",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第33页-段落101",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1745",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974508881568909,
        "probabilities": {
          "human": 0.9974508881568909,
          "aigc": 0.0025491174310445786
        },
        "text": "1.2",
        "title": "第33页-段落102",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1746",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第33页-段落103",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1747",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第33页-段落104",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1748",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第33页-段落105",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1749",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第33页-段落106",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1750",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第33页-段落107",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1751",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第33页-段落108",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1752",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第33页-段落109",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1753",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9956041574478149,
        "probabilities": {
          "human": 0.9956041574478149,
          "aigc": 0.004395889118313789
        },
        "text": "0.8",
        "title": "第33页-段落110",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1754",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第33页-段落111",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1755",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9961075186729431,
        "probabilities": {
          "human": 0.9961075186729431,
          "aigc": 0.003892492735758424
        },
        "text": "0.4",
        "title": "第33页-段落112",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1756",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9933878183364868,
        "probabilities": {
          "human": 0.9933878183364868,
          "aigc": 0.006612131372094154
        },
        "text": "0.6",
        "title": "第33页-段落113",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1757",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落114",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1758",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落115",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1759",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9475033283233643,
        "probabilities": {
          "human": 0.9475033283233643,
          "aigc": 0.052496667951345444
        },
        "text": "0\n5\n10\n15\n20\n25\nLayer id",
        "title": "第33页-段落116",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1760",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988232254981995,
        "probabilities": {
          "human": 0.9988232254981995,
          "aigc": 0.0011768025578930974
        },
        "text": "(j) K2V8 eo: 0.679",
        "title": "第33页-段落117",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1761",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989168643951416,
        "probabilities": {
          "human": 0.9989168643951416,
          "aigc": 0.0010831588879227638
        },
        "text": "(k) K2V4 eo: 0.696",
        "title": "第33页-段落118",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1762",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984920024871826,
        "probabilities": {
          "human": 0.9984920024871826,
          "aigc": 0.0015079459408298135
        },
        "text": "(l) K2V2 eo: 0.838",
        "title": "第33页-段落119",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1763",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9989385008811951,
        "probabilities": {
          "human": 0.0010615127393975854,
          "aigc": 0.9989385008811951
        },
        "text": "Figure 18: Layer-wise attention score ea and relative attention output error eo of key per-channel-asym and value\nper-token-asym quantization with simulated offline quantization and dequantization (without error accumulation) of the\nQwen2.5-7B-Instruct model and the first 20 prompts in the AIGC multiturn softage dataset. Key quantization along the\nchannel dimension significantly affects the distribution of critical layers for 4-bit and 2-bit precision compared with those in\nFigure 17. The averaged attention output errors eo under the same KV precision pairs also dramatically reduced.",
        "title": "第33页-段落120",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1764",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9927603006362915,
        "probabilities": {
          "human": 0.9927603006362915,
          "aigc": 0.0072397696785628796
        },
        "text": "33",
        "title": "第33页-段落121",
        "page_number": 33,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1765",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第34页-段落1",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1766",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997326731681824,
        "probabilities": {
          "human": 0.9997326731681824,
          "aigc": 0.0002673604467418045
        },
        "text": "0.00030",
        "title": "第34页-段落2",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1767",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993957281112671,
        "probabilities": {
          "human": 0.9993957281112671,
          "aigc": 0.0006042672321200371
        },
        "text": "0.0200",
        "title": "第34页-段落3",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1768",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992576241493225,
        "probabilities": {
          "human": 0.9992576241493225,
          "aigc": 0.0007423667120747268
        },
        "text": "0.004",
        "title": "第34页-段落4",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1769",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995777010917664,
        "probabilities": {
          "human": 0.9995777010917664,
          "aigc": 0.00042231963016092777
        },
        "text": "0.0175",
        "title": "第34页-段落5",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1770",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997716546058655,
        "probabilities": {
          "human": 0.9997716546058655,
          "aigc": 0.00022837534197606146
        },
        "text": "0.00025",
        "title": "第34页-段落6",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1771",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997106194496155,
        "probabilities": {
          "human": 0.9997106194496155,
          "aigc": 0.00028935197042301297
        },
        "text": "0.0150",
        "title": "第34页-段落7",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1772",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第34页-段落8",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1773",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第34页-段落9",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1774",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8450453281402588,
        "probabilities": {
          "human": 0.1549546867609024,
          "aigc": 0.8450453281402588
        },
        "text": "Attention score error",
        "title": "第34页-段落10",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1775",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997771382331848,
        "probabilities": {
          "human": 0.9997771382331848,
          "aigc": 0.00022288701438810676
        },
        "text": "0.00020",
        "title": "第34页-段落11",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1776",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991624355316162,
        "probabilities": {
          "human": 0.9991624355316162,
          "aigc": 0.0008376350160688162
        },
        "text": "0.003",
        "title": "第34页-段落12",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1777",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996048808097839,
        "probabilities": {
          "human": 0.9996048808097839,
          "aigc": 0.0003951281832996756
        },
        "text": "0.0125",
        "title": "第34页-段落13",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1778",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997890591621399,
        "probabilities": {
          "human": 0.9997890591621399,
          "aigc": 0.00021090918744448572
        },
        "text": "0.00015",
        "title": "第34页-段落14",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1779",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994840621948242,
        "probabilities": {
          "human": 0.9994840621948242,
          "aigc": 0.0005159316351637244
        },
        "text": "0.0100",
        "title": "第34页-段落15",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1780",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993071556091309,
        "probabilities": {
          "human": 0.9993071556091309,
          "aigc": 0.0006928837392479181
        },
        "text": "0.002",
        "title": "第34页-段落16",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1781",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994761347770691,
        "probabilities": {
          "human": 0.9994761347770691,
          "aigc": 0.0005239242454990745
        },
        "text": "0.0075",
        "title": "第34页-段落17",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1782",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9997902512550354,
        "probabilities": {
          "human": 0.9997902512550354,
          "aigc": 0.00020982028217986226
        },
        "text": "0.00010",
        "title": "第34页-段落18",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1783",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996929168701172,
        "probabilities": {
          "human": 0.9996929168701172,
          "aigc": 0.0003071600804105401
        },
        "text": "0.0050",
        "title": "第34页-段落19",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1784",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994066953659058,
        "probabilities": {
          "human": 0.9994066953659058,
          "aigc": 0.0005933357169851661
        },
        "text": "0.001",
        "title": "第34页-段落20",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1785",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996898174285889,
        "probabilities": {
          "human": 0.9996898174285889,
          "aigc": 0.000310188508592546
        },
        "text": "0.00005",
        "title": "第34页-段落21",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1786",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995228052139282,
        "probabilities": {
          "human": 0.9995228052139282,
          "aigc": 0.0004772258980665356
        },
        "text": "0.0025",
        "title": "第34页-段落22",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1787",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988836646080017,
        "probabilities": {
          "human": 0.9988836646080017,
          "aigc": 0.0011163086164742708
        },
        "text": "0.000",
        "title": "第34页-段落23",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1788",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995447993278503,
        "probabilities": {
          "human": 0.9995447993278503,
          "aigc": 0.0004551542515400797
        },
        "text": "0.00000",
        "title": "第34页-段落24",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1789",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993269443511963,
        "probabilities": {
          "human": 0.9993269443511963,
          "aigc": 0.0006731341127306223
        },
        "text": "0.0000",
        "title": "第34页-段落25",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1790",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落26",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1791",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落27",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1792",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落28",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1793",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9904416799545288,
        "probabilities": {
          "human": 0.9904416799545288,
          "aigc": 0.009558310732245445
        },
        "text": "(a) K8: 5.90 × 10−5",
        "title": "第34页-段落29",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1794",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9856085777282715,
        "probabilities": {
          "human": 0.9856085777282715,
          "aigc": 0.014391457661986351
        },
        "text": "(b) K4: 8.51 × 10−4",
        "title": "第34页-段落30",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1795",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9836286902427673,
        "probabilities": {
          "human": 0.9836286902427673,
          "aigc": 0.016371337696909904
        },
        "text": "(c) K2: 4.04 × 10−3",
        "title": "第34页-段落31",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1796",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985718727111816,
        "probabilities": {
          "human": 0.9985718727111816,
          "aigc": 0.001428139046765864
        },
        "text": "0.22",
        "title": "第34页-段落32",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1797",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第34页-段落33",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1798",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第34页-段落34",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1799",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989742040634155,
        "probabilities": {
          "human": 0.9989742040634155,
          "aigc": 0.0010258157271891832
        },
        "text": "0.020",
        "title": "第34页-段落35",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1800",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落36",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1801",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落37",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1802",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落38",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1803",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第34页-段落39",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1804",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986950755119324,
        "probabilities": {
          "human": 0.9986950755119324,
          "aigc": 0.0013049826957285404
        },
        "text": "0.18",
        "title": "第34页-段落40",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1805",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992164373397827,
        "probabilities": {
          "human": 0.9992164373397827,
          "aigc": 0.00078356615267694
        },
        "text": "0.018",
        "title": "第34页-段落41",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1806",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第34页-段落42",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1807",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9976329803466797,
        "probabilities": {
          "human": 0.9976329803466797,
          "aigc": 0.0023670201189816
        },
        "text": "0.16",
        "title": "第34页-段落43",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1808",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987271428108215,
        "probabilities": {
          "human": 0.9987271428108215,
          "aigc": 0.0012728179572150111
        },
        "text": "0.016",
        "title": "第34页-段落44",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1809",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989007711410522,
        "probabilities": {
          "human": 0.9989007711410522,
          "aigc": 0.0010992471361532807
        },
        "text": "0.14",
        "title": "第34页-段落45",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1810",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第34页-段落46",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1811",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993630051612854,
        "probabilities": {
          "human": 0.9993630051612854,
          "aigc": 0.0006369950715452433
        },
        "text": "0.014",
        "title": "第34页-段落47",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1812",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986730813980103,
        "probabilities": {
          "human": 0.9986730813980103,
          "aigc": 0.0013269685441628098
        },
        "text": "0.12",
        "title": "第34页-段落48",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1813",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第34页-段落49",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1814",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980625510215759,
        "probabilities": {
          "human": 0.9980625510215759,
          "aigc": 0.0019373914692550898
        },
        "text": "0.10",
        "title": "第34页-段落50",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1815",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993888139724731,
        "probabilities": {
          "human": 0.9993888139724731,
          "aigc": 0.0006111774710007012
        },
        "text": "0.012",
        "title": "第34页-段落51",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1816",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第34页-段落52",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1817",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975504279136658,
        "probabilities": {
          "human": 0.9975504279136658,
          "aigc": 0.0024495613761246204
        },
        "text": "0.08",
        "title": "第34页-段落53",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1818",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第34页-段落54",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1819",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991521835327148,
        "probabilities": {
          "human": 0.9991521835327148,
          "aigc": 0.0008478129166178405
        },
        "text": "0.010",
        "title": "第34页-段落55",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1820",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.995676577091217,
        "probabilities": {
          "human": 0.995676577091217,
          "aigc": 0.0043234690092504025
        },
        "text": "0.06",
        "title": "第34页-段落56",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1821",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第34页-段落57",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1822",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落58",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1823",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落59",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1824",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落60",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1825",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9974545836448669,
        "probabilities": {
          "human": 0.9974545836448669,
          "aigc": 0.002545441733673215
        },
        "text": "(d) KV8 eo: 0.013",
        "title": "第34页-段落61",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1826",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987667798995972,
        "probabilities": {
          "human": 0.9987667798995972,
          "aigc": 0.001233189250342548
        },
        "text": "(e) K8V4 eo: 0.102",
        "title": "第34页-段落62",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1827",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980879426002502,
        "probabilities": {
          "human": 0.9980879426002502,
          "aigc": 0.0019120387732982635
        },
        "text": "(f) K8V2 eo: 0.411",
        "title": "第34页-段落63",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1828",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980891346931458,
        "probabilities": {
          "human": 0.9980891346931458,
          "aigc": 0.0019108442356809974
        },
        "text": "0.70",
        "title": "第34页-段落64",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1829",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992924928665161,
        "probabilities": {
          "human": 0.9992924928665161,
          "aigc": 0.0007074420573189855
        },
        "text": "0.275",
        "title": "第34页-段落65",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1830",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981028437614441,
        "probabilities": {
          "human": 0.9981028437614441,
          "aigc": 0.0018972244579344988
        },
        "text": "0.65",
        "title": "第34页-段落66",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1831",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第34页-段落67",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1832",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996182918548584,
        "probabilities": {
          "human": 0.9996182918548584,
          "aigc": 0.0003816639364231378
        },
        "text": "0.250",
        "title": "第34页-段落68",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1833",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落69",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1834",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落70",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1835",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落71",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1836",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9981776475906372,
        "probabilities": {
          "human": 0.9981776475906372,
          "aigc": 0.0018223667284473777
        },
        "text": "0.60",
        "title": "第34页-段落72",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1837",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994695782661438,
        "probabilities": {
          "human": 0.9994695782661438,
          "aigc": 0.0005304827354848385
        },
        "text": "0.225",
        "title": "第34页-段落73",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1838",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9987558126449585,
        "probabilities": {
          "human": 0.9987558126449585,
          "aigc": 0.00124417117331177
        },
        "text": "0.55",
        "title": "第34页-段落74",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1839",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9983186721801758,
        "probabilities": {
          "human": 0.9983186721801758,
          "aigc": 0.001681337016634643
        },
        "text": "0.25",
        "title": "第34页-段落75",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1840",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999346911907196,
        "probabilities": {
          "human": 0.999346911907196,
          "aigc": 0.0006531361141242087
        },
        "text": "0.200",
        "title": "第34页-段落76",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1841",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989238381385803,
        "probabilities": {
          "human": 0.9989238381385803,
          "aigc": 0.001076166401617229
        },
        "text": "0.50",
        "title": "第34页-段落77",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1842",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994631409645081,
        "probabilities": {
          "human": 0.9994631409645081,
          "aigc": 0.0005368837155401707
        },
        "text": "0.175",
        "title": "第34页-段落78",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1843",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9978731870651245,
        "probabilities": {
          "human": 0.9978731870651245,
          "aigc": 0.002126824576407671
        },
        "text": "0.20",
        "title": "第34页-段落79",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1844",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989855885505676,
        "probabilities": {
          "human": 0.9989855885505676,
          "aigc": 0.0010143679101020098
        },
        "text": "0.45",
        "title": "第34页-段落80",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1845",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996342658996582,
        "probabilities": {
          "human": 0.9996342658996582,
          "aigc": 0.0003657276974990964
        },
        "text": "0.150",
        "title": "第34页-段落81",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1846",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9989446997642517,
        "probabilities": {
          "human": 0.9989446997642517,
          "aigc": 0.0010553357424214482
        },
        "text": "0.40",
        "title": "第34页-段落82",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1847",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9995495676994324,
        "probabilities": {
          "human": 0.9995495676994324,
          "aigc": 0.00045040101394988596
        },
        "text": "0.125",
        "title": "第34页-段落83",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1848",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984581470489502,
        "probabilities": {
          "human": 0.9984581470489502,
          "aigc": 0.0015418886905536056
        },
        "text": "0.15",
        "title": "第34页-段落84",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1849",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984017014503479,
        "probabilities": {
          "human": 0.9984017014503479,
          "aigc": 0.0015983461635187268
        },
        "text": "0.35",
        "title": "第34页-段落85",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1850",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9992352724075317,
        "probabilities": {
          "human": 0.9992352724075317,
          "aigc": 0.0007647418533451855
        },
        "text": "0.100",
        "title": "第34页-段落86",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1851",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9980263113975525,
        "probabilities": {
          "human": 0.9980263113975525,
          "aigc": 0.0019737009424716234
        },
        "text": "0.30",
        "title": "第34页-段落87",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1852",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9991389513015747,
        "probabilities": {
          "human": 0.9991389513015747,
          "aigc": 0.0008610335062257946
        },
        "text": "0.075",
        "title": "第34页-段落88",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1853",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落89",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1854",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落90",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1855",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落91",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1856",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9986981153488159,
        "probabilities": {
          "human": 0.9986981153488159,
          "aigc": 0.001301836920902133
        },
        "text": "(g) K4V8 eo: 0.149",
        "title": "第34页-段落92",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1857",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9990572333335876,
        "probabilities": {
          "human": 0.9990572333335876,
          "aigc": 0.0009427700424566865
        },
        "text": "(h) KV4 eo: 0.191",
        "title": "第34页-段落93",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1858",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985694885253906,
        "probabilities": {
          "human": 0.9985694885253906,
          "aigc": 0.0014305299846455455
        },
        "text": "(i) K4V2 eo: 0.453",
        "title": "第34页-段落94",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1859",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9898854494094849,
        "probabilities": {
          "human": 0.9898854494094849,
          "aigc": 0.010114525444805622
        },
        "text": "3.0",
        "title": "第34页-段落95",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1860",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第34页-段落96",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1861",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第34页-段落97",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1862",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9960911870002747,
        "probabilities": {
          "human": 0.9960911870002747,
          "aigc": 0.003908805549144745
        },
        "text": "2.5",
        "title": "第34页-段落98",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1863",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落99",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1864",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落100",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1865",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8946127891540527,
        "probabilities": {
          "human": 0.10538721829652786,
          "aigc": 0.8946127891540527
        },
        "text": "Attention output relative error",
        "title": "第34页-段落101",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1866",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第34页-段落102",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1867",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第34页-段落103",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1868",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.992738664150238,
        "probabilities": {
          "human": 0.992738664150238,
          "aigc": 0.007261344231665134
        },
        "text": "2.0",
        "title": "第34页-段落104",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1869",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第34页-段落105",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1870",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第34页-段落106",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1871",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9975739121437073,
        "probabilities": {
          "human": 0.9975739121437073,
          "aigc": 0.002426144201308489
        },
        "text": "1.5",
        "title": "第34页-段落107",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1872",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第34页-段落108",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1873",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第34页-段落109",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1874",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9949449896812439,
        "probabilities": {
          "human": 0.9949449896812439,
          "aigc": 0.005055043380707502
        },
        "text": "1.0",
        "title": "第34页-段落110",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1875",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第34页-段落111",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1876",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第34页-段落112",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1877",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9953625202178955,
        "probabilities": {
          "human": 0.9953625202178955,
          "aigc": 0.004637508187443018
        },
        "text": "0.5",
        "title": "第34页-段落113",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1878",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落114",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1879",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落115",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1880",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9527553915977478,
        "probabilities": {
          "human": 0.9527553915977478,
          "aigc": 0.04724462330341339
        },
        "text": "0\n5\n10\n15\n20\n25\n30\nLayer id",
        "title": "第34页-段落116",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1881",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988283514976501,
        "probabilities": {
          "human": 0.9988283514976501,
          "aigc": 0.0011716405861079693
        },
        "text": "(j) K2V8 eo: 0.823",
        "title": "第34页-段落117",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1882",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9988522529602051,
        "probabilities": {
          "human": 0.9988522529602051,
          "aigc": 0.001147791394032538
        },
        "text": "(k) K2V4 eo: 0.837",
        "title": "第34页-段落118",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1883",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9984692931175232,
        "probabilities": {
          "human": 0.9984692931175232,
          "aigc": 0.0015307000139728189
        },
        "text": "(l) KV2 eo: 0.939",
        "title": "第34页-段落119",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1884",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9989849925041199,
        "probabilities": {
          "human": 0.001015037065371871,
          "aigc": 0.9989849925041199
        },
        "text": "Figure 19: Layer-wise attention score ea and relative attention output error eo of per-token-asym KV cache quantization\nwith simulated offline quantization and dequantization (without error accumulation) of the Mistral-7B-Instruct-v0.3 model\nand the first 20 prompts in the 0-shot GSM8K dataset. When the key quantization precision decreases to 2-bit, the layer-wise\nrelative attention output error distribution significantly shifts. Especially, the errors of layer-1, 2, 3, and 4 are significantly\nlarger than other layers.",
        "title": "第34页-段落120",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1885",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9968265295028687,
        "probabilities": {
          "human": 0.9968265295028687,
          "aigc": 0.003173448843881488
        },
        "text": "34",
        "title": "第34页-段落121",
        "page_number": 34,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1886",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6470910906791687,
        "probabilities": {
          "human": 0.3529089391231537,
          "aigc": 0.6470910906791687
        },
        "text": "KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization",
        "title": "第35页-段落1",
        "page_number": 35,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1887",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9324703812599182,
        "probabilities": {
          "human": 0.06752966344356537,
          "aigc": 0.9324703812599182
        },
        "text": "Table 14: KIVI-HQQ KV cache quantization results of different precision and LLM models on the GSM8K few-shot CoTs\nas multiturn conversation dataset.",
        "title": "第35页-段落2",
        "page_number": 35,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1888",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6383638381958008,
        "probabilities": {
          "human": 0.6383638381958008,
          "aigc": 0.3616361618041992
        },
        "text": "Precision\nGSM8K\nAverage\nGSM8K\nAverage\n4-shot\n8-shot\n16-shot\n4-shot\n8-shot\n16-shot\nLlama-3-8B-Instruct\nQwen2.5-7B-Instruct\nBF16\n0.7794\n0.8006\n0.7847\n0.7882\n0.6998\n0.7377\n0.7506\n0.7294\nKV8\n0.7801\n0.8006\n0.7824\n0.7877\n0.6801\n0.7369\n0.7460\n0.7210\nK8V4\n0.7688\n0.7862\n0.7809\n0.7786\n0.6793\n0.724\n0.7468\n0.7167\nK8V2\n0.7566\n0.7763\n0.7642\n0.7657\n0.6801\n0.7491\n0.7437\n0.7243\nK4V8\n0.7445\n0.7695\n0.7498\n0.7546\n0.0076\n0.0038\n0.0053\n0.0056\nKV4\n0.7422\n0.7688\n0.7384\n0.7498\n0.0038\n0.0053\n0.0023\n0.0038\nK4V2\n0.7346\n0.7437\n0.7430\n0.7404\n0.0061\n0.0023\n0.0038\n0.0041\nK2V4\n0.0152\n0.0167\n0.0159\n0.0159\n0.0045\n0.0045\n0.0023\n0.0038\nKV2\n0.0159\n0.0144\n0.0152\n0.0152\n0.0023\n0.0015\n0.003\n0.0023\nMistral-7B-Instruct-v0.3\nQwen2.5-Math-7B-Instruct\nBF16\n0.5019\n0.4890\n0.4973\n0.4961\n0.8901\n0.8666\n0.8658\n0.8742\nKV8\n0.5042\n0.4890\n0.4966\n0.4966\n0.8901\n0.8658\n0.8666\n0.8742\nK8V4\n0.5064\n0.4890\n0.4913\n0.4956\n0.8931\n0.8688\n0.8628\n0.8749\nK8V2\n0.4837\n0.4663\n0.4632\n0.4711\n0.8719\n0.8741\n0.8491\n0.8650\nK4V8\n0.4754\n0.4701\n0.4534\n0.4663\n0.0500\n0.0576\n0.0697\n0.0591\nKV4\n0.4875\n0.4754\n0.4822\n0.4817\n0.0455\n0.0516\n0.0796\n0.0589\nK4V2\n0.4428\n0.4503\n0.4579\n0.4503\n0.0425\n0.0516\n0.0607\n0.0516\nK2V4\n0.0258\n0.0288\n0.0250\n0.0265\n0.0023\n0\n0\n0.0008\nKV2\n0.0190\n0.0220\n0.0208\n0.0206\n0.0023\n0.0008\n0.0015\n0.0015\nQwen2.5-3B-Instruct\nQwen2.5-14B-Instruct\nBF16\n0.5732\n0.5997\n0.6459\n0.6063\n0.7536\n0.7862\n0.8180\n0.7859\nKV8\n0.583\n0.6035\n0.6353\n0.6073\n0.7491\n0.7877\n0.8158\n0.7842\nK8V4\n0.5603\n0.5967\n0.6513\n0.6028\n0.7551\n0.7953\n0.8264\n0.7923\nK8V2\n0.5133\n0.5481\n0.5997\n0.5537\n0.743\n0.7733\n0.8029\n0.7731\nK4V8\n0.5118\n0.5057\n0.5049\n0.5075\n0.7430\n0.7779\n0.7998\n0.7736\nKV4\n0.5080\n0.4845\n0.4837\n0.4921\n0.7339\n0.7908\n0.8112\n0.7786\nK4V2\n0.4587\n0.4124\n0.4170\n0.4294\n0.7475\n0.7733\n0.7953\n0.7720\nK2V4\n0.0083\n0.0061\n0.0136\n0.0093\n0.0220\n0.0144\n0.0174\n0.0179\nKV2\n0.0061\n0.0076\n0.0076\n0.0071\n0.0288\n0.0152\n0.0167\n0.0202\nQwen2.5-3B-Instruct-AWQ\nQwen2.5-32B-Instruct\nBF16\n0.5656\n0.6209\n0.6399\n0.6088\n0.7619\n0.7809\n0.7961\n0.7796\nKV8\n0.5686\n0.6149\n0.6550\n0.6128\n0.7650\n0.7877\n0.8021\n0.7849\nK8V4\n0.5747\n0.608\n0.6406\n0.6078\n0.7726\n0.7801\n0.7998\n0.7842\nK8V2\n0.5466\n0.5694\n0.6149\n0.5770\n0.7384\n0.7703\n0.7877\n0.7655\nK4V8\n0.4845\n0.4564\n0.4443\n0.4617\n0.7597\n0.7794\n0.8135\n0.7842\nKV4\n0.4845\n0.4807\n0.4352\n0.4668\n0.7680\n0.7718\n0.8097\n0.7832\nK4V2\n0.4177\n0.3730\n0.3518\n0.3808\n0.7559\n0.7733\n0.7801\n0.7698\nK2V4\n0.0114\n0.0091\n0.0053\n0.0086\n0.0379\n0.0281\n0.0311\n0.0324\nKV2\n0.0167\n0.0114\n0.0129\n0.0137\n0.0258\n0.0136\n0.0311\n0.0235",
        "title": "第35页-段落3",
        "page_number": 35,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_paper_0_1889",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9955559372901917,
        "probabilities": {
          "human": 0.9955559372901917,
          "aigc": 0.004444067366421223
        },
        "text": "35",
        "title": "第35页-段落4",
        "page_number": 35,
        "source_file": "KVTuner.pdf"
      },
      {
        "item_id": "multi_review_file_0_0",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9684247970581055,
        "probabilities": {
          "human": 0.9684247970581055,
          "aigc": 0.03157522529363632
        },
        "text": "Official Review of Submission11535 by Reviewer fdwh",
        "title": "第1页-段落1",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_1",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999969482421875,
        "probabilities": {
          "human": 0.999969482421875,
          "aigc": 0.000030502025765599683
        },
        "text": "评审人fdwh 对提交11535 的官方评审",
        "title": "第1页-段落2",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_2",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9940162897109985,
        "probabilities": {
          "human": 0.9940162897109985,
          "aigc": 0.005983664654195309
        },
        "text": "Official Reviewby Reviewer fdwh15 Mar 2025, 21:24 (modified: 18 Jun 2025, 17:55)EveryoneRevisions",
        "title": "第1页-段落3",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_3",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985238909721375,
        "probabilities": {
          "human": 0.9985238909721375,
          "aigc": 0.0014761186903342605
        },
        "text": "Summary: 摘要：",
        "title": "第1页-段落4",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_4",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9929115176200867,
        "probabilities": {
          "human": 0.007088476791977882,
          "aigc": 0.9929115176200867
        },
        "text": "The authors propose KVTuner, a sensitivity-aware layer-wise mixed-precision KV cache quantization framework for LLM inference. KVTuner",
        "title": "第1页-段落5",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_5",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9979323148727417,
        "probabilities": {
          "human": 0.0020676711574196815,
          "aigc": 0.9979323148727417
        },
        "text": "addresses key challenges in KV cache quantization, including layer-wise sensitivity to quantization errors, high overhead of fine-grained online",
        "title": "第1页-段落6",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_6",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9898152351379395,
        "probabilities": {
          "human": 0.010184735991060734,
          "aigc": 0.9898152351379395
        },
        "text": "adjustments, and inflexibility across different LLM architectures. Instead of applying uniform quantization across all layers, KVTuner performs an",
        "title": "第1页-段落7",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_7",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9064105153083801,
        "probabilities": {
          "human": 0.09358954429626465,
          "aigc": 0.9064105153083801
        },
        "text": "offline search for optimal layer-wise key and value precision pairs (e.g., K8V4, K4V2) using multi-objective optimization (MOO). This search",
        "title": "第1页-段落8",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_8",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.999514102935791,
        "probabilities": {
          "human": 0.00048585556214675307,
          "aigc": 0.999514102935791
        },
        "text": "considers both memory constraints and model accuracy. The precomputed precision pairs are then applied directly during inference, reducing",
        "title": "第1页-段落9",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_9",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7320606708526611,
        "probabilities": {
          "human": 0.2679392993450165,
          "aigc": 0.7320606708526611
        },
        "text": "computational overhead while maintaining nearly lossless accuracy.",
        "title": "第1页-段落10",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_10",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999746084213257,
        "probabilities": {
          "human": 0.9999746084213257,
          "aigc": 0.000025438323064008728
        },
        "text": "作者提出了KVTuner，一种敏感度感知的层级混合精度KV 缓存量化框架，用于LLM 推断。KVTuner 解决了KV 缓存量化的关键挑战，包括对量化错误",
        "title": "第1页-段落11",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_11",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999949932098389,
        "probabilities": {
          "human": 0.9999949932098389,
          "aigc": 0.00000498575127494405
        },
        "text": "的层级敏感性、高细粒度在线调整的开销，以及不同大型语言模型架构间的灵活性不足。KVTuner 不在所有层间均匀量化，而是通过多目标优化（MOO）进",
        "title": "第1页-段落12",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_12",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999954700469971,
        "probabilities": {
          "human": 0.9999954700469971,
          "aigc": 0.000004478254140849458
        },
        "text": "行离线搜索，寻找最优的层级密钥和值精度对（例如K8V4、K4V2）。该搜索既考虑内存约束，也考虑模型准确性。预先计算好的精度对随后直接应用于推断",
        "title": "第1页-段落13",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_13",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999840259552002,
        "probabilities": {
          "human": 0.9999840259552002,
          "aigc": 0.000016016472727642395
        },
        "text": "过程中，降低计算开销，同时保持几乎无损的准确性。",
        "title": "第1页-段落14",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_14",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9947340488433838,
        "probabilities": {
          "human": 0.9947340488433838,
          "aigc": 0.005265960469841957
        },
        "text": "Claims And Evidence: 主张与证据：",
        "title": "第1页-段落15",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_15",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.985980749130249,
        "probabilities": {
          "human": 0.01401921920478344,
          "aigc": 0.985980749130249
        },
        "text": "The paper claims that KVTuner significantly improves LLM inference efficiency while maintaining accuracy close to full-precision KV caching. As",
        "title": "第1页-段落16",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_16",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.987534761428833,
        "probabilities": {
          "human": 0.012465192936360836,
          "aigc": 0.987534761428833
        },
        "text": "shown in Table 7, KVTuner-C6 achieves a 38.3% throughput improvement compared to KV8, and KVTuner-C3 achieves an even higher 76.4%",
        "title": "第1页-段落17",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_17",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9996123909950256,
        "probabilities": {
          "human": 0.0003876935807056725,
          "aigc": 0.9996123909950256
        },
        "text": "improvement. However, the selection method may introduce additional computational complexity. In lines 275-295, the authors discuss how",
        "title": "第1页-段落18",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_18",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9891419410705566,
        "probabilities": {
          "human": 0.9891419410705566,
          "aigc": 0.010858052410185337
        },
        "text": "KVTuner avoids online decision-making overhead.",
        "title": "第1页-段落19",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_19",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998700618743896,
        "probabilities": {
          "human": 0.9998700618743896,
          "aigc": 0.00012993304699193686
        },
        "text": "论文声称KVTuner 显著提升了LLM 的推理效率，同时保持接近全精度KV 缓存的准确性。如表7 所示，KVTuner-C6 相比KV8 实现了38.3%的吞吐量",
        "title": "第1页-段落20",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_20",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.7516177892684937,
        "probabilities": {
          "human": 0.7516177892684937,
          "aigc": 0.24838216602802277
        },
        "text": "提升，KVTuner-C3 的提升更高，提升了76.4%。然而，选择方法可能会带来额外的计算复杂度。在第275-295 行，作者讨论了KVTuner 如何避免在线决",
        "title": "第1页-段落21",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_21",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9993247985839844,
        "probabilities": {
          "human": 0.9993247985839844,
          "aigc": 0.0006752711487933993
        },
        "text": "策的繁琐负担。",
        "title": "第1页-段落22",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_22",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6911413073539734,
        "probabilities": {
          "human": 0.6911413073539734,
          "aigc": 0.3088586926460266
        },
        "text": "Methods And Evaluation Criteria:",
        "title": "第1页-段落23",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_23",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996558427810669,
        "probabilities": {
          "human": 0.9996558427810669,
          "aigc": 0.0003441618464421481
        },
        "text": "方法与评估标准：",
        "title": "第1页-段落24",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_24",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9989029169082642,
        "probabilities": {
          "human": 0.001097127329558134,
          "aigc": 0.9989029169082642
        },
        "text": "The methodology is well-structured and based on a layer-wise sensitivity analysis of KV cache quantization. The evaluation uses standard",
        "title": "第1页-段落25",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_25",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9952197670936584,
        "probabilities": {
          "human": 0.004780178889632225,
          "aigc": 0.9952197670936584
        },
        "text": "mathematical reasoning benchmarks such as GSM8K and GPQA, which are appropriate for testing the impact of quantization errors. However, as",
        "title": "第1页-段落26",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_26",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9992431402206421,
        "probabilities": {
          "human": 0.0007568738074041903,
          "aigc": 0.9992431402206421
        },
        "text": "noted in lines 220-250, additional profiling of the computational overhead per layer and the impact on inference latency in real-world applications",
        "title": "第1页-段落27",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_27",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.7807769179344177,
        "probabilities": {
          "human": 0.21922311186790466,
          "aigc": 0.7807769179344177
        },
        "text": "(e.g., batched inference on vLLM) would strengthen the claims. A comparison of layer-wise FLOP costs before and after applying KVTuner’s",
        "title": "第1页-段落28",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_28",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9965664148330688,
        "probabilities": {
          "human": 0.0034335858654230833,
          "aigc": 0.9965664148330688
        },
        "text": "selection would provide a clearer picture of its computational efficiency.",
        "title": "第1页-段落29",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_29",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999926090240479,
        "probabilities": {
          "human": 0.9999926090240479,
          "aigc": 0.000007431478934449842
        },
        "text": "该方法结构严谨，基于KV 缓存量化的层级敏感性分析。评估采用标准数学推理基准，如GSM8K 和GPQA，这些标准适用于量化误差的影响测试。然而，",
        "title": "第1页-段落30",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_30",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999963045120239,
        "probabilities": {
          "human": 0.9999963045120239,
          "aigc": 0.0000037181762309046462
        },
        "text": "如第220-250 行所述，进一步分析每层计算开销及其对实际应用推理延迟的影响（如vLLM 上的批量推理）将支持这些主张。在应用KVTuner 选择前后对",
        "title": "第1页-段落31",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_31",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999377727508545,
        "probabilities": {
          "human": 0.9999377727508545,
          "aigc": 0.00006225652759894729
        },
        "text": "比层级FLOP 成本，将更清晰地反映其计算效率。",
        "title": "第1页-段落32",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_32",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9994189739227295,
        "probabilities": {
          "human": 0.9994189739227295,
          "aigc": 0.0005810933653265238
        },
        "text": "Theoretical Claims: 理论主张：",
        "title": "第1页-段落33",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_33",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9989044666290283,
        "probabilities": {
          "human": 0.0010954801691696048,
          "aigc": 0.9989044666290283
        },
        "text": "The paper correctly identifies that key cache quantization errors accumulate across both model layers and generation steps, leading to significant",
        "title": "第1页-段落34",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_34",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9994326233863831,
        "probabilities": {
          "human": 0.0005673354025930166,
          "aigc": 0.9994326233863831
        },
        "text": "degradation in long-context inference. The discussion in lines 330-350 formalizes the optimization problem for selecting layer-wise precision pairs,",
        "title": "第1页-段落35",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_35",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9896752238273621,
        "probabilities": {
          "human": 0.010324745438992977,
          "aigc": 0.9896752238273621
        },
        "text": "but it does not analyze whether the proposed selection strategy guarantees global optimality. Additionally, while KVTuner reduces memory usage,",
        "title": "第1页-段落36",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_36",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8987494111061096,
        "probabilities": {
          "human": 0.10125059634447098,
          "aigc": 0.8987494111061096
        },
        "text": "it does not completely eliminate online computational overhead.",
        "title": "第1页-段落37",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_37",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999926090240479,
        "probabilities": {
          "human": 0.9999926090240479,
          "aigc": 0.0000073579121817601845
        },
        "text": "论文正确指出，关键缓存量化错误会在模型层和生成步骤中积累，导致长上下文推断显著退化。第330-350 行的讨论形式化了选择层次精度对的优化问题，",
        "title": "第1页-段落38",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_38",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999927282333374,
        "probabilities": {
          "human": 0.9999927282333374,
          "aigc": 0.0000072324214670516085
        },
        "text": "但未分析所提选择策略是否保证全局最优性。此外，虽然KVTuner 减少了内存使用，但并未完全消除在线计算开销。",
        "title": "第1页-段落39",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_39",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8269854784011841,
        "probabilities": {
          "human": 0.8269854784011841,
          "aigc": 0.1730145663022995
        },
        "text": "Experimental Designs Or Analyses:",
        "title": "第1页-段落40",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_40",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999920129776001,
        "probabilities": {
          "human": 0.999920129776001,
          "aigc": 0.0000799090412328951
        },
        "text": "实验设计或分析：",
        "title": "第1页-段落41",
        "page_number": 1,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_41",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8441346287727356,
        "probabilities": {
          "human": 0.15586543083190918,
          "aigc": 0.8441346287727356
        },
        "text": "The experiments comprehensively evaluate KVTuner across different models (Llama-3.1-8B, Qwen2.5-7B, Mistral-7B) and various KV precision",
        "title": "第2页-段落1",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_42",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9980084300041199,
        "probabilities": {
          "human": 0.0019915332086384296,
          "aigc": 0.9980084300041199
        },
        "text": "configurations. The results in Table 5 show that KVTuner maintains accuracy while achieving significant memory savings. However, a few aspects",
        "title": "第2页-段落2",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_43",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9431995153427124,
        "probabilities": {
          "human": 0.9431995153427124,
          "aigc": 0.056800488382577896
        },
        "text": "could be further explored.",
        "title": "第2页-段落3",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_44",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999920129776001,
        "probabilities": {
          "human": 0.9999920129776001,
          "aigc": 0.000008013499609660357
        },
        "text": "实验全面评估了不同型号（Llama-3.1-8B、Qwen2.5-7B、Mistral-7B）及多种KV 精密配置的KVTuner。表5 的结果显示，KVTuner 在实现显著内存节",
        "title": "第2页-段落4",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_45",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9711632132530212,
        "probabilities": {
          "human": 0.9711632132530212,
          "aigc": 0.028836766257882118
        },
        "text": "省的同时，保持了准确性。不过，还有一些方面可以进一步探讨。",
        "title": "第2页-段落5",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_46",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9726287722587585,
        "probabilities": {
          "human": 0.9726287722587585,
          "aigc": 0.02737121470272541
        },
        "text": "Supplementary Material: 补充资料：",
        "title": "第2页-段落6",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_47",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.998813271522522,
        "probabilities": {
          "human": 0.001186739420518279,
          "aigc": 0.998813271522522
        },
        "text": "I reviewed the supplementary material, which provides additional ablation studies and sensitivity analysis.",
        "title": "第2页-段落7",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_48",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9967958331108093,
        "probabilities": {
          "human": 0.9967958331108093,
          "aigc": 0.0032041275408118963
        },
        "text": "我查阅了补充材料，其中包含了额外的消融研究和敏感性分析。",
        "title": "第2页-段落8",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_49",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6941882967948914,
        "probabilities": {
          "human": 0.6941882967948914,
          "aigc": 0.30581173300743103
        },
        "text": "Relation To Broader Scientific Literature:",
        "title": "第2页-段落9",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_50",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9985664486885071,
        "probabilities": {
          "human": 0.9985664486885071,
          "aigc": 0.0014335744781419635
        },
        "text": "与更广泛科学文献的关系：",
        "title": "第2页-段落10",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_51",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9991818070411682,
        "probabilities": {
          "human": 0.0008181596640497446,
          "aigc": 0.9991818070411682
        },
        "text": "The paper is well-situated in the literature on KV cache quantization and memory-efficient LLM inference. It correctly cites works on uniform KV",
        "title": "第2页-段落11",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_52",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9981586337089539,
        "probabilities": {
          "human": 0.001841313554905355,
          "aigc": 0.9981586337089539
        },
        "text": "quantization (KV8, KV4) and hybrid eviction strategies. However, as discussed in lines 275-295, it does not sufficiently compare with recent",
        "title": "第2页-段落12",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_53",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9430898427963257,
        "probabilities": {
          "human": 0.056910112500190735,
          "aigc": 0.9430898427963257
        },
        "text": "approaches that integrate quantization with eviction (e.g., SnapKV. A direct comparison would strengthen the positioning of KVTuner as a",
        "title": "第2页-段落13",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_54",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.6079459190368652,
        "probabilities": {
          "human": 0.39205411076545715,
          "aigc": 0.6079459190368652
        },
        "text": "practical alternative to existing methods.",
        "title": "第2页-段落14",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_55",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9848414659500122,
        "probabilities": {
          "human": 0.9848414659500122,
          "aigc": 0.015158522874116898
        },
        "text": "该论文在KV 缓存量化和内存高效LLM 推断的文献中地位良好。它正确引用了关于均匀KV 量化（KV8、KV4）和混合驱逐策略的研究成果。然而，正如第",
        "title": "第2页-段落15",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_56",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999949932098389,
        "probabilities": {
          "human": 0.9999949932098389,
          "aigc": 0.0000049507839321449865
        },
        "text": "275-295 行所讨论的，它与近期将量化与驱逐结合的方法（例如SnapKV）相比，尚不足以实现。直接比较将加强KVTuner 作为现有方法实用替代方案的地",
        "title": "第2页-段落16",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_57",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9485971927642822,
        "probabilities": {
          "human": 0.9485971927642822,
          "aigc": 0.05140279233455658
        },
        "text": "位。",
        "title": "第2页-段落17",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_58",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6214302778244019,
        "probabilities": {
          "human": 0.6214302778244019,
          "aigc": 0.37856969237327576
        },
        "text": "Essential References Not Discussed:",
        "title": "第2页-段落18",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_59",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9970205426216125,
        "probabilities": {
          "human": 0.9970205426216125,
          "aigc": 0.0029793777503073215
        },
        "text": "未被提及的重要参考文献：",
        "title": "第2页-段落19",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_60",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9904322028160095,
        "probabilities": {
          "human": 0.00956779532134533,
          "aigc": 0.9904322028160095
        },
        "text": "The paper does not discuss alternative mixed-precision approaches that incorporate token-importance ranking for KV selection.",
        "title": "第2页-段落20",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_61",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999834299087524,
        "probabilities": {
          "human": 0.9999834299087524,
          "aigc": 0.000016618123481748626
        },
        "text": "本文未讨论将代币重要性排序用于KV 选择的替代混合精度方法。",
        "title": "第2页-段落21",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_62",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9890453815460205,
        "probabilities": {
          "human": 0.9890453815460205,
          "aigc": 0.010954631492495537
        },
        "text": "Other Strengths And Weaknesses:",
        "title": "第2页-段落22",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_63",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9947749376296997,
        "probabilities": {
          "human": 0.9947749376296997,
          "aigc": 0.00522506283596158
        },
        "text": "其他优缺点：",
        "title": "第2页-段落23",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_64",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9987607002258301,
        "probabilities": {
          "human": 0.0012392522767186165,
          "aigc": 0.9987607002258301
        },
        "text": "The paper makes an important contribution to memory-efficient LLM inference with strong empirical results. However, there are areas for",
        "title": "第2页-段落24",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_65",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9893965125083923,
        "probabilities": {
          "human": 0.9893965125083923,
          "aigc": 0.010603529401123524
        },
        "text": "improvement:",
        "title": "第2页-段落25",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_66",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999361038208008,
        "probabilities": {
          "human": 0.9999361038208008,
          "aigc": 0.00006389357440639287
        },
        "text": "本文在内存高效大语言模型推断方面做出了重要贡献，并取得了强有力的实证成果。不过，仍有改进空间：",
        "title": "第2页-段落26",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_67",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.988907516002655,
        "probabilities": {
          "human": 0.988907516002655,
          "aigc": 0.011092400178313255
        },
        "text": "1.",
        "title": "第2页-段落27",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_68",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9947351217269897,
        "probabilities": {
          "human": 0.00526486337184906,
          "aigc": 0.9947351217269897
        },
        "text": "The additional computational cost of computation is not fully analyzed.",
        "title": "第2页-段落28",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_69",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9998224377632141,
        "probabilities": {
          "human": 0.9998224377632141,
          "aigc": 0.0001775528653524816
        },
        "text": "计算过程中额外的计算成本尚未被充分分析。",
        "title": "第2页-段落29",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_70",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9813727140426636,
        "probabilities": {
          "human": 0.9813727140426636,
          "aigc": 0.018627354875206947
        },
        "text": "2.",
        "title": "第2页-段落30",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_71",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9765908718109131,
        "probabilities": {
          "human": 0.9765908718109131,
          "aigc": 0.023409107699990273
        },
        "text": "3.",
        "title": "第2页-段落31",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_72",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9548439979553223,
        "probabilities": {
          "human": 0.04515599086880684,
          "aigc": 0.9548439979553223
        },
        "text": "The practical impact on multi-head attention efficiency is unclear.",
        "title": "第2页-段落32",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_73",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996050000190735,
        "probabilities": {
          "human": 0.9996050000190735,
          "aigc": 0.0003950672398786992
        },
        "text": "对多头注意力效率的实际影响尚不明确。",
        "title": "第2页-段落33",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_74",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.981113076210022,
        "probabilities": {
          "human": 0.981113076210022,
          "aigc": 0.01888689026236534
        },
        "text": "4.",
        "title": "第2页-段落34",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_75",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9820863008499146,
        "probabilities": {
          "human": 0.9820863008499146,
          "aigc": 0.01791374571621418
        },
        "text": "5.",
        "title": "第2页-段落35",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_76",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.5494669079780579,
        "probabilities": {
          "human": 0.5494669079780579,
          "aigc": 0.45053309202194214
        },
        "text": "The method’s effectiveness in extremely long-context settings (e.g., 100K+ tokens) is not evaluated.",
        "title": "第2页-段落36",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_77",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999943733215332,
        "probabilities": {
          "human": 0.999943733215332,
          "aigc": 0.000056226286687888205
        },
        "text": "该方法在极长上下文环境（如100K+令牌）中的有效性未被评估。",
        "title": "第2页-段落37",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_78",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9735731482505798,
        "probabilities": {
          "human": 0.9735731482505798,
          "aigc": 0.02642686851322651
        },
        "text": "6.",
        "title": "第2页-段落38",
        "page_number": 2,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_79",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.6033517122268677,
        "probabilities": {
          "human": 0.6033517122268677,
          "aigc": 0.39664822816848755
        },
        "text": "Other Comments Or Suggestions:",
        "title": "第3页-段落1",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_80",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9880190491676331,
        "probabilities": {
          "human": 0.9880190491676331,
          "aigc": 0.011980974115431309
        },
        "text": "其他评论或建议：",
        "title": "第3页-段落2",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_81",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.8690889477729797,
        "probabilities": {
          "human": 0.13091102242469788,
          "aigc": 0.8690889477729797
        },
        "text": "Including a runtime profiling analysis of KVTuner’s selection method would strengthen claims about efficiency.",
        "title": "第3页-段落3",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_82",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999707937240601,
        "probabilities": {
          "human": 0.9999707937240601,
          "aigc": 0.000029180899218772538
        },
        "text": "包括对KVTuner 选择方法的运行时分析，将加强关于效率的主张。",
        "title": "第3页-段落4",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_83",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9719250202178955,
        "probabilities": {
          "human": 0.9719250202178955,
          "aigc": 0.028075024485588074
        },
        "text": "Questions For Authors: 作者提问：",
        "title": "第3页-段落5",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_84",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.996222972869873,
        "probabilities": {
          "human": 0.0037770443595945835,
          "aigc": 0.996222972869873
        },
        "text": "What is the additional FLOP overhead per generation step compared to traditional KV quantization methods?",
        "title": "第3页-段落6",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_85",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999802112579346,
        "probabilities": {
          "human": 0.9999802112579346,
          "aigc": 0.000019776649423874915
        },
        "text": "与传统KV 量化方法相比，每代代额外的FLOP 开销是多少？",
        "title": "第3页-段落7",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_86",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9172370433807373,
        "probabilities": {
          "human": 0.9172370433807373,
          "aigc": 0.08276288956403732
        },
        "text": "How does KVTuner scale with batch size increases?",
        "title": "第3页-段落8",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_87",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999698400497437,
        "probabilities": {
          "human": 0.9999698400497437,
          "aigc": 0.000030188537493813783
        },
        "text": "随着批次规模的增加，KVTuner 是如何扩展的？",
        "title": "第3页-段落9",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_88",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.996258020401001,
        "probabilities": {
          "human": 0.0037419702857732773,
          "aigc": 0.996258020401001
        },
        "text": "Can KVTuner be integrated with KV cache eviction methods like SnapKV for improved memory efficiency? Have you considered hybrid",
        "title": "第3页-段落10",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_89",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.997480571269989,
        "probabilities": {
          "human": 0.997480571269989,
          "aigc": 0.002519393339753151
        },
        "text": "approaches?",
        "title": "第3页-段落11",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_90",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999289512634277,
        "probabilities": {
          "human": 0.9999289512634277,
          "aigc": 0.00007100016955519095
        },
        "text": "KVTuner 能否与SnapKV 等KV 缓存驱逐方法集成，以提高内存效率？你考虑过混合式教学方法吗？",
        "title": "第3页-段落12",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_91",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9523860812187195,
        "probabilities": {
          "human": 0.9523860812187195,
          "aigc": 0.047613922506570816
        },
        "text": "How does KVTuner handle extreme long-context inference (e.g., 100K+ tokens)? Does performance degrade due to accumulated quantization",
        "title": "第3页-段落13",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_92",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8569043874740601,
        "probabilities": {
          "human": 0.8569043874740601,
          "aigc": 0.14309562742710114
        },
        "text": "errors?",
        "title": "第3页-段落14",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_93",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.999985933303833,
        "probabilities": {
          "human": 0.999985933303833,
          "aigc": 0.000014031516002432909
        },
        "text": "KVTuner 如何处理极端的长上下文推断（例如，100K+ 代币）？性能会因为量化误差积累而下降吗？",
        "title": "第3页-段落15",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_94",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.8778511881828308,
        "probabilities": {
          "human": 0.8778511881828308,
          "aigc": 0.12214884907007217
        },
        "text": "Code Of Conduct: Affirmed.",
        "title": "第3页-段落16",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_95",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9996600151062012,
        "probabilities": {
          "human": 0.9996600151062012,
          "aigc": 0.0003399572742637247
        },
        "text": "行为准则：确认。",
        "title": "第3页-段落17",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_96",
        "is_aigc": true,
        "label_name": "aigc",
        "confidence_score": 0.9955162405967712,
        "probabilities": {
          "human": 0.004483725409954786,
          "aigc": 0.9955162405967712
        },
        "text": "Overall Recommendation: 2: Weak reject (i.e., leaning towards reject, but could also be accepted)",
        "title": "第3页-段落18",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      },
      {
        "item_id": "multi_review_file_0_97",
        "is_aigc": false,
        "label_name": "human",
        "confidence_score": 0.9999855756759644,
        "probabilities": {
          "human": 0.9999855756759644,
          "aigc": 0.000014413439203053713
        },
        "text": "总体建议：2：弱拒绝（即倾向于拒绝，但也可能被接受）",
        "title": "第3页-段落19",
        "page_number": 3,
        "source_file": "kvtuner-review.pdf"
      }
    ]
  },
  "summary": "BERT text classification completed across 1988 text sections"
}