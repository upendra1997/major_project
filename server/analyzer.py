from train import Instructor
from pytorch_pretrained_bert import BertModel
# from train import Instructor
import numpy as np
from data_utils import pad_and_truncate
from sklearn import metrics
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
import argparse
import math
import os
import torch.nn.functional as F
from data_utils import build_tokenizer, build_embedding_matrix, Tokenizer4Bert, ABSADataset
from models import LSTM, IAN, MemNet, RAM, TD_LSTM, Cabasc, ATAE_LSTM, TNet_LF, AOA, MGAN
from models.aen import CrossEntropyLoss_LSR, AEN, AEN_BERT
from models.bert_spc import BERT_SPC
import torch
import spacy


class analyze():
    def __init__(self):
        class Option(object): pass
        opt = Option()

        opt.model_name = "bert_spc"
        opt.dataset = "twitter"
        opt.datasets = ["twitter", "restaurant", "laptop"]
        opt.optimizer = "adam"
        opt.initializer = "xavier_uniform_"
        opt.learning_rate = 2e-5
        opt.dropout = 0.1
        opt.l2reg = 0.1
        opt.num_epoch = 5
        opt.batch_size = 24
        opt.log_step = 5
        opt.logdir = 'log'
        opt.embed_dim = 300
        opt.hidden_dim = 300
        opt.bert_dim = 768
        opt.pretrained_bert_name = 'bert-base-uncased'
        opt.max_seq_len = 80
        opt.polarities_dim = 3
        opt.hops = 3
        opt.device = None

        model_classes = {
            'lstm': LSTM,
            'td_lstm': TD_LSTM,
            'atae_lstm': ATAE_LSTM,
            'ian': IAN,
            'memnet': MemNet,
            'ram': RAM,
            'cabasc': Cabasc,
            'tnet_lf': TNet_LF,
            'aoa': AOA,
            'mgan': MGAN,
            'bert_spc': BERT_SPC,
            'aen': AEN,
            'aen_bert': AEN_BERT,
        }
        dataset_files = {
            'twitter': {
                'train': './datasets/acl-14-short-data/train.raw',
                'test': './datasets/acl-14-short-data/test.raw'
            },
            'restaurant': {
                'train': './datasets/semeval14/Restaurants_Train.xml.seg',
                'test': './datasets/semeval14/Restaurants_Test_Gold.xml.seg'
            },
            'laptop': {
                'train': './datasets/semeval14/Laptops_Train.xml.seg',
                'test': './datasets/semeval14/Laptops_Test_Gold.xml.seg'
            }
        }
        input_colses = {
            'lstm': ['text_raw_indices'],
            'td_lstm': ['text_left_with_aspect_indices', 'text_right_with_aspect_indices'],
            'atae_lstm': ['text_raw_indices', 'aspect_indices'],
            'ian': ['text_raw_indices', 'aspect_indices'],
            'memnet': ['text_raw_without_aspect_indices', 'aspect_indices'],
            'ram': ['text_raw_indices', 'aspect_indices', 'text_left_indices'],
            'cabasc': ['text_raw_indices', 'aspect_indices', 'text_left_with_aspect_indices', 'text_right_with_aspect_indices'],
            'tnet_lf': ['text_raw_indices', 'aspect_indices', 'aspect_in_text'],
            'aoa': ['text_raw_indices', 'aspect_indices'],
            'mgan': ['text_raw_indices', 'aspect_indices', 'text_left_indices'],
            'bert_spc': ['text_bert_indices', 'bert_segments_ids'],
            'aen': ['text_raw_indices', 'aspect_indices'],
            'aen_bert' : ['text_raw_bert_indices', 'aspect_bert_indices'],
        }
        initializers = {
            'xavier_uniform_': torch.nn.init.xavier_uniform_,
            'xavier_normal_': torch.nn.init.xavier_normal,
            'orthogonal_': torch.nn.init.orthogonal_,
        }
        optimizers = {
            'adadelta': torch.optim.Adadelta,  # default lr=1.0
            'adagrad': torch.optim.Adagrad,  # default lr=0.01
            'adam': torch.optim.Adam,  # default lr=0.001
            'adamax': torch.optim.Adamax,  # default lr=0.002
            'asgd': torch.optim.ASGD,  # default lr=0.01
            'rmsprop': torch.optim.RMSprop,  # default lr=0.01
            'sgd': torch.optim.SGD,
        }
        
        opt.model_class = model_classes[opt.model_name]
        opt.dataset_file = dataset_files[opt.dataset]
        opt.dataset_files = dataset_files
        opt.inputs_cols = input_colses[opt.model_name]
        opt.initializer = initializers[opt.initializer]
        opt.optimizer = optimizers[opt.optimizer]
        opt.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') \
            if opt.device is None else torch.device(opt.device)
        self.opt = opt
        self.tokenizer = Tokenizer4Bert(opt.max_seq_len, opt.pretrained_bert_name)
        opt.state_dict_path = 'state_dict/trained.torch'
        try:
            bert = BertModel.from_pretrained(opt.pretrained_bert_name, state_dict = torch.load(opt.state_dict_path))
            self.model = opt.model_class(bert, opt).to(opt.device)
        except FileNotFoundError:
            bert = BertModel.from_pretrained(opt.pretrained_bert_name)
            ins = Instructor(opt)

            self.model = ins.run()
            
            self.model = ins.model
            torch.save(self.model.state_dict(), opt.state_dict_path)
    
    def evaluate(self, line, aspect):
        line = str(line)
        aspect = str(aspect)
        text_left, _, text_right = [s.lower().strip() for s in line.partition("$T$")]
        aspect = aspect.lower().strip()
        text_raw_indices = self.tokenizer.text_to_sequence(text_left + " " + aspect + " " + text_right)
        aspect_indices = self.tokenizer.text_to_sequence(aspect)
        aspect_len = np.sum(aspect_indices != 0)
        text_bert_indices = self.tokenizer.text_to_sequence('[CLS] ' + text_left + " " + aspect + " " + text_right + ' [SEP] ' + aspect + " [SEP]")
        bert_segments_ids = np.asarray([0] * (np.sum(text_raw_indices != 0) + 2) + [1] * (aspect_len + 1))
        bert_segments_ids = pad_and_truncate(bert_segments_ids, self.tokenizer.max_seq_len)
        inp = np.array([[text_bert_indices], [bert_segments_ids]])
        inp = torch.from_numpy(inp)
        inp = inp.to(self.opt.device)
        t_outputs = self.model(inp)
        t_probs = F.softmax(t_outputs, dim=-1).cpu().detach().numpy()
        return t_probs
    
    def result(self, line):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(line)
        labels = ["negative", "neutral", "positive"]
        result = []
        for idx, word in enumerate(doc):
            res = {"word": word.text, "label": "neutral", "value": 1}
#             print(word, word.text, word.pos_, word.dep_, word.is_alpha, word.is_stop)
            if word.is_alpha and (not word.is_stop):
                l = str(doc[: idx]) + ' $T$ ' + str(doc[idx+1:])
                r = self.evaluate(l, word)
                res["label"] = labels[r.argmax()]
                res["value"] = r.max()
            result.append(res)
        return result