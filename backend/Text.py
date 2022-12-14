from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Union
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from sentence_transformers.util import cos_sim
import logging
import os
# import torch as t
from pathlib import Path
import random
# from torch import Tensor
from csv import DictWriter

logger = logging.getLogger(__name__)


# model = SentenceTransformer(
#     model_name_or_path="hfl/chinese-roberta-wwm-ext", device='cuda')

@dataclass
class TextStatus:
    FULL = 1
    EMPTY = 2


@dataclass
class SendTextOutput:
    text_status: TextStatus
    need2labeltext: str
    similar_label: List[str]


@dataclass
class LabelStatus:
    SUCCESS = 1
    ERROR = 2


@dataclass
class SaveTextInput:
    project: str
    text: str
    label: str
    # text_status: LabelStatus
    label_user: str
    label_datetime: datetime


class TextSave:
    def __init__(self) -> None:
        self.AllText: List[str] = []

    def Add(self, newtext: Union[List[str], str]):
        if isinstance(newtext, str):
            newtext = [newtext]

        if len(self.AllText) == 0:
            self.AllText = newtext
        else:
            self.AllText = list(set(self.AllText + newtext))

    @property
    def GetElement(self) -> str:
        if len(self.AllText) > 0:

            element = random.choice(self.AllText)
            return element
        else:
            return None

    def DropElement(self, element: str) -> None:
        try:
            index = self.AllText.index(element)
            self.AllText.pop(index)
        except Exception as e:
            pass

    @property
    def Len(self) -> int:
        return len(self.AllText)


class ManageText:
    def __init__(self, project_name: str, model: SentenceTransformer) -> None:
        self.model = model
        self.PROJECT_NAME = project_name
        self.data_file_dir = Path(__file__).parent.parent.joinpath('data')
        self.result_dir = self.data_file_dir.joinpath("result")
        self.text_dir = self.data_file_dir.joinpath("text")

        os.makedirs(self.data_file_dir, exist_ok=True)
        os.makedirs(self.result_dir, exist_ok=True)
        os.makedirs(self.text_dir, exist_ok=True)

        self.global_label: List[str] = []
        self.global_label_encoding = None

        # self.text_list: List[str] = []

        self.text_list = TextSave()

        self.save_csv_header = ['project', 'text', 'label',
                                'label_user', 'label_datetime']

        self.ALLRESULT_PATH = self.result_dir.joinpath('ALLRESULT.csv')
        if not self.ALLRESULT_PATH.exists():
            with open(self.ALLRESULT_PATH, 'a') as f_In:
                dictwrite_object = DictWriter(
                    f_In, fieldnames=self.save_csv_header)
                result = {i: i for i in self.save_csv_header}
                dictwrite_object.writerow(result)

    def InitLabel(self, label_list: List[str]):
        """
        ??????????????? ????????????????????????????????? ??????????????????????????????
        """
        logger.info("?????????????????????")
        self.global_label = label_list
        self.global_label_encoding = self.model.encode(self.global_label)

    def add_label(self, label_list: List[str]):
        """
        ??????????????????
        """
        logger.info("??????????????????")
        self.global_label = list(set(self.global_label + label_list))
        # temp_label_encoding = self.model.encode(label_list)
        # self.global_label_encoding = np.concatenate(
        #     [self.global_label_encoding, temp_label_encoding])
        self.global_label_encoding = self.model.encode(label_list)

    def delete_label(self, label_list: List[str]):
        """
        ??????label
        """
        logger.info("????????????")
        for temp_label in list(set(label_list)):
            if temp_label in self.global_label:
                index = self.global_label.index(temp_label)
                self.global_label.pop(index)
                self.global_label_encoding = np.delete(
                    self.global_label_encoding, index, axis=0)

    def init_text(self, text_list: List[str]):
        """
        ???????????????????????????
        """
        self.text_list.Add(text_list)

    @property
    def remained_text_number(self) -> int:
        """
        ??????????????????????????????
        """
        rtn = self.text_list.Len
        return rtn

    @property
    def SendText(self) -> SendTextOutput:
        """
        ????????????????????????
        """

        cur_text = self.text_list.GetElement

        if cur_text is not None:
            simi_list = self.GetSimilarList(cur_text)
            return SendTextOutput(text_status=TextStatus.FULL, need2labeltext=cur_text, similar_label=simi_list)
        else:
            return SendTextOutput(text_status=TextStatus.EMPTY, similar_label=[], need2labeltext='')

    def GetSimilarList(self, temp_text: str) -> List[str]:
        """
        ???????????????????????????10???
        """
        temp_encoding = self.model.encode([temp_text])
        score = cos_sim(temp_encoding, self.global_label_encoding).flatten()
        label_score: List[str] = pd.DataFrame({
            'label': self.global_label,
            'score': score
        }).pipe(
            lambda x: x.sort_values(by=['score'], ascending=False).head(10)
        )['label'].tolist()
        return label_score

    def SearchKey(self) -> list[str]:
        """
        ?????????????????????
        """
        result = self.global_label  # [i for i in self.global_label if i.find(key) != -1]
        return result

    def SaveResult(self, save_text: SaveTextInput):
        """
        ????????????
        """

        self.text_list.DropElement(save_text.text)

        with open(self.ALLRESULT_PATH, 'a') as f_In:
            dictwrite_object = DictWriter(
                f_In, fieldnames=self.save_csv_header)
            result = asdict(save_text)
            # result.pop('text_status')
            dictwrite_object.writerow(result)







