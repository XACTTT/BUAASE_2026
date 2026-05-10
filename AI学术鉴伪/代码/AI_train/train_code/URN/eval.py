import argparse

import torch
import tqdm
from easydict import EasyDict

import configs.coarse_bio_hyper_para
from factory.bio_data_factory import get_data
from factory.hp_factory import get_hp
from factory.model_factory import get_model
from utils.metric_collector import MetricCollector


def get_model_device(network: torch.nn.Module) -> torch.device:
    return next(network.parameters()).device

def eval_after_train(network, data_loader, hyper_p, k=0.5):
    """
    Calculate metric values
    :param network: Network to use
    :param data_loader: Dataloader of test dataset
    :param hyper_p: Hyper parameters
    :param k: Threshold for calculating the metrics
    :return: Pixel-level and image-level metrics
    """
    metric_values = MetricCollector()
    device = get_model_device(network)
    # Stop gradients
    network.eval()
    with torch.no_grad():
        for idx, batch in enumerate(tqdm.tqdm(data_loader)):
            # Feed a batch to the network
            batch_img = batch['img'].to(device, non_blocking=True)
            batch_mask = batch['mask'].to(device, non_blocking=True)
            batch_cls = batch['cls'].to(device, non_blocking=True)
            net_out = network(batch_img)
            # Update pixel-level metrics
            if hyper_p.loss.seg.enable:
                main_pred_flat = torch.sigmoid(net_out['seg']).float().view(-1)
                main_true_flat = batch_mask.float().view(-1)
                metric_values.update(main_pred_flat, main_true_flat, data_loader.batch_size, 'seg', k)

            # Update image-level metrics
            if hyper_p.loss.cls.enable:
                cls_pred_flat = torch.sigmoid(net_out['cls']).float().view(-1)
                cls_true_flat = batch_cls.float().view(-1)
                metric_values.update(cls_pred_flat, cls_true_flat, data_loader.batch_size, 'cls', k)

    # Output metric values
    seg_res = metric_values.show('seg')
    print(metric_values.metrics.seg.f1_seg.avg, metric_values.metrics.seg.mcc_seg.avg)

    cls_res = metric_values.show('cls')
    print(metric_values.metrics.cls.auc_cls.avg, metric_values.metrics.cls.acc_cls.avg)
    print('\n')

    return seg_res, cls_res


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate URN on a manifest-based dataset")
    parser.add_argument("--checkpoint", required=True, help="Checkpoint path to evaluate")
    parser.add_argument("--test-set", default=None, help="Test manifest name without .txt suffix")
    parser.add_argument("--gpu", type=int, default=0, help="CUDA device index")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold used for binary metrics")
    return parser.parse_args()


if __name__ == '__main__':
    cli_args = parse_args()
    args = EasyDict({
        "train_set": None,
        "test_set": cli_args.test_set,
        "gpu": cli_args.gpu,
        "seed": cli_args.seed,
    })
    hp = get_hp(configs.coarse_bio_hyper_para.hp, args)
    torch.cuda.set_device(cli_args.gpu)
    net = get_model(hp).cuda()
    checkpoint = torch.load(cli_args.checkpoint, map_location="cpu", weights_only=True)
    net.load_state_dict(checkpoint['model_state_dict'])
    from configs.config import config_dict as config

    test_loaders = get_data(hp, config, 'test')
    eval_after_train(net, test_loaders, hp, k=cli_args.threshold)
