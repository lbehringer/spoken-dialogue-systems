###############################################################################
#
# Copyright 2020, University of Stuttgart: Institute for Natural Language Processing (IMS)
#
# This file is part of Adviser.
# Adviser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3.
#
# Adviser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Adviser.  If not, see <https://www.gnu.org/licenses/>.
#
###############################################################################

from typing import List
from utils.sysact import SysActionType

from utils.logger import DiasysLogger
from utils.domain.lookupdomain import LookupDomain
from utils import UserAct, UserActionType
from utils.sysact import SysAct
from utils.beliefstate import BeliefState
from services.service import PublishSubscribe
from utils.common import Language

from services.nlu import HandcraftedNLU
import re, json, os

def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class SongNLU(HandcraftedNLU):
    """Adapted handcrafted NLU for the song domain.

    The default handcrafted NLU is adapted to automatically add the user act request(name).
    This is necessary because the name is not the primary key, i.e. it is not printed by default
    once an element is found. To force the Policy to automatically inform about the name, too,
    a request for the name is added in each turn.
    """

    def __init__(self, domain: LookupDomain, logger: DiasysLogger = DiasysLogger()):
        # only calls super class' constructor
        HandcraftedNLU.__init__(self, domain, logger)
        
        # Getting domain information
        # self.domain_name = domain.get_domain_name()
        # self.domain_key = domain.get_primary_key()

        # # Getting lists of informable and requestable slots
        # self.USER_INFORMABLE = domain.get_informable_slots()
        # self.USER_REQUESTABLE = domain.get_requestable_slots()

        # # Getting the relative path where regexes are stored
        # #self.root_dir = get_root_dir()
        # self.base_folder = os.path.join(get_root_dir(), 'resources', 'nlu_regexes')
        # self.language = Language.ENGLISH
        # self._initialize()

    @PublishSubscribe(sub_topics=["user_utterance"], pub_topics=["user_acts"])
    def extract_user_acts(self, user_utterance: str = None, sys_act: SysAct = None, beliefstate: BeliefState = None) \
            -> dict(user_acts=List[UserAct]):
        """Original code but adapted to automatically add a request(name) act"""
        result = {}

        # Setting request everything to False at every turn
        self.req_everything = False

        self.user_acts = []

        # if last system act was Select, generate SelectOption user act:
        if self.sys_act_info["last_act"]:
            if self.sys_act_info["last_act"].type == SysActionType.Select:
                print(self.sys_act_info)
                if user_utterance is not None:
                    user_utterance = user_utterance.strip()
                    # PASS INFO FOR DANCEABILITY IN A WAY THAT IT COULD BE UPDATED IN THE BST
                    if self.sys_act_info["last_act"].slot_values:
                        # check if user utterance matches any of the selectable values (e.g. for track_name, if it matches one of the track_name options)
                        key = list(self.sys_act_info["last_act"].slot_values.keys())[0]
                        for val in self.sys_act_info["last_act"].slot_values[key][0]:
                            if user_utterance == val.lower():
                                slot = key
                                self.user_acts.append(UserAct(slot=slot, value=val,
                                                act_type=UserActionType.SelectOption))
                                result["user_acts"] = self.user_acts
                                return result

        # slots_requested & slots_informed store slots requested and informed in this turn
        # they are used later for later disambiguation
        self.slots_requested, self.slots_informed = set(), set()
        if user_utterance is not None:
            user_utterance = user_utterance.strip()
            self._match_general_act(user_utterance)
            self._match_domain_specific_act(user_utterance)

        # Solving ambiguities from regexes, especially with requests and informs happening
        # simultaneously on the same slot and two slots taking the same value
        self._disambiguate_co_occurrence(beliefstate)
        self._solve_informable_values()

        # If nothing else has been matched, see if the user chose a domain; otherwise if it's
        # not the first turn, it's a bad act
        if len(self.user_acts) == 0:
            if self.domain.get_keyword() in user_utterance:
                self.user_acts.append(UserAct(text=user_utterance if user_utterance else "",
                                              act_type=UserActionType.SelectDomain))
            elif self.sys_act_info['last_act'] is not None:
                # start of dialogue or no regex matched
                self.user_acts.append(UserAct(text=user_utterance if user_utterance else "",
                                              act_type=UserActionType.Bad))

        self._assign_scores()
        result['user_acts'] = self.user_acts
        self.logger.dialog_turn("User Actions: %s" % str(self.user_acts))
        return result


    @PublishSubscribe(sub_topics=["sys_state"])
    def _update_sys_act_info(self, sys_state):
        print("CALLING _UPDATE_SYS_ACT_INFO")
        if "lastInformedPrimKeyVal" in sys_state:
            self.sys_act_info['last_offer'] = sys_state['lastInformedPrimKeyVal']
        if "lastRequestSlot" in sys_state:
            self.sys_act_info['last_request'] = sys_state['lastRequestSlot']
        if "last_act" in sys_state:
            self.sys_act_info['last_act'] = sys_state['last_act']
            # THIS NEEDS TO BE SAVED SOMEWHERE
            # something like current song should mark this
            print(f"UPDATING LAST_ACT: {self.sys_act_info['last_act']}")


    def _match_general_act(self, user_utterance: str):
        """
        Finds general acts (e.g. Hello, Bye) in the user input

        Args:
            user_utterance {str} --  text input from user

        Returns:

        """

        # Iteration over all general acts
        for act in self.general_regex:
            # Check if the regular expression and the user utterance match
            if re.search(self.general_regex[act], user_utterance, re.I):
                # Mapping the act to User Act
                if act != 'dontcare' and act != 'req_everything':
                    user_act_type = UserActionType(act)
                else:
                    user_act_type = act
                # Check if the found user act is affirm or deny
                if self.sys_act_info['last_act'] and (user_act_type == UserActionType.Affirm or
                                                      user_act_type == UserActionType.Deny):
                    # Conditions to check the history in order to assign affirm or deny
                    # slots mentioned in the previous system act

                    # Check if the preceeding system act was confirm
                    if self.sys_act_info['last_act'].type == SysActionType.Confirm:
                        # Iterate over all slots in the system confimation
                        # and make a list of Affirm/Deny(slot=value)
                        # where value is taken from the previous sys act
                        for slot in self.sys_act_info['last_act'].slot_values:
                            # New user act -- Affirm/Deny(slot=value)
                            user_act = UserAct(act_type=UserActionType(act),
                                               text=user_utterance,
                                               slot=slot,
                                               value=self.sys_act_info['last_act'].slot_values[slot])
                            self.user_acts.append(user_act)

                    # Check if the preceeding system act was request
                    # This covers the binary requests, e.g. 'Is the course related to Math?'
                    elif self.sys_act_info['last_act'].type == SysActionType.Request:
                        # Iterate over all slots in the system request
                        # and make a list of Inform(slot={True|False})
                        for slot in self.sys_act_info['last_act'].slot_values:
                            # Assign value for the slot mapping from Affirm or Request to Logical,
                            # True if user affirms, False if user denies
                            value = 'true' if user_act_type == UserActionType.Affirm else 'false'
                            # Adding user inform act
                            self._add_inform(user_utterance, slot, value)

                    # Check if Deny happens after System Request more, then trigger bye
                    elif self.sys_act_info['last_act'].type == SysActionType.RequestMore \
                            and user_act_type == UserActionType.Deny:
                        user_act = UserAct(text=user_utterance, act_type=UserActionType.Bye)
                        self.user_acts.append(user_act)

                # Check if Request or Select is the previous system act
                elif user_act_type == 'dontcare':
                    if self.sys_act_info['last_act'].type == SysActionType.Request or \
                            self.sys_act_info['last_act'].type == SysActionType.Select:
                        # Iteration over all slots mentioned in the last system act
                        for slot in self.sys_act_info['last_act'].slot_values:
                            # Adding user inform act
                            self._add_inform(user_utterance, slot, value=user_act_type)

                # Check if the user wants to get all information about a particular entity
                elif user_act_type == 'req_everything':
                    self.req_everything = True

                else:
                    # This section covers all general user acts that do not depend on
                    # the dialog history
                    # New user act -- UserAct()
                    user_act = UserAct(act_type=user_act_type, text=user_utterance)
                    self.user_acts.append(user_act)



    def _initialize(self):
        """
            Loads the correct regex files based on which language has been selected
            this should only be called on the first turn of the dialog

            Args:
                language (Language): Enum representing the language the user has selected
        """
        if self.language == Language.ENGLISH:
            # Loading regular expression from JSON files
            # as dictionaries {act:regex, ...} or {slot:{value:regex, ...}, ...}
            self.general_regex = json.load(open(self.base_folder + '/GeneralRules.json'))
            self.request_regex = json.load(open(self.base_folder + '/' + self.domain_name
                                                + 'RequestRules.json'))
            self.inform_regex = json.load(open(self.base_folder + '/' + self.domain_name
                                               + 'InformRules.json'))
        elif self.language == Language.GERMAN:
            # TODO: Change this once
            # Loading regular expression from JSON files
            # as dictionaries {act:regex, ...} or {slot:{value:regex, ...}, ...}
            self.general_regex = json.load(open(self.base_folder + '/GeneralRulesGerman.json'))
            self.request_regex = json.load(open(self.base_folder + '/' + self.domain_name
                                                + 'GermanRequestRules.json'))
            self.inform_regex = json.load(open(self.base_folder + '/' + self.domain_name
                                               + 'GermanInformRules.json'))
        else:
            print('No language')