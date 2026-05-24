"""
Training Script - Huấn luyện Liveness Detection Model
=======================================================
Script huấn luyện MobileNetV2 để phân loại Real vs Fake face.

Pipeline:
  1. Load dataset từ defender/dataset/{real, fake}
  2. Data augmentation (flip, rotation, color jitter, ...)
  3. Phase 1: Freeze backbone → train classifier head (10 epochs)
  4. Phase 2: Unfreeze last layers → fine-tune (15 epochs)
  5. Evaluate trên test set
  6. Export model → liveness_model.pth

Cách sử dụng:
  python train_liveness.py                     # Train mặc định
  python train_liveness.py --epochs1 15 --epochs2 20  # Custom epochs
  python train_liveness.py --evaluate model.pth       # Chỉ evaluate
"""

import os
import sys
import argparse
import time
from datetime import datetime

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision import transforms, datasets

from liveness_model import LivenessDetector


class TransformedSubset(torch.utils.data.Dataset):
    """Wrapper để áp dụng transform khác nhau cho train/val subset.
    Định nghĩa ở module level để có thể pickle trên Windows."""
    def __init__(self, subset, transform):
        self.subset = subset
        self.transform = transform

    def __getitem__(self, idx):
        img, label = self.subset[idx]
        return self.transform(img), label

    def __len__(self):
        return len(self.subset)


# Đường dẫn
DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
MODEL_PATH = os.path.join(OUTPUT_DIR, "liveness_model.pth")


def get_data_transforms():
    """Định nghĩa data augmentation cho training và validation."""
    train_transform = transforms.Compose([
        transforms.Resize((240, 240)),
        transforms.RandomCrop(224),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.1),
        transforms.RandomGrayscale(p=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
        transforms.RandomErasing(p=0.1),
    ])

    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    return train_transform, val_transform


def load_dataset(train_transform, val_transform, val_ratio=0.2):
    """Load dataset và split train/val."""
    # ImageFolder: mỗi subfolder là 1 class
    # dataset/fake/ -> class 0, dataset/real/ -> class 1
    full_dataset = datasets.ImageFolder(DATASET_DIR)

    # Split
    total = len(full_dataset)
    val_size = int(total * val_ratio)
    train_size = total - val_size

    train_subset, val_subset = random_split(
        full_dataset, [train_size, val_size],
        generator=torch.Generator().manual_seed(42)
    )

    # Áp dụng transform khác nhau cho train và val
    train_dataset = TransformedSubset(train_subset, train_transform)
    val_dataset = TransformedSubset(val_subset, val_transform)

    print(f"[*] Dataset loaded:")
    print(f"    Classes: {full_dataset.classes}")
    print(f"    Class->Idx: {full_dataset.class_to_idx}")
    print(f"    Total: {total} | Train: {train_size} | Val: {val_size}")

    return train_dataset, val_dataset, full_dataset.classes


def train_one_epoch(model, dataloader, criterion, optimizer, device):
    """Train 1 epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, labels) in enumerate(dataloader):
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    val_loss = running_loss / total
    val_acc = correct / total
    return val_loss, val_acc, np.array(all_preds), np.array(all_labels)


def plot_training_history(history, save_path):
    """Vẽ biểu đồ training history."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss
    ax1.plot(history['train_loss'], label='Train Loss', color='blue')
    ax1.plot(history['val_loss'], label='Val Loss', color='red')
    ax1.set_title('Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Accuracy
    ax2.plot(history['train_acc'], label='Train Acc', color='blue')
    ax2.plot(history['val_acc'], label='Val Acc', color='red')
    ax2.set_title('Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[+] Training history saved: {save_path}")


def plot_confusion_matrix(preds, labels, classes, save_path):
    """Vẽ confusion matrix."""
    from sklearn.metrics import confusion_matrix, classification_report

    cm = confusion_matrix(labels, preds)
    print("\n=== CLASSIFICATION REPORT ===")
    print(classification_report(labels, preds, target_names=classes))

    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=range(len(classes)), yticks=range(len(classes)),
           xticklabels=classes, yticklabels=classes,
           ylabel='Actual', xlabel='Predicted',
           title='Confusion Matrix')

    # Hiển thị số trong mỗi ô
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]),
                    ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black",
                    fontsize=14)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[+] Confusion matrix saved: {save_path}")


