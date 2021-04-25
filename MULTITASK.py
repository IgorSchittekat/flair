import flair
from flair.data import Corpus, Sentence, TARSCorpus
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models.multitask_model.task_model import RefactoredTARSClassifier
from flair.models.text_classification_model import TARSClassifier
from flair.tokenization import SegtokTokenizer
from flair.trainers import ModelTrainer
from flair.datasets import TREC_50, CSVClassificationCorpus, SentenceDataset
import random
import itertools

base_path = "experiments_v2"

def make_text(data_point, text_columns):
    return [data_point[0], " ".join(data_point[text_column] for text_column in text_columns)]

def make_sentence(data_point, tokenizer):
    s = Sentence(data_point[1], use_tokenizer=tokenizer)
    s.add_label("class", data_point[0])
    return s

def get_trec(train: bool = False, test: bool = False):
    trec50_label_name_map = {
        'ENTY:sport': 'question about entity sport',
         'ENTY:dismed': 'question about entity diseases medicine',
         'LOC:city': 'question about location city',
         'DESC:reason': 'question about description reasons',
         'NUM:other': 'question about number other',
         'LOC:state': 'question about location state',
         'NUM:speed': 'question about number speed',
         'NUM:ord': 'question about number order ranks',
         'ENTY:event': 'question about entity event',
         'ENTY:substance': 'question about entity element substance',
         'NUM:perc': 'question about number percentage fractions',
         'ENTY:product': 'question about entity product',
         'ENTY:animal': 'question about entity animal',
         'DESC:manner': 'question about description manner of action',
         'ENTY:cremat': 'question about entity creative pieces inventions books',
         'ENTY:color': 'question about entity color',
         'ENTY:techmeth': 'question about entity technique method',
         'NUM:dist': 'question about number distance measure',
         'NUM:weight': 'question about number weight',
         'LOC:mount': 'question about location mountains',
         'HUM:title': 'question about person title',
         'HUM:gr': 'question about person group organization of persons',
         'HUM:desc': 'question about person description',
         'ABBR:abb': 'question about abbreviation abbreviation',
         'ENTY:currency': 'question about entity currency',
         'DESC:def': 'question about description definition',
         'NUM:code': 'question about number code',
         'LOC:other': 'question about location other',
         'ENTY:other': 'question about entity other',
         'ENTY:body': 'question about entity body organ',
         'ENTY:instru': 'question about entity musical instrument',
         'ENTY:termeq': 'question about entity term equivalent',
         'NUM:money': 'question about number money prices',
         'NUM:temp': 'question about number temperature',
         'LOC:country': 'question about location country',
         'ABBR:exp': 'question about abbreviation expression',
         'ENTY:symbol': 'question about entity symbol signs',
         'ENTY:religion': 'question about entity religion',
         'HUM:ind': 'question about person individual',
         'ENTY:letter': 'question about entity letters characters',
         'NUM:date': 'question about number date',
         'ENTY:lang': 'question about entity language',
         'ENTY:veh': 'question about entity vehicle',
         'NUM:count': 'question about number count',
         'ENTY:word': 'question about entity word special property',
         'NUM:period': 'question about number period lasting time',
         'ENTY:plant': 'question about entity plant',
         'ENTY:food': 'question about entity food',
         'NUM:volsize': 'question about number volume size',
         'DESC:desc': 'question about description description'
        }
    trec_full: Corpus = TREC_50(label_name_map=trec50_label_name_map)
    train_split = Corpus(train=trec_full.train, dev=trec_full.dev)
    test_split = [x for x in trec_full.test]

    if train and test:
        return trec_full
    elif train and not test:
        return train_split
    elif not train and test:
        return test_split

