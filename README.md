# Generating SVG Images from Text Descriptions

## Objective
Develop a model that generates Scalable Vector Graphics (SVG) code based on a given text prompt, rendering the described image as accurately as possible.

## Problem Statement
Large Language Models (LLMs) often struggle to generate precise image-rendering code. This project aims to bridge that gap by generating SVG, a vector image format that uses XML to define two-dimensional graphics. SVGs can be scaled without quality loss, making them ideal for various applications.

## Dataset
The dataset consists of 500 text descriptions of everyday objects and scenes across diverse domains.

### Description Properties
- Common objects and generic subjects (no brand names, trademarks, or personal names).
- Covers approximately a dozen categories, including landscapes, abstract art, and fashion.
- Descriptions are capped at 200 characters, with an average length of 50 characters.
- `train.csv` includes data from the landscape, abstract, and fashion categories.
- Public and private test sets follow a similar category distribution.

## Submission Requirements
Participants must submit a `Model` class with a `predict()` function that takes a text description as input and returns SVG code.

## Evaluation Criteria
Performance is measured using **Mean CLIP Similarity** between the text description and the generated SVG image:
1. Each SVG is converted into a PNG using the `cairosvg` Python library.
2. The PNG image is encoded into feature embeddings using a **SigLIP SoVIT-400m** model.
3. The final score is the **average cosine similarity** between the text description embeddings and the corresponding image embeddings.

## Constraints

### SVG Constraints
- The SVG file must not exceed **10,000 bytes**.
- Only elements and attributes from a **predefined allowlist** are permitted.
- **CSS styles are not allowed**.
- No **rasterized images** or external data sources are allowed in the SVG.

### Model Constraints
- The model must return **SVG output within 5 minutes** of receiving a description.
- All SVGs must be **generated within 9 hours**.

## Installation & Usage
### Dependencies
To run the model, install the required dependencies:
```bash
pip install cairosvg torch torchvision
```

### Running the Model
Ensure you have the dataset and then run the model:
```python
from model import Model

model = Model()
text_description = "A simple mountain landscape with a rising sun."
svg_output = model.predict(text_description)
print(svg_output)  # Outputs SVG code
```

## License
This project is open-source under the MIT License.

## Contributors
- [Your Name]
- [Other Contributors]

## Acknowledgments
Special thanks to the AI and graphics research community for inspiration and tools that made this project possible.

