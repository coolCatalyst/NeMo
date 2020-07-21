# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
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


from unittest import TestCase

import pytest
import torch
from sklearn.metrics import precision_recall_fscore_support

from nemo.collections.nlp.metrics.classification_report import ClassificationReport


class ClassificationReportTests(TestCase):
    num_classes = 3
    label_ids = {'a': 0, 'b': 1, 'c': 2}

    @pytest.mark.unit
    def test_classification_report(self):
        classification_report_nemo = ClassificationReport(num_classes=self.num_classes, label_ids=self.label_ids)

        preds = torch.Tensor([0, 1, 1, 1, 2, 2, 0])
        labels = torch.Tensor([1, 0, 0, 1, 2, 1, 0])

        tp, fp, fn = classification_report_nemo(preds, labels)

        def __convert_to_tensor(sklearn_metric):
            return torch.Tensor([round(sklearn_metric * 100)])[0]

        for mode in ['macro', 'micro', 'weighted']:

            precision, recall, f1 = classification_report_nemo.get_precision_recall_f1(tp, fn, fp, mode)
            pr_sklearn, recall_sklearn, f1_sklearn, _ = precision_recall_fscore_support(labels, preds, average=mode)

            self.assertEqual(torch.round(precision), __convert_to_tensor(pr_sklearn), f'wrong precision for {mode}')
            self.assertEqual(torch.round(recall), __convert_to_tensor(recall_sklearn), f'wrong recall for {mode}')
            self.assertEqual(torch.round(f1), __convert_to_tensor(f1_sklearn), f'wrong f1 for {mode}')