def get_agnews(train: bool = False, test: bool = False):
    random.seed(42)
    tokenizer = SegtokTokenizer()

    agnews_label_name_map = {
        '1': 'World',
          '2': 'Sports',
          '3': 'Business',
          '4': 'Science Technology'
    }
    column_name_map = {0: "label", 1: "text", 2: "text"}
    corpus_path = f"{flair.cache_root}/datasets/ag_news_csv"
    agnews_full: Corpus = CSVClassificationCorpus(
        corpus_path,
        column_name_map,
        skip_header=False,
        delimiter=',',
        label_name_map=agnews_label_name_map
    )
    train_split = SentenceDataset([s for s in agnews_full.train])
    dev_split = SentenceDataset([s for s in agnews_full.dev])
    train_split = Corpus(train=train_split, dev=dev_split)
    text_columns = [1,2]
    test_split_sentences = [make_text(data_point, text_columns) for data_point in agnews_full.test.raw_data]
    test_split = [make_sentence(data_point, tokenizer) for data_point in test_split_sentences]

    if train and not test:
        return train_split
    elif not train and test:
        return test_split

def get_dbpedia(train: bool = False, test: bool = False):
    random.seed(42)
    tokenizer = SegtokTokenizer()

    dbpedia_label_name_map = {'1': 'Company',
                              '2': 'Educational Institution',
                              '3': 'Artist',
                              '4': 'Athlete',
                              '5': 'Office Holder',
                              '6': 'Mean Of Transportation',
                              '7': 'Building',
                              '8': 'Natural Place',
                              '9': 'Village',
                              '10': 'Animal',
                              '11': 'Plant',
                              '12': 'Album',
                              '13': 'Film',
                              '14': 'Written Work'
                              }
    column_name_map = {0: "label", 1: "text", 2: "text"}
    corpus_path = f"{flair.cache_root}/datasets/dbpedia_csv"
    dbpedia_full: Corpus = CSVClassificationCorpus(
        corpus_path,
        column_name_map,
        skip_header=False,
        delimiter=',',
        label_name_map=dbpedia_label_name_map
    ).downsample(0.15)
    train_split = SentenceDataset([s for s in dbpedia_full.train])
    dev_split = SentenceDataset([s for s in dbpedia_full.dev])
    train_split = Corpus(train=train_split, dev=dev_split)
    text_columns = [1,2]
    test_split_sentences = [make_text(data_point, text_columns) for data_point in dbpedia_full.test.dataset.raw_data]
    test_split = [make_sentence(data_point, tokenizer) for data_point in test_split_sentences]

    if train and not test:
        return train_split
    elif not train and test:
        return test_split

def get_amazon(train: bool = False, test: bool = False):
    random.seed(42)
    tokenizer = SegtokTokenizer()

    amazon_label_name_map = {'1': 'very negative product sentiment',
                      '2': 'negative product sentiment',
                      '3': 'neutral product sentiment',
                      '4': 'positive product sentiment',
                      '5': 'very positive product sentiment'
                      }
    column_name_map = {0: "label", 2: "text"}
    corpus_path = f"{flair.cache_root}/datasets/amazon_review_full_csv"
    amazon_full: Corpus = CSVClassificationCorpus(
        corpus_path,
        column_name_map,
        skip_header=False,
        delimiter=',',
        label_name_map=amazon_label_name_map
    ).downsample(0.25)
    train_split = SentenceDataset([s for s in amazon_full.train])
    dev_split = SentenceDataset([s for s in amazon_full.dev])
    train_split = Corpus(train=train_split, dev=dev_split)
    text_columns = [2]
    test_split_sentences = [make_text(data_point, text_columns) for data_point in amazon_full.test.dataset.raw_data]
    test_split = [make_sentence(data_point, tokenizer) for data_point in test_split_sentences]

    if train and not test:
        return train_split
    elif not train and test:
        return test_split

