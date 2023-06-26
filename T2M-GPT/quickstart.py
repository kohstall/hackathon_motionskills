import clip
import torch
import numpy as np
import models.vqvae as vqvae
import models.t2m_trans as trans
import warnings


import sys
import time

import options.option_transformer as option_trans

class Model:

    def __init__(self):
        sys.argv = ['GPT_eval_multi.py']
        args = option_trans.get_args_parser()

        args.dataname = 't2m'
        args.resume_pth = 'pretrained/VQVAE/net_last.pth'
        args.resume_trans = 'pretrained/VQTransformer_corruption05/net_best_fid.pth'
        args.down_t = 2
        args.depth = 3
        args.block_size = 51
        warnings.filterwarnings('ignore')

        ## load clip model and datasets
        self.clip_model, self.clip_preprocess = clip.load("ViT-B/32", device=torch.device('cuda'), jit=False, download_root='./')  # Must set jit=False for training
        clip.model.convert_weights(self.clip_model)  # Actually this line is unnecessary since clip by default already on float16
        self.clip_model.eval()
        for p in self.clip_model.parameters():
            p.requires_grad = False

        self.net = vqvae.HumanVQVAE(args, ## use args to define different parameters in different quantizers
                            args.nb_code,
                            args.code_dim,
                            args.output_emb_width,
                            args.down_t,
                            args.stride_t,
                            args.width,
                            args.depth,
                            args.dilation_growth_rate)


        self.trans_encoder = trans.Text2Motion_Transformer(num_vq=args.nb_code, 
                                        embed_dim=1024, 
                                        clip_dim=args.clip_dim, 
                                        block_size=args.block_size, 
                                        num_layers=9, 
                                        n_head=16, 
                                        drop_out_rate=args.drop_out_rate, 
                                        fc_rate=args.ff_rate)


        print ('loading checkpoint from {}'.format(args.resume_pth))
        ckpt = torch.load(args.resume_pth, map_location='cpu')
        self.net.load_state_dict(ckpt['net'], strict=True)
        self.net.eval()
        self.net.cuda()

        print ('loading transformer checkpoint from {}'.format(args.resume_trans))
        ckpt = torch.load(args.resume_trans, map_location='cpu')
        self.trans_encoder.load_state_dict(ckpt['trans'], strict=True)
        self.trans_encoder.eval()
        self.trans_encoder.cuda()

        self.mean = torch.from_numpy(np.load('./checkpoints/t2m/VQVAEV3_CB1024_CMT_H1024_NRES3/meta/mean.npy')).cuda()
        self.std = torch.from_numpy(np.load('./checkpoints/t2m/VQVAEV3_CB1024_CMT_H1024_NRES3/meta/std.npy')).cuda()


    def inference(self, clip_text : [str]):


        start_time = time.time()

        text = clip.tokenize(clip_text, truncate=True).cuda()
        feat_clip_text = self.clip_model.encode_text(text).float()
        index_motion = self.trans_encoder.sample(feat_clip_text[0:1], False)
        pred_pose = self.net.forward_decoder(index_motion)

        from utils.motion_process import recover_from_ric
        pred_xyz = recover_from_ric((pred_pose* self.std+self.mean).float(), 22)
        xyz = pred_xyz.reshape(1, -1, 22, 3)

        np.save('motion.npy', xyz.detach().cpu().numpy())

        import visualization.plot_3d_and_get_arm_coord as plot_3d
        pose_vis, arms_coords = plot_3d.draw_to_batch(xyz.detach().cpu().numpy(),clip_text, ['example.gif']) 

        print(f"{arms_coords=}")
        print(f"Program took {time.time() - start_time} to run")

        return arms_coords


if __name__ == "__main__":
    model = Model()

    # while True:
    #     txt = input("Enter text here: ")

    #     model.inference([txt])

    model.inference(['a person is moving their arm forward'])