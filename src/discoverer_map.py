from typing import Tuple

import cv2
import numpy as np
import torch


class DiscovererMap:
    def __init__(self):
        self.map = {}
        self.continue_discovery = True
        self.model_type = "MiDaS_small"

        self.midas = torch.hub.load("intel-isl/MiDaS", self.model_type)

        self.device = (
            torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
        self.midas.to(self.device)
        self.midas.eval()

        self.midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if self.model_type == "DPT_Large" or self.model_type == "DPT_Hybrid":
            self.transform = self.midas_transforms.dpt_transform
        else:
            self.transform = self.midas_transforms.small_transform

    def transform_depth_map(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        input_batch = self.transform(img).to(self.device)

        with torch.no_grad():
            prediction = self.midas(input_batch)

            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()

        depth_map = prediction.cpu().numpy()

        depth_map = cv2.normalize(
            depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_64F
        )

        depth_map = (depth_map * 255).astype(np.uint8)
        depth_map = cv2.applyColorMap(depth_map, cv2.COLORMAP_MAGMA)
        return depth_map

    @staticmethod
    def get_point_depth(depth_map: cv2.typing.MatLike) -> Tuple[int, int]:
        return (
            np.unravel_index(np.argmin(depth_map, axis=None), depth_map.shape)[1],
            np.unravel_index(np.argmin(depth_map, axis=None), depth_map.shape)[0],
        )