def get_yelp(train: bool = False, test: bool = False):
    random.seed(42)
    tokenizer = SegtokTokenizer()

    yelp_label_name_map = {'1': 'very negative restaurant sentiment',
                      '2': 'negative restaurant sentiment',
                      '3': 'neutral restaurant sentiment',
                      '4': 'positive restaurant sentiment',
                      '5': 'very positive restaurant sentiment'
                      }
    column_name_map = {0: "label", 1: "text"}
    corpus_path = f"{flair.cache_root}/datasets/yelp_review_full_csv"
    yelp_full: Corpus = CSVClassificationCorpus(
        corpus_path,
        column_name_map,
        skip_header=False,
        delimiter=',',
        label_name_map=yelp_label_name_map
    ).downsample(0.13)
    train_split = SentenceDataset([s for s in yelp_full.train])
    dev_split = SentenceDataset([s for s in yelp_full.dev])
    train_split = Corpus(train=train_split, dev=dev_split)
    text_columns = [1]
    test_split_sentences = [make_text(data_point, text_columns) for data_point in yelp_full.test.dataset.raw_data]
    test_split = [make_sentence(data_point, tokenizer) for data_point in test_split_sentences]

    if train and not test:
        return train_split
    elif not train and test:
        return test_split

def train_sequential_model(corpora, task_name, configurations):
    if task_name == "AMAZON":
        tars = TARSClassifier(task_name=task_name, label_dictionary=corpora.make_label_dictionary(),
                              document_embeddings=configurations["model"])
    elif task_name == "YELP":
        tars = TARSClassifier.load(f"{configurations['path']}/sequential_model/after_AMAZON/best-model.pt")
        tars.add_and_switch_to_new_task(task_name, label_dictionary=corpora.make_label_dictionary())
    elif task_name == "DBPEDIA":
        tars = TARSClassifier.load(f"{configurations['path']}/sequential_model/after_YELP/best-model.pt")
        tars.add_and_switch_to_new_task(task_name, label_dictionary=corpora.make_label_dictionary())
    elif task_name == "AGNEWS":
        tars = TARSClassifier.load(f"{configurations['path']}/sequential_model/after_DBPEDIA/best-model.pt")
        tars.add_and_switch_to_new_task(task_name, label_dictionary=corpora.make_label_dictionary())
    elif task_name == "TREC":
        tars = TARSClassifier.load(f"{configurations['path']}/sequential_model/after_AGNEWS/best-model.pt")
        tars.add_and_switch_to_new_task(task_name, label_dictionary=corpora.make_label_dictionary())
    trainer = ModelTrainer(tars, corpora)
    trainer.train(base_path=f"{configurations['path']}/sequential_model/after_{task_name}",
                  learning_rate=0.02,
                  mini_batch_size=16,
                  max_epochs=10,
                  embeddings_storage_mode='none')

