import sys
import os
from typing import List
import time
sys.path.append(os.path.abspath('../..'))

from utils.topics import Topic
from services.service import Service, PublishSubscribe, RemoteService

from utils.domain.domain import Domain
from utils.domain.jsonlookupdomain import JSONLookupDomain
from utils.logger import DiasysLogger, LogLevel

from services.hci import ConsoleInput, ConsoleOutput
from services.nlu import HandcraftedNLU
from services.bst import HandcraftedBST
from services.policy import HandcraftedPolicy
from services.nlg import HandcraftedNLG
from services.domain_tracker import DomainTracker

from services.service import DialogSystem

from torch.utils.tensorboard import SummaryWriter
from services.policy.rl.experience_buffer import NaivePrioritizedBuffer
from services.simulator import HandcraftedUserSimulator
from services.policy import DQNPolicy
from services.stats.evaluation import PolicyEvaluator


class ConcatenateServiceWithDomain(Service):
    def __init__(self, domain: str = "mydomain"):
        """ NEW: domain name! """
        song_domain = JSONLookupDomain(name="songfinder")
        Service.__init__(self, domain=domain)

    @PublishSubscribe(sub_topics=["A", "B"], pub_topics=["C", "D"])
    def concatenate(self, A: int = None, B: str = None) -> dict(C=str,D=str):
        """ NOTE: This function did not change at all """
        print("CONCATENATING ", A, "AND ", B)
        result = str(A) + " " + B
        if A == 3:
            return {'D': result}
        else:
            return  {'C': result}