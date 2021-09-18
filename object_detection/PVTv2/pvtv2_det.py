#   Copyright (c) 2021 PPViT Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PVTv2 Object Detection"""

import paddle
import paddle.nn as nn
from config import get_config
from pvtv2_backbone import build_pvtv2

# from det_necks.fpn import FPN, LastLevelMaxPool, TopFeatP6P7
from det_heads.maskrcnn_head.rpn_head import RPNHead
from det_heads.maskrcnn_head.roi_head import RoIHead
from det_heads.retinanet_head.retinanet_head import RetinaNetHead
cfg = get_config()

# class PVTv2Det(nn.Layer):
#     def __init__(self, config):
#         super().__init__()
#         self.backbone = build_pvtv2(config)
#         self.neck = FPN(
#             in_channels=config.FPN.IN_CHANNELS,
#             out_channel=config.FPN.OUT_CHANNELS,
#             strides=config.FPN.STRIDES,
#             use_c5=config.FPN.USE_C5,
#             top_block=LastLevelMaxPool(),
#             use_bias=True
#         )
#         self.rpnhead = RPNHead(config)
#         self.roihead = RoIHead(config)

#         self.config = config
    
#     def forward(self, x, gt=None):
#         feats = self.neck(self.backbone(x.tensors))
#         rpn_out = self.rpnhead(feats, gt)

#         if self.training and self.config.ROI.PAT_GT_AS_PRO:
#             proposals = []
#             for proposal, gt_box in zip(rpn_out[0], gt["gt_boxes"]):
#                 proposals.append(paddle.concat([proposal, gt_box]))
#         else:
#             proposals = rpn_out[0]

#         final_out = self.roihead(feats, proposals, gt)
#         #print('final_out:', final_out)

#         if self.training:
#             rpn_losses = rpn_out[2]
#             # if training, final_out returns losses, now we combine the losses dicts
#             final_out.update(rpn_losses)

#         return final_out


class PVTv2Det(nn.Layer):
    def __init__(self, config):
        super().__init__()
        self.backbone = build_pvtv2(config)
        self.neck = FPN(
            in_channels=config.FPN.IN_CHANNELS,
            out_channel=config.FPN.OUT_CHANNELS,
            strides=config.FPN.STRIDES,
            use_c5=config.FPN.USE_C5,
            top_block=TopFeatP6P7(config.FPN.IN_CHANNELS[-1], config.FPN.OUT_CHANNELS),
            use_bias=True
        )
        self.retinahead = RetinaNetHead(config)
        self.config = config
    
    def forward(self, x, gt=None):
        feats = self.neck(self.backbone(x.tensors))
        head_out = self.retinahead(feats, gt)

        return head_out

def build_pvtv2_det(config):
    model = PVTv2Det(config)
    return model

