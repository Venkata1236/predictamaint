from typing import Dict

import numpy as np
from loguru import logger
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)


class MaintenanceMetrics:
    """
    Evaluation metrics for predictive maintenance models.
    """

    @staticmethod
    def evaluate_classification(
        y_true: np.ndarray,
        y_prob: np.ndarray,
        threshold: float = 0.5,
    ) -> Dict:
        """
        Evaluate binary classification metrics.
        """

        logger.info(
            "Calculating predictive maintenance metrics"
        )

        y_pred = (
            y_prob >= threshold
        ).astype(int)

        roc_auc = roc_auc_score(
            y_true,
            y_prob,
        )

        precision = precision_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            y_pred,
            zero_division=0,
        )

        accuracy = accuracy_score(
            y_true,
            y_pred,
        )

        conf_matrix = confusion_matrix(
            y_true,
            y_pred,
        )

        precision_curve, recall_curve, _ = (
            precision_recall_curve(
                y_true,
                y_prob,
            )
        )

        pr_auc = auc(
            recall_curve,
            precision_curve,
        )

        tn, fp, fn, tp = (
            conf_matrix.ravel()
        )

        false_alarm_rate = (
            fp / (fp + tn)
            if (fp + tn) > 0
            else 0
        )

        metrics = {
            "roc_auc": round(
                float(roc_auc),
                4,
            ),
            "pr_auc": round(
                float(pr_auc),
                4,
            ),
            "precision": round(
                float(precision),
                4,
            ),
            "recall": round(
                float(recall),
                4,
            ),
            "accuracy": round(
                float(accuracy),
                4,
            ),
            "false_alarm_rate": round(
                float(false_alarm_rate),
                4,
            ),
            "true_positives": int(tp),
            "false_positives": int(fp),
            "true_negatives": int(tn),
            "false_negatives": int(fn),
        }

        logger.info(
            f"Metrics calculated: {metrics}"
        )

        return metrics