def train(args):
    """Main training pipeline."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Device: {device}")
    if device.type == "cuda":
        print(f"    GPU: {torch.cuda.get_device_name(0)}")

    # Data
    train_transform, val_transform = get_data_transforms()
    train_dataset, val_dataset, classes = load_dataset(
        train_transform, val_transform
    )

    train_loader = DataLoader(
        train_dataset, batch_size=args.batch_size,
        shuffle=True, num_workers=0, pin_memory=False
    )
    val_loader = DataLoader(
        val_dataset, batch_size=args.batch_size,
        shuffle=False, num_workers=0, pin_memory=False
    )

    # Model
    model = LivenessDetector(num_classes=2, pretrained=True)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    best_val_acc = 0.0

    # ====== PHASE 1: Train classifier head (backbone frozen) ======
    print("\n" + "=" * 60)
    print("  PHASE 1: Train classifier head (backbone frozen)")
    print("=" * 60)

    model.freeze_backbone()
    total, trainable = model.get_trainable_params()
    print(f"  Trainable: {trainable:,} / {total:,} params")

    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr1, weight_decay=1e-4
    )
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)

    for epoch in range(args.epochs1):
        start = time.time()
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device
        )
        val_loss, val_acc, _, _ = validate(model, val_loader, criterion, device)
        scheduler.step()
        elapsed = time.time() - start

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print(f"  Epoch {epoch+1:2d}/{args.epochs1} | "
              f"Train: loss={train_loss:.4f} acc={train_acc:.4f} | "
              f"Val: loss={val_loss:.4f} acc={val_acc:.4f} | "
              f"Time: {elapsed:.1f}s")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"    -> Best model saved! (val_acc: {val_acc:.4f})")

    # ====== PHASE 2: Fine-tune (partially unfrozen) ======
    print("\n" + "=" * 60)
    print("  PHASE 2: Fine-tune (unfreeze last layers)")
    print("=" * 60)

    model.unfreeze_backbone(from_layer=14)
    total, trainable = model.get_trainable_params()
    print(f"  Trainable: {trainable:,} / {total:,} params")

    optimizer = optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr2, weight_decay=1e-4
    )
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs2)

    for epoch in range(args.epochs2):
        start = time.time()
        train_loss, train_acc = train_one_epoch(
            model, train_loader, criterion, optimizer, device
        )
        val_loss, val_acc, preds, labels = validate(
            model, val_loader, criterion, device
        )
        scheduler.step()
        elapsed = time.time() - start

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        total_epoch = args.epochs1 + epoch + 1
        print(f"  Epoch {total_epoch:2d}/{args.epochs1 + args.epochs2} | "
              f"Train: loss={train_loss:.4f} acc={train_acc:.4f} | "
              f"Val: loss={val_loss:.4f} acc={val_acc:.4f} | "
              f"Time: {elapsed:.1f}s")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), MODEL_PATH)
            print(f"    -> Best model saved! (val_acc: {val_acc:.4f})")

    # ====== Final Evaluation ======
    print("\n" + "=" * 60)
    print("  FINAL EVALUATION")
    print("=" * 60)

    # Load best model
    model.load_state_dict(
        torch.load(MODEL_PATH, map_location=device, weights_only=True)
    )
    val_loss, val_acc, preds, labels = validate(
        model, val_loader, criterion, device
    )
    print(f"  Best val accuracy: {best_val_acc:.4f}")

    # Plot
    plot_training_history(history, os.path.join(OUTPUT_DIR, "training_history.png"))
    plot_confusion_matrix(preds, labels, classes, os.path.join(OUTPUT_DIR, "confusion_matrix.png"))

    print(f"\n[+] Model saved: {MODEL_PATH}")
    print(f"[*] Để tích hợp vào server, copy model vào server/ và chạy app_secured.py")


def evaluate_model(model_path):
    """Evaluate model đã train trên toàn bộ dataset."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    _, val_transform = get_data_transforms()
    dataset = datasets.ImageFolder(DATASET_DIR, transform=val_transform)
    loader = DataLoader(dataset, batch_size=32, shuffle=False)

    model = LivenessDetector(num_classes=2, pretrained=False)
    model.load_state_dict(
        torch.load(model_path, map_location=device, weights_only=True)
    )
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    val_loss, val_acc, preds, labels = validate(model, loader, criterion, device)

    print(f"Accuracy: {val_acc:.4f}")
    plot_confusion_matrix(preds, labels, dataset.classes,
                          os.path.join(OUTPUT_DIR, "eval_confusion_matrix.png"))


def main():
    parser = argparse.ArgumentParser(
        description="Train Liveness Detection Model"
    )
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs1", type=int, default=10,
                        help="Epochs cho Phase 1 (frozen backbone)")
    parser.add_argument("--epochs2", type=int, default=15,
                        help="Epochs cho Phase 2 (fine-tune)")
    parser.add_argument("--lr1", type=float, default=1e-3,
                        help="Learning rate Phase 1")
    parser.add_argument("--lr2", type=float, default=1e-4,
                        help="Learning rate Phase 2")
    parser.add_argument("--evaluate", type=str, default=None,
                        help="Chỉ evaluate model (đường dẫn .pth)")

    args = parser.parse_args()

    if args.evaluate:
        evaluate_model(args.evaluate)
    else:
        # Kiểm tra dataset
        if not os.path.exists(DATASET_DIR):
            print("[!] Chưa có dataset!")
            print("[*] Chạy: python create_dataset.py --class real --num 200")
            print("[*] Rồi:  python create_dataset.py --class fake --num 200")
            sys.exit(1)

        real_dir = os.path.join(DATASET_DIR, "real")
        fake_dir = os.path.join(DATASET_DIR, "fake")

        if not os.path.exists(real_dir) or not os.path.exists(fake_dir):
            print("[!] Thiếu thư mục real/ hoặc fake/ trong dataset!")
            sys.exit(1)

        real_count = len(os.listdir(real_dir))
        fake_count = len(os.listdir(fake_dir))

        if real_count < 10 or fake_count < 10:
            print(f"[!] Dataset quá nhỏ: real={real_count}, fake={fake_count}")
            print("[*] Nên có ít nhất 100 ảnh mỗi class.")
            sys.exit(1)

        train(args)


if __name__ == "__main__":
    main()
