from transformers import AutoTokenizer
import torch
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import f1_score, accuracy_score

def get_output(model_checkpoint, data):
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, use_fast=False, local_files_only = True, tokenizer_args = {'normalization':True})
    test_encodings = tokenizer(data, truncation=True, padding=True, max_length=128)

    class SentimentDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, length):
            self.encodings = encodings
            self.length = length

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            return item

        def __len__(self):
            return self.length
    
    test_dataset = SentimentDataset(test_encodings, len(data))

    training_args = TrainingArguments(
        output_dir="model-output",          # output directory
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        num_train_epochs= 4,              # total number of training epochs
        per_device_train_batch_size = 4,  # batch size per device during training
        per_device_eval_batch_size = 4,   # batch size for evaluation
        warmup_steps=500,                # number of warmup steps for learning rate scheduler
        weight_decay=0.01,
        load_best_model_at_end=True
    )
    model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=3)

    trainer = Trainer(
        model=model,                         # the instantiated 🤗 Transformers model to be trained
        args=training_args,                  # training arguments, defined above
    )
    result = trainer.predict(test_dataset)
    
    from scipy.special import softmax

    probabilities = softmax(result.predictions, axis=1)
    predictions = []
    for triple in probabilities:
        predictions.append(int(list(triple).index(max(triple))))
    return predictions

def get_sentiment_predictions(data):
    vaccineBERT_output = get_output("./model/vaccineBert_SA", data)
    twitter_roberta_output = get_output("./model/twitter-roberta_SA", data)
    bertweet_covid19_output = get_output("./model/bertweet-covid19-base-uncased_SA", data)

    from random import randint
    from random import seed
    seed(123)
    test_size = len(data)
    ensemble = []
    for i in range(test_size):
        votes = [vaccineBERT_output[i], twitter_roberta_output[i], bertweet_covid19_output[i]]
        if votes.count(0) >= 2:
            ensemble.append(0)
        elif votes.count(1) >= 2:
            ensemble.append(1)
        elif votes.count(2) >= 2:
            ensemble.append(2)
        else:
            ensemble.append(randint(0, 2))
    
    return ensemble