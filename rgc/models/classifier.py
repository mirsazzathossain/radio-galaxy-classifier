import pytorch_lightning as pl
import torch
import wandb
from sklearn.metrics import classification_report
from torchmetrics.classification import (
    Accuracy,
    ConfusionMatrix,
    F1Score,
    Precision,
    Recall,
)


class Classifier(pl.LightningModule):
    """
    A PyTorch Lightning module for training and evaluating a vision model.
    """

    def __init__(
        self, model: torch.nn.Module, num_classes: int, learning_rate: float = 1e-3, weight_decay: float = 0.0
    ) -> None:
        """
        Initialize the VisionClassifier.

        :param model: The vision model to be trained.
        :type model: torch.nn.Module
        :param num_classes: Number of classes for classification.
        :type num_classes: int
        :param learning_rate: Learning rate for the optimizer.
        :type learning_rate: float
        :param weight_decay: Weight decay for the optimizer.
        :type weight_decay: float
        """
        super().__init__()
        self.model = model
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.num_classes = num_classes
        self.criterion = torch.nn.CrossEntropyLoss()

        # Metrics
        self.train_accuracy = Accuracy(task="multiclass", num_classes=num_classes)
        self.val_accuracy = Accuracy(task="multiclass", num_classes=num_classes)
        self.test_accuracy = Accuracy(task="multiclass", num_classes=num_classes)

        self.precision = Precision(task="multiclass", num_classes=num_classes)
        self.recall = Recall(task="multiclass", num_classes=num_classes)
        self.f1_score = F1Score(task="multiclass", num_classes=num_classes)
        self.confusion_matrix = ConfusionMatrix(task="multiclass", num_classes=num_classes)

        self.test_outputs = []

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)

        # Log training accuracy
        acc = self.train_accuracy(y_hat, y)
        self.log("train/loss", loss, on_step=True, on_epoch=True, prog_bar=True, logger=True)
        self.log("train/acc", acc, on_step=True, on_epoch=True, prog_bar=True, logger=True)

        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)

        # Log validation accuracy and other metrics
        acc = self.val_accuracy(y_hat, y)
        prec = self.precision(y_hat, y)
        rec = self.recall(y_hat, y)
        f1 = self.f1_score(y_hat, y)

        self.log("val/loss", loss, on_epoch=True, logger=True)
        self.log("val/acc", acc, on_epoch=True, prog_bar=True, logger=True)
        self.log("val/precision", prec, on_epoch=True, logger=True)
        self.log("val/recall", rec, on_epoch=True, logger=True)
        self.log("val/f1_score", f1, on_epoch=True, logger=True)

        return loss

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = self.criterion(y_hat, y)

        # Store test outputs for logging at the end of the epoch
        self.test_outputs.append({"y_hat": y_hat, "y": y})

        return loss

    def on_test_epoch_end(self):
        # Combine outputs from the test step
        y_hats = torch.cat([output["y_hat"] for output in self.test_outputs], dim=0)
        y_true = torch.cat([output["y"] for output in self.test_outputs], dim=0)

        # Compute aggregated metrics
        acc = self.test_accuracy(y_hats, y_true)
        precision = self.precision(y_hats, y_true)
        recall = self.recall(y_hats, y_true)
        f1 = self.f1_score(y_hats, y_true)

        # Log these metrics for reporting
        self.log("test/acc", acc, on_epoch=True, logger=True)
        self.log("test/precision", precision, on_epoch=True, logger=True)
        self.log("test/recall", recall, on_epoch=True, logger=True)
        self.log("test/f1_score", f1, on_epoch=True, logger=True)

        # Calculate and log class-wise metrics
        y_true_np = y_true.cpu().numpy()
        y_hats_np = torch.argmax(y_hats, dim=1).cpu().numpy()
        report = classification_report(
            y_true_np,
            y_hats_np,
            target_names=[str(i) for i in range(self.num_classes)],
            zero_division=0,
        )

        # Log the classification report
        self.logger.experiment.log({"classification_report": wandb.Html(f"<pre>{report}</pre>")})

        # Log confusion matrix if needed for visualization in the paper
        self.logger.experiment.log({
            "confusion_matrix": wandb.plot.confusion_matrix(
                probs=None,
                y_true=y_true.cpu().numpy(),
                preds=torch.argmax(y_hats, dim=1).cpu().numpy(),
                class_names=[str(i) for i in range(self.num_classes)],
            )
        })

        # Save the test probabilities as a tensor file
        test_output = torch.cat([output["y_hat"] for output in self.test_outputs], dim=0)
        torch.save(test_output, "test_output.pt")

        # Log the saved file to W&B
        artifact = wandb.Artifact("test_output", type="dataset", description="Test output probabilities")
        artifact.add_file("test_output.pt")
        self.logger.experiment.log_artifact(artifact)

    def configure_optimizers(self):
        if self.model.__class__.__name__ in ["SwinTransformer", "VisionTransformer"]:
            optimizer = torch.optim.AdamW(self.parameters(), lr=self.learning_rate)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=5, eta_min=0)
        elif self.model.__class__.__name__ == "DSteerableLeNet":
            optimizer = torch.optim.AdamW(self.parameters(), lr=self.learning_rate, weight_decay=self.weight_decay)
            scheduler = {
                "scheduler": torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", patience=2, factor=0.9),
                "monitor": "train/loss",
                "interval": "epoch",
                "frequency": 1,
                "strict": True,
            }
        else:
            optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
            scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

        return [optimizer], [scheduler]
