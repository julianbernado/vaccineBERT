# vaccineBERT workflow

Here we outline the workflow used for our Sentiment Analysis and Topic Modelling approach. Included are some flowcharts and more extensive description below.

## Sentiment Analysis

Details:
For general information about BERT models check out [this informative article](https://towardsdatascience.com/bert-explained-state-of-the-art-language-model-for-nlp-f8b21a9b6270) or [the original BERT paper from Google](https://arxiv.org/abs/1810.04805).
* To pre-process each Tweet, the following actions were taken:
  - All usernames were changed to the token "@USER"
  - All URLs were changed to the token "HTTPURL"
  - Emojis were removed 😔
  - Common contractions and punctuation was standardized (e.g. ’ vs. ')
  - Neither stemming nor lemmatization was done because the BERT model takes advantage of specific context described by different word forms.
* In the case where no majority label was decided (since there are three poossible labels and three models) a random label was chosen.

## Topic Modelling

Details:
* The transformation from Tweet to vector comes from extracting the final hidden layer of the vaccineBERT model
* The initial UMAP algorithm to reduce dimensionality uses the arguments `n_neighbors = 5`, `n_components = 20`, `metric = 'cosine'`, `random_state = 123`, and `min_dist = 0.1`. Documentation for this Python library can be found [here](https://umap-learn.readthedocs.io/en/latest/).
* The HDBSCAN algorithm to cluster uses the arguments `min_cluster_size = 10`, `min_sample = 2`, `metric = 'euclidean'`, and `cluster_selection_method = 'eom'`. Documentation for this Python library can be found [here](https://hdbscan.readthedocs.io/en/latest/index.html).
* The final UMAP call to create a 2D plot uses all the same arguments as the prior call, except with `n_neighbors = 10` and `n_components = 2`.
