"""
Liveness Detection Model - MobileNetV2 Binary Classifier
=========================================================
Model phân loại ảnh khuôn mặt: Real (sống) vs Fake (giả mạo).

Kiến trúc:
  - Backbone: MobileNetV2 pretrained trên ImageNet
  - Classifier head: AdaptiveAvgPool -> Dropout -> FC(1280, 256) -> ReLU -> Dropout -> FC(256, 2)

Output:
  - Class 0: FAKE (ảnh từ màn hình, ảnh in, video replay)
  - Class 1: REAL (khuôn mặt thật trước camera)
"""

import torch
import torch.nn as nn
from torchvision import models


class LivenessDetector(nn.Module):
    """
    CNN phát hiện khuôn mặt giả mạo dựa trên MobileNetV2.

    Transfer learning:
      1. Sử dụng MobileNetV2 pretrained (ImageNet) làm feature extractor
      2. Thay classifier head bằng custom head cho binary classification
      3. Fine-tune từng phần: freeze backbone → train head → unfreeze dần
    """

    def __init__(self, num_classes=2, pretrained=True):
        super().__init__()

        # Load MobileNetV2 pretrained
        if pretrained:
            weights = models.MobileNet_V2_Weights.IMAGENET1K_V1
            self.backbone = models.mobilenet_v2(weights=weights)
        else:
            self.backbone = models.mobilenet_v2(weights=None)

        # Lấy số features từ backbone (thường là 1280 cho MobileNetV2)
        num_features = self.backbone.classifier[1].in_features

        # Thay thế classifier head
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(num_features, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

    def freeze_backbone(self):
        """Đóng băng backbone - chỉ train classifier head."""
        for param in self.backbone.features.parameters():
            param.requires_grad = False
        print("[*] Backbone FROZEN - chỉ train classifier head")

    def unfreeze_backbone(self, from_layer=14):
        """
        Mở đóng băng từ layer chỉ định.
        MobileNetV2 có 19 inverted residual blocks (0-18).
        Mặc định unfreeze từ layer 14 trở đi.
        """
        for i, block in enumerate(self.backbone.features):
            if i >= from_layer:
                for param in block.parameters():
                    param.requires_grad = True
        print(f"[*] Backbone UNFROZEN từ layer {from_layer}")

    def get_trainable_params(self):
        """Đếm số parameters đang trainable."""
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return total, trainable


class LivenessPredictor:
    """
    Wrapper để inference liveness detection.
    Dùng để tích hợp vào server xác thực.
    """

    def __init__(self, model_path, device=None):
        """
        Args:
            model_path: Đường dẫn file .pth đã train
            device: 'cuda' hoặc 'cpu' (tự detect nếu None)
        """
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        # Load model
        self.model = LivenessDetector(num_classes=2, pretrained=False)
        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

        # Transform cho input image
        from torchvision import transforms
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        print(f"[+] Liveness model loaded: {model_path} (device: {self.device})")

    def predict(self, face_image_rgb):
        """
        Dự đoán ảnh khuôn mặt là real hay fake.

        Args:
            face_image_rgb: numpy array (H, W, 3) RGB

        Returns:
            dict: {
                "is_real": bool,
                "confidence": float (0-1),
                "label": "REAL" hoặc "FAKE",
                "scores": {"real": float, "fake": float}
            }
        """
        import torch.nn.functional as F

        # Preprocess
        tensor = self.transform(face_image_rgb)
        tensor = tensor.unsqueeze(0).to(self.device)  # Add batch dim

        # Inference
        with torch.no_grad():
            logits = self.model(tensor)
            probs = F.softmax(logits, dim=1)[0]

        fake_score = probs[0].item()
        real_score = probs[1].item()
        is_real = real_score > fake_score

        return {
            "is_real": is_real,
            "confidence": max(real_score, fake_score),
            "label": "REAL" if is_real else "FAKE",
            "scores": {
                "real": round(real_score, 4),
                "fake": round(fake_score, 4)
            }
        }


if __name__ == "__main__":
    # Quick test: tạo model và in thông tin
    model = LivenessDetector(pretrained=True)
    total, trainable = model.get_trainable_params()
    print(f"Total params:     {total:,}")
    print(f"Trainable params: {trainable:,}")

    model.freeze_backbone()
    total, trainable = model.get_trainable_params()
    print(f"After freeze - Trainable: {trainable:,}")

    model.unfreeze_backbone(from_layer=14)
    total, trainable = model.get_trainable_params()
    print(f"After partial unfreeze - Trainable: {trainable:,}")

    # Test forward pass
    dummy = torch.randn(1, 3, 224, 224)
    output = model(dummy)
    print(f"Output shape: {output.shape}")  # [1, 2]
    print(f"Output: {output}")
