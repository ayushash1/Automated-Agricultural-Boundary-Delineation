import torch
import torch.nn as nn

class ResBlock(nn.Module):
    def __init__(self, n_feats, kernel_size, bn=False, act=nn.ReLU(True), res_scale=1):
        super(ResBlock, self).__init__()
        m = []
        for i in range(2):
            m.append(nn.Conv2d(n_feats, n_feats, kernel_size, padding=kernel_size//2))
            if bn: m.append(nn.BatchNorm2d(n_feats))
            if i == 0: m.append(act)

        self.body = nn.Sequential(*m)
        self.res_scale = res_scale

    def forward(self, x):
        res = self.body(x).mul(self.res_scale)
        return x + res

class Upsampler(nn.Sequential):
    def __init__(self, conv, scale, n_feats, bn=False, act=False):
        m = []
        if (scale & (scale - 1)) == 0:    # Is scale power of 2?
            for _ in range(int(torch.log2(torch.tensor(scale)))):
                m.append(conv(n_feats, 4 * n_feats, 3, padding=1))
                m.append(nn.PixelShuffle(2))
                if bn: m.append(nn.BatchNorm2d(n_feats))
                if act: m.append(act)
        elif scale == 3:
            m.append(conv(n_feats, 9 * n_feats, 3, padding=1))
            m.append(nn.PixelShuffle(3))
            if bn: m.append(nn.BatchNorm2d(n_feats))
            if act: m.append(act)
        else:
            raise NotImplementedError

        super(Upsampler, self).__init__(*m)

class EDSR(nn.Module):
    def __init__(self, n_resblocks=16, n_feats=64, n_colors=3, scale=4, conv=nn.Conv2d):
        super(EDSR, self).__init__()
        
        kernel_size = 3
        act = nn.ReLU(True)
        
        self.sub_mean = MeanShift(255)
        self.add_mean = MeanShift(255, sign=1)

        # define head module
        m_head = [conv(n_colors, n_feats, kernel_size, padding=kernel_size//2)]

        # define body module
        m_body = [
            ResBlock(n_feats, kernel_size, res_scale=0.1, act=act) for _ in range(n_resblocks)
        ]
        m_body.append(conv(n_feats, n_feats, kernel_size, padding=kernel_size//2))

        # define tail module
        m_tail = [
            Upsampler(conv, scale, n_feats, act=False),
            conv(n_feats, n_colors, kernel_size, padding=kernel_size//2)
        ]

        self.head = nn.Sequential(*m_head)
        self.body = nn.Sequential(*m_body)
        self.tail = nn.Sequential(*m_tail)

    def forward(self, x):
        # x = self.sub_mean(x)
        x = self.head(x)
        res = self.body(x)
        res += x
        x = self.tail(res)
        # x = self.add_mean(x)
        return x

class MeanShift(nn.Conv2d):
    def __init__(self, rgb_range, rgb_mean=(0.4488, 0.4371, 0.4040), rgb_std=(1.0, 1.0, 1.0), sign=-1):
        super(MeanShift, self).__init__(3, 3, kernel_size=1)
        std = torch.Tensor(rgb_std)
        self.weight.data = torch.eye(3).view(3, 3, 1, 1) / std.view(3, 1, 1, 1)
        self.bias.data = sign * rgb_range * torch.Tensor(rgb_mean) / std
        for p in self.parameters():
            p.requires_grad = False
