# Social Media Text Preprocessing & Sentiment Analysis

An educational Python notebook by **Abdessamad Nafissi** exploring preprocessing choices for social-media sentiment analysis. It combines URL removal, custom emoji-to-text mappings, English-oriented normalization, optional profanity masking, TextBlob polarity, and exploratory charts.

[Original video tutorial](https://youtu.be/YBqk9RPrg1Y) · [Author's portfolio](https://nafissi-nlp.netlify.app/)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/A-Nafissi/Custom-NLP-pipeline/blob/main/Youtube_Tutorial_code.ipynb)

## Run the notebook

### Google Colab

1. Open the notebook using the badge above.
2. Download `youtube_coding.csv` from this repository and upload it through Colab's Files panel. Despite the extension, the sample is **tab-separated**.
3. Run the installation cell once, then run the remaining cells from top to bottom.

### Local Jupyter

Use Python 3.11 or later. From the repository directory:

```sh
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install jupyterlab
python -m jupyter lab Youtube_Tutorial_code.ipynb
```

Select the environment's Python kernel. The installation cell is optional when dependencies are already installed. No spaCy model or TextBlob corpus download is needed for these operations. Dependencies are explicit but not a lockfile.

## Processing steps

| Step | Behavior |
| --- | --- |
| Load | Read `tweet` and `language`; retain original text for comparison. |
| Select | Default to English-labeled rows; no translation provider is contacted. |
| Remove URLs | Strip HTTP(S) and `www.` URLs, including at the start of text. Does not extract domains or resolve links. |
| Convert emoji | Apply custom interpretations such as `😊` → `happy`, then descriptive Unicode names for other emoji. |
| Normalize | Replace mentions, split underscores and CamelCase, simplify hashtags while retaining C#, reduce elongated letters and repeated words, and normalize whitespace. |
| Mask profanity | Optional and disabled by default because it can change sentiment cues. |
| Score | Assign Negative, Neutral, or Positive from TextBlob polarity (< 0, = 0, > 0). |
| Visualize | Display a word cloud and sentiment-label counts for the processed sample. |

The final comparison contains `tweet`, `language`, `processed_text`, and `sentiment`.

## Customization

- Edit `my_dict` to change emoji interpretations for your domain.
- Set `CENSOR_PROFANITY = True` to enable masking.
- Adapt `data_cleaning` deliberately: its character filter targets English text and removes non-Latin characters.
- For translation, assign `TRANSLATE_TO_ENGLISH` a callable accepting a string and returning English text. Configure and evaluate your provider separately. Enabling it processes all loaded rows and can send text to that provider; review its data handling and costs first. No translation client is installed or configured by default.

This refresh removes the legacy automatic `googletrans` call and unnecessary large spaCy model download. It fixes definition order, URL removal, emoji handling, and accidental digit shortening. The original video is historical context and may differ from the updated notebook.

## Limitations and data

This is a tutorial, **not a trained or benchmarked classifier, hosted API, or production service**. It makes no accuracy claim. Normalization can remove useful syntax, repetition, symbols, and language information. Emoji interpretations are subjective; TextBlob may miss sarcasm, context, domain-specific meaning, and dialectal variation. Translation can introduce further sentiment changes. Evaluate against independently labeled data before downstream use.

`youtube_coding.csv` contains 510 historical social-media records; 468 carry the `en` label used by default. These labels are source metadata, not independently verified annotations. The sample has no sentiment ground truth, so label counts are not evaluation results. Original metadata includes usernames and links. This repository does not assert a license over those source posts; follow applicable source terms and permissions. No new posts are collected by the notebook.

## Files and checks

- `Youtube_Tutorial_code.ipynb` — tutorial and visualizations; saved outputs cleared.
- `youtube_coding.csv` — original tab-separated sample, unchanged.
- `requirements.txt` — runtime dependencies.
- `tests/test_notebook.py` — preprocessing regressions and offline-default checks.

After installing dependencies:

```sh
python -m unittest discover -s tests -v
```

The repository has no project license file. Contact the author about code reuse rather than assuming an open-source license.