def eval_sequential_model(sentence_list, name, method, model, zeroshot = False):
    if method == "sequential_model":
        best_model_path = f"experiments_v2/{model}/{method}/after_AGNEWS/best-model.pt"
        best_model = TARSClassifier.load(best_model_path)
        best_model.switch_to_task(name)
        corpus = sentence_list
    else:
        best_model_path = f"experiments_v2/{model}/{method}/best-model.pt"
        best_model = RefactoredTARSClassifier.load(best_model_path)
        corpus = [x._add_tars_assignment(name.lower()) for x in sentence_list]

    if zeroshot:
        label_name_map = {'ENTY:sport': 'question about entity sport',
                          'ENTY:dismed': 'question about entity diseases medicine',
                          'LOC:city': 'question about location city',
                          'DESC:reason': 'question about description reasons',
                          'NUM:other': 'question about number other',
                          'LOC:state': 'question about location state',
                          'NUM:speed': 'question about number speed',
                          'NUM:ord': 'question about number order ranks',
                          'ENTY:event': 'question about entity event',
                          'ENTY:substance': 'question about entity element substance',
                          'NUM:perc': 'question about number percentage fractions',
                          'ENTY:product': 'question about entity product',
                          'ENTY:animal': 'question about entity animal',
                          'DESC:manner': 'question about description manner of action',
                          'ENTY:cremat': 'question about entity creative pieces inventions books',
                          'ENTY:color': 'question about entity color',
                          'ENTY:techmeth': 'question about entity technique method',
                          'NUM:dist': 'question about number distance measure',
                          'NUM:weight': 'question about number weight',
                          'LOC:mount': 'question about location mountains',
                          'HUM:title': 'question about person title',
                          'HUM:gr': 'question about person group organization of persons',
                          'HUM:desc': 'question about person description',
                          'ABBR:abb': 'question about abbreviation abbreviation',
                          'ENTY:currency': 'question about entity currency',
                          'DESC:def': 'question about description definition',
                          'NUM:code': 'question about number code',
                          'LOC:other': 'question about location other',
                          'ENTY:other': 'question about entity other',
                          'ENTY:body': 'question about entity body organ',
                          'ENTY:instru': 'question about entity musical instrument',
                          'ENTY:termeq': 'question about entity term equivalent',
                          'NUM:money': 'question about number money prices',
                          'NUM:temp': 'question about number temperature',
                          'LOC:country': 'question about location country',
                          'ABBR:exp': 'question about abbreviation expression',
                          'ENTY:symbol': 'question about entity symbol signs',
                          'ENTY:religion': 'question about entity religion',
                          'HUM:ind': 'question about person individual',
                          'ENTY:letter': 'question about entity letters characters',
                          'NUM:date': 'question about number date',
                          'ENTY:lang': 'question about entity language',
                          'ENTY:veh': 'question about entity vehicle',
                          'NUM:count': 'question about number count',
                          'ENTY:word': 'question about entity word special property',
                          'NUM:period': 'question about number period lasting time',
                          'ENTY:plant': 'question about entity plant',
                          'ENTY:food': 'question about entity food',
                          'NUM:volsize': 'question about number volume size',
                          'DESC:desc': 'question about description description'
                          }

        tp = 0
        all = 0
        classes = [key for key in label_name_map.values()]
        best_model.predict_zero_shot(corpus, classes, multi_label=False)
        for sentence in corpus:
            true = sentence.get_labels("class")[0]
            pred = sentence.get_labels("label")[0]
            if pred:
                if pred.value == true.value:
                    tp += 1
            all += 1
        print(f"Accuracy: {tp / all} \n")
        print(f"Correct predictions: {tp} \n")
        print(f"Total labels: {all} \n")
        with open(f"new_results/{name}-{method}-{model}.txt", "w") as file:
            file.write(f"Accuracy: {tp / all} \n")
            file.write(f"Correct predictions: {tp} \n")
            file.write(f"Total labels: {all} \n")
    else:
        result, _ = best_model.evaluate(corpus)
        with open(f"new_results/{name}-{method}-{model}.txt", "w") as f:
            f.write(result.detailed_results)

def train_multitask_model(corpora, configurations):

    tars_corpus = TARSCorpus(
        {"corpus": corpora["AMAZON"], "task_name": "amazon"},
        {"corpus": corpora["YELP"], "task_name": "yelp"},
        {"corpus": corpora["DBPEDIA"], "task_name": "dbpedia"},
        {"corpus": corpora["AGNEWS"], "task_name": "agnews"},
    )

    tars = RefactoredTARSClassifier(tars_corpus.tasks, document_embeddings="distilbert_entailment_label_sep_text/pretrained_mnli_rte_fever/best_model")

    trainer = ModelTrainer(tars, tars_corpus)
    trainer.train(base_path="experiments_v2/2_entailment_advanced/multitask_model_without_trec",
                  learning_rate=0.02,
                  mini_batch_size=16,
                  max_epochs=10,
                  embeddings_storage_mode='none')

