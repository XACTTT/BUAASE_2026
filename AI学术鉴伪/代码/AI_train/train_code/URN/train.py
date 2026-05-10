import argparse
import os
import time
import configs.coarse_bio_hyper_para
import configs.fine_bce_bio_hyper_para
import torch

from eval import eval_after_train
from factory.bio_data_factory import get_data, get_dataloader
from factory.hp_factory import get_hp
from factory.model_factory import get_model
from factory.optim_factory import get_optimizer
import tqdm
from easydict import EasyDict

from step import predict


def train_net(net, hp=None, config=None):
    """
    Train our network
    :param net: network to be trained
    :param hp: hyperparameter
    :param config: config file path
    """
    # Choose dataset
    if config is None:
        config = EasyDict()
    if hp is None:
        hp = EasyDict()
    train_loader = get_data(hp, config, 'train')
    test_loaders = get_data(hp, config, 'test')

    # Choose optimizer
    optimizer = get_optimizer(hp, net)

    # Generate log dir
    if not os.path.exists(config.logs_dir):
        os.makedirs(config.logs_dir)

    # Initialize metrics
    torch.cuda.empty_cache()
    current_loss = 1e9
    t_epoch = tqdm.trange(hp.train.epochs)

    # Start to train
    for epoch in t_epoch:
        t_epoch.set_description(f"Epoch, loss={current_loss}")
        t_epoch.refresh()
        time.sleep(0.01)
        epoch_loss, epoch_seg_loss, epoch_cls_loss = 0, 0, 0

        # Begin to step
        for idx, batch in enumerate(train_loader):
            optimizer.zero_grad()
            net.train()
            # Train on a batch
            loss_dict = predict(net, batch, hp)
            epoch_loss = epoch_loss + loss_dict['batch_loss'].item()
            loss_dict['batch_loss'].backward()
            optimizer.step()

        current_loss = epoch_loss / (idx + 1)

        # Save checkpoints
        if config.save_checkpoint and (epoch + 1) % config.checkpoint_epochs == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': net.state_dict(),
                'optimizer_state_dict': optimizer.state_dict()
            }, f'{config.logs_dir}/checkpoint_{str(epoch)}.pkl')

    eval_after_train(net, test_loaders, hp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train URN on a manifest-based dataset")
    parser.add_argument("--train-set", default=None, help="Train manifest name without .txt suffix")
    parser.add_argument("--test-set", default=None, help="Test manifest name without .txt suffix")
    parser.add_argument("--gpu", type=int, default=0, help="CUDA device index")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--epochs", type=int, default=None, help="Override training epochs")
    parser.add_argument("--batch-size", type=int, default=None, help="Override training batch size")
    parser.add_argument("--checkpoint-dir", default=None, help="Directory used to save checkpoints and logs")
    parser.add_argument("--smoke-test", action="store_true", help="Load one train batch and one test batch, then exit")
    cli_args = parser.parse_args()

    args = EasyDict({
        "train_set": cli_args.train_set,
        "test_set": cli_args.test_set,
        "gpu": cli_args.gpu,
        "seed": cli_args.seed,
    })
    hp = get_hp(configs.coarse_bio_hyper_para.hp, args)
    from configs.config import config_dict as config

    if cli_args.epochs is not None:
        hp.train.epochs = cli_args.epochs
    if cli_args.batch_size is not None:
        hp.train.batch_size = cli_args.batch_size
    if cli_args.checkpoint_dir is not None:
        config.logs_dir = os.path.abspath(cli_args.checkpoint_dir)

    torch.cuda.set_device(args.gpu)
    net = get_model(hp).cuda()

    if cli_args.smoke_test:
        train_loader = get_data(hp, config, 'train')
        test_loader = get_data(hp, config, 'test')
        train_batch = next(iter(train_loader))
        test_batch = next(iter(test_loader))
        train_out = predict(net, train_batch, hp)
        print(
            f"Smoke test passed. train_batch={train_batch['img'].shape}, "
            f"test_batch={test_batch['img'].shape}, "
            f"train_loss={float(train_out['batch_loss'].detach().cpu()):.6f}"
        )
    else:
        train_net(net, hp, config)
