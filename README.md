---
license: cc-by-sa-4.0
library_name: transformers
pipeline_tag: image-classification
base_model: facebook/dinov2-small
datasets:
- mohanty/PlantVillage
tags:
- agriculture
- plant-disease
- computer-vision
- dinov2
- image-classification
metrics:
- accuracy
- f1
model-index:
- name: plant-disease-dinov2-small
  results:
  - task:
      type: image-classification
      name: Plant disease classification (38 classes)
    dataset:
      name: PlantVillage (colour), leaf-level held-out split
      type: mohanty/PlantVillage
    metrics:
    - type: accuracy
      value: 0.9886
      name: Accuracy (unseen leaves)
    - type: f1
      value: 0.9849
      name: Macro F1 (unseen leaves)
---

# Plant Disease Classifier (DINOv2-small + linear head)

Identifies **38 crop–condition classes** (26 diseases and 12 healthy classes across 14 crops)
from a photo of a single leaf. Built as the open disease-scanning model for
[BloomTech](https://github.com/itsRou/bloomtech-smart-agriculture), my AI + IoT smart-agriculture
graduation project.

**Try it:** [Plant Disease Scanner Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner)

| Metric (held-out test set, 10,862 photos) | Value |
|---|---|
| Accuracy on **leaves never seen in training** | **98.9%** |
| Macro F1 on leaves never seen in training | **98.5%** |
| Accuracy with a naive photo-level random split (for comparison) | 99.1% |

## Why "leaves never seen in training" matters

PlantVillage contains several photos of the **same physical leaf**. If photos are split
randomly, near-duplicates of a test leaf end up in training, which inflates test accuracy.
The dataset authors' `leaf-map.json` links 40,490 photos to 7,524 physical leaves. I split the
data so that **every photo of a given leaf lands on only one side** (stratified, leaf-grouped
80/20 split), and asserted that no leaf crosses the split. For this model the inflation from a
naive split is small (99.1% vs 98.9%), but the leaf-level number is the one to trust. The
remaining 13,815 photos have no leaf mapping and are split photo by photo.

## Usage

```python
from transformers import pipeline

classifier = pipeline("image-classification", model="rodynaemad/plant-disease-dinov2-small")
print(classifier("leaf.jpg", top_k=3))
# [{'label': 'Tomato___Late_blight', 'score': 0.999}, ...]
```

### In the browser (ONNX)

`onnx/model_with_features.onnx` (88 MB, fp32) and `onnx/model_with_features_quantized.onnx`
(24 MB, int8) take `pixel_values` (1×3×224×224, ImageNet-normalized) and return `logits` and
the 768-d `features` used for the out-of-distribution check. The fp32 export matches PyTorch
exactly. The int8 copy, which powers the [Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner),
scores **98.7% accuracy (98.1% macro F1)** on the full leaf-level test set. Example with
[onnxruntime-web](https://onnxruntime.ai/docs/tutorials/web/) in the Space's `index.html`.

## How it was trained

- **Backbone:** [`facebook/dinov2-small`](https://huggingface.co/facebook/dinov2-small),
  frozen. Features are the concatenation of the CLS token and the mean patch token (768
  dimensions), exactly what `Dinov2ForImageClassification` feeds its classifier.
- **Head:** multinomial logistic regression on standardized features, with the standardization
  folded into the final linear layer. The regularization strength (C = 0.1) was chosen on a
  leaf-grouped validation split carved out of the training set; validation accuracy was 98.4–98.6%
  across C ∈ {0.1, 0.3, 1, 3}.
- **Data:** all 54,305 colour images of [PlantVillage](https://huggingface.co/datasets/mohanty/PlantVillage)
  (43,443 train / 10,862 test).
- **Check:** the exported Transformers model reproduces the trained classifier's predictions on
  100% of 200 sampled test images.

## Per-class F1 on unseen leaves

27 of 38 classes reach F1 ≥ 0.99. Weakest classes first:

| Crop | Condition | F1 |
|---|---|---|
| Corn (maize) | Cercospora leaf spot Gray leaf spot | 0.900 |
| Potato | healthy | 0.915 |
| Tomato | Early blight | 0.924 |
| Corn (maize) | Northern Leaf Blight | 0.949 |
| Tomato | Target Spot | 0.958 |
| Tomato | Late blight | 0.966 |
| Tomato | Bacterial spot | 0.967 |
| Tomato | Spider mites Two-spotted spider mite | 0.972 |
| Potato | Late blight | 0.972 |
| Tomato | Leaf Mold | 0.974 |
| Tomato | Septoria leaf spot | 0.984 |
| Tomato | healthy | 0.991 |
| Tomato | Tomato Yellow Leaf Curl Virus | 0.991 |
| Apple | Apple scab | 0.992 |
| Grape | Black rot | 0.994 |
| Grape | Esca (Black Measles) | 0.995 |
| Corn (maize) | Common rust | 0.996 |
| Pepper, bell | Bacterial spot | 0.997 |
| Potato | Early blight | 0.998 |
| Strawberry | Leaf scorch | 0.998 |
| Corn (maize) | healthy | 0.998 |
| Squash | Powdery mildew | 0.999 |
| Peach | Bacterial spot | 0.999 |
| Soybean | healthy | 1.000 |
| Apple | Black rot | 1.000 |
| Apple | Cedar apple rust | 1.000 |
| Apple | healthy | 1.000 |
| Blueberry | healthy | 1.000 |
| Cherry (including sour) | Powdery mildew | 1.000 |
| Cherry (including sour) | healthy | 1.000 |
| Grape | Leaf blight (Isariopsis Leaf Spot) | 1.000 |
| Grape | healthy | 1.000 |
| Orange | Haunglongbing (Citrus greening) | 1.000 |
| Peach | healthy | 1.000 |
| Pepper, bell | healthy | 1.000 |
| Raspberry | healthy | 1.000 |
| Strawberry | healthy | 1.000 |
| Tomato | Tomato mosaic virus | 1.000 |

The main confusion is between the two corn leaf-blight diseases (gray leaf spot vs. northern
leaf blight), which look alike. Potato healthy has only 152 photos in the whole dataset.

## Limitations

- **Lab photos only.** PlantVillage images show a single detached leaf on a plain background.
  Accuracy on field photos with clutter, multiple leaves, shadows or different cameras will be
  substantially lower. Do not read 98.9% as field performance.
- **Closed set.** The classifier always picks one of its 38 classes, even for images that are
  not leaves. The [Space](https://huggingface.co/spaces/rodynaemad/plant-disease-scanner) adds
  an out-of-distribution check (cosine similarity to per-class training centroids, calibrated so
  99% of real test leaves pass) that rejects solid colours, random noise and photos of people.
- **Not a diagnosis.** Use it as a screening aid and confirm with an agronomist or extension
  service before treating crops.

## License and attribution

Trained on PlantVillage (Hughes & Salathé, 2015; Mohanty, Hughes & Salathé, 2016), released
under CC BY-SA. This model is shared under **CC BY-SA 4.0**; the DINOv2 backbone is Apache 2.0.

## Author

[Rodayna Emad Mohamed](https://huggingface.co/rodynaemad), Research and Teaching Assistant,
College of Computer Science and AI, Pharos University in Alexandria ·
[GitHub](https://github.com/itsRou)