def eval_multitask():
    label_name_map = {'ENTY:sport': 'question about entity sport',
                      'ENTY:dismed': 'question about entity diseases medicine',
                      'LOC:city': 'question about location city',
                      'DESC:reason': 'question about description reasons',
                      'NUM:other': 'question about number other',
                      'LOC:state': 'question about location state',
                      'NUM:speed': 'question about number speed',
                      'NUM:ord': 'question about number order ranks',
                      'ENTY:event': 'question about entity event',
                      'ENTY:substance': 'question about entity element substance',
                      'NUM:perc': 'question about number percentage fractions',
                      'ENTY:product': 'question about entity product',
                      'ENTY:animal': 'question about entity animal',
                      'DESC:manner': 'question about description manner of action',
                      'ENTY:cremat': 'question about entity creative pieces inventions books',
                      'ENTY:color': 'question about entity color',
                      'ENTY:techmeth': 'question about entity technique method',
                      'NUM:dist': 'question about number distance measure',
                      'NUM:weight': 'question about number weight',
                      'LOC:mount': 'question about location mountains',
                      'HUM:title': 'question about person title',
                      'HUM:gr': 'question about person group organization of persons',
                      'HUM:desc': 'question about person description',
                      'ABBR:abb': 'question about abbreviation abbreviation',
                      'ENTY:currency': 'question about entity currency',
                      'DESC:def': 'question about description definition',
                      'NUM:code': 'question about number code',
                      'LOC:other': 'question about location other',
                      'ENTY:other': 'question about entity other',
                      'ENTY:body': 'question about entity body organ',
                      'ENTY:instru': 'question about entity musical instrument',
                      'ENTY:termeq': 'question about entity term equivalent',
                      'NUM:money': 'question about number money prices',
                      'NUM:temp': 'question about number temperature',
                      'LOC:country': 'question about location country',
                      'ABBR:exp': 'question about abbreviation expression',
                      'ENTY:symbol': 'question about entity symbol signs',
                      'ENTY:religion': 'question about entity religion',
                      'HUM:ind': 'question about person individual',
                      'ENTY:letter': 'question about entity letters characters',
                      'NUM:date': 'question about number date',
                      'ENTY:lang': 'question about entity language',
                      'ENTY:veh': 'question about entity vehicle',
                      'NUM:count': 'question about number count',
                      'ENTY:word': 'question about entity word special property',
                      'NUM:period': 'question about number period lasting time',
                      'ENTY:plant': 'question about entity plant',
                      'ENTY:food': 'question about entity food',
                      'NUM:volsize': 'question about number volume size',
                      'DESC:desc': 'question about description description'
                      }
    trec = TREC_50(label_name_map=label_name_map)
    label_dict = trec.make_label_dictionary()
    tars_classic = TARSClassifier.load("experiments_v2/2_bert_baseline/sequential_model/after_AGNEWS/best-model.pt")
    tars_classic.add_and_switch_to_new_task("trec", label_dict)
    tp = 0
    all = 0
    classes = [key for key in label_name_map.values()]
    tars_classic.predict_zero_shot(trec.test, classes, multi_label=False)
    for sentence in trec.test:
        true = sentence.get_labels("class")[0]
        pred = sentence.get_labels("label")[0]
        if pred:
            if pred.value == true.value:
                tp += 1
        all += 1
    print(f"Accuracy: {tp / all} \n")
    print(f"Correct predictions: {tp} \n")
    print(f"Total labels: {all} \n")
    with open(f"experiments_v2/2_bert_baseline/sequential_model/hold_trec_out.log", "w") as file:
        file.write(f"Accuracy: {tp / all} \n")
        file.write(f"Correct predictions: {tp} \n")
        file.write(f"Total labels: {all} \n")

if __name__ == "__main__":
    flair.device = "cuda:0"
    eval_multitask()
    #corpora = {}
    #corpora["AMAZON"] = get_amazon(train=True)
    #corpora["YELP"] = get_yelp(train=True)
    #corpora["AGNEWS"] = get_agnews(train=True)
    #corpora["DBPEDIA"] = get_dbpedia(train=True)
    #train_multitask_model(corpora, "")

    #flair.device = "cuda:2"
    #for name, method, model in itertools.product(["TREC"], ["sequential_model"],
    #                                             ["2_bert_baseline", "2_entailment_standard", "2_entailment_advanced"]):
    #    eval_sequential_model(get_trec(test=True), name, method, model, zeroshot=True)


    """

    corpora = {}
    for name in ["AMAZON", "YELP", "DBPEDIA", "AGNEWS"]:
        corpora[name] = get_corpora(name)
    for key, configurations in path_model_mapping.items():
        train_multitask_model(corpora, configurations)


    for key, configurations in path_model_mapping.items():
        if key == "bert-base-uncased" and name == "AMAZON":
            pass
        else:
            train_sequential_model(corpora.get(name).get("train"), name, configurations)

    #eval_sequential_model(corpora.get(name).get("test"), configurations)
        #train_multitask_model()
    """