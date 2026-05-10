import argparse
from pathlib import Path

import cv2
import numpy as np
import torch
from easydict import EasyDict
from torchvision.utils import make_grid

import configs.coarse_bio_hyper_para
from data.bio_infer_data import BioData
from factory.hp_factory import get_hp
from factory.model_factory import get_model


def get_grid_img(img: torch.Tensor, pred: torch.Tensor, k: float = 0.5) -> np.ndarray:
    pred_255 = (pred >= k) * 255.0
    pred_255 = torch.repeat_interleave(pred_255, repeats=3, dim=0)
    show_list = [img, pred_255]
    grid_img = make_grid(show_list, nrow=2, padding=20, normalize=True, scale_each=True, pad_value=1)
    np_grid_img = grid_img.detach().cpu().numpy().transpose(1, 2, 0)
    return (np_grid_img * 255).astype(np.uint8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Infer a single image with URN")
    parser.add_argument("--checkpoint", required=True, help="Checkpoint path used for inference")
    parser.add_argument("--image", required=True, help="Input image path")
    parser.add_argument("--gpu", type=int, default=0, help="CUDA device index")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold used to binarize the prediction mask")
    parser.add_argument("--output-mask", default=None, help="Optional path to save the predicted probability mask")
    parser.add_argument("--output-grid", default=None, help="Optional path to save a side-by-side image and mask preview")
    return parser.parse_args()


def load_model(checkpoint_path: str, gpu: int, seed: int):
    args = EasyDict({
        "train_set": None,
        "test_set": None,
        "gpu": gpu,
        "seed": seed,
    })
    hp = get_hp(configs.coarse_bio_hyper_para.hp, args)
    torch.cuda.set_device(gpu)
    net = get_model(hp).cuda()
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    net.load_state_dict(checkpoint["model_state_dict"])
    net.eval()
    return net, hp


def infer_single(network, img_path: str, hyper_p, threshold: float):
    bio_data = BioData(img_path)
    data = bio_data.get()
    input_img = torch.unsqueeze(data["img"], dim=0).cuda()

    with torch.no_grad():
        net_out = network(input_img)
        pred_mask = torch.sigmoid(net_out["seg"]).float()[0]
        cls_prob = torch.sigmoid(net_out["cls"]).float().view(-1)[0]

    mask_np = pred_mask.detach().cpu().numpy()
    preview_np = get_grid_img(data["img"], pred_mask, threshold)
    return mask_np, float(cls_prob.detach().cpu()), preview_np


def main() -> int:
    cli_args = parse_args()
    net, hp = load_model(cli_args.checkpoint, cli_args.gpu, cli_args.seed)
    mask_np, cls_prob, preview_np = infer_single(net, cli_args.image, hp, cli_args.threshold)

    print(f"class_probability={cls_prob:.6f}")

    if cli_args.output_mask:
        output_mask = Path(cli_args.output_mask)
        output_mask.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_mask), (mask_np * 255).astype(np.uint8))
        print(f"saved_mask={output_mask}")

    if cli_args.output_grid:
        output_grid = Path(cli_args.output_grid)
        output_grid.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_grid), cv2.cvtColor(preview_np, cv2.COLOR_RGB2BGR))
        print(f"saved_grid={output_grid}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
