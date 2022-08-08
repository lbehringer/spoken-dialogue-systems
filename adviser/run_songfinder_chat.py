import argparse
import os

from services.bst import HandcraftedBST
from services.domain_tracker.domain_tracker import DomainTracker
from services.service import DialogSystem
from utils.logger import DiasysLogger, LogLevel


def load_console():
    from services.hci.console import ConsoleInput, ConsoleOutput

    user_in = ConsoleInput(domain="")
    user_out = ConsoleOutput(domain="")
    return [user_in, user_out]


def load_backchannel():
    from services.backchannel import AcousticBackchanneller

    backchanneler = AcousticBackchanneller()
    # note: SpeechInputFeatureExtractor already loaded by requirement "--ASR"
    return [backchanneler]


# def load_gui():
#     from services.hci.gui import GUIServer
#     return GUIServer()


def load_nlg(backchannel: bool, domain=None):
    if backchannel:
        from services.nlg import BackchannelHandcraftedNLG

        nlg = BackchannelHandcraftedNLG(
            domain=domain, sub_topic_domains={"predicted_BC": ""}
        )
    else:
        from services.nlg.nlg import HandcraftedNLG

        nlg = HandcraftedNLG(domain=domain)
    return nlg


def load_songfinder_domain(backchannel: bool = False):
    # from utils.domain.jsonlookupdomain import JSONLookupDomain
    from utils.domain.song import SongDomain

    # from services.nlu.nlu import HandcraftedNLU
    from utils.domain.song.nlu import SongNLU
    from services.nlg.nlg import HandcraftedNLG

    # from services.policy import HandcraftedPolicy
    from services.policy.policy_api import HandcraftedPolicy as PolicyAPI

    songfinder = SongDomain()
    song_nlu = SongNLU(domain=songfinder)
    song_bst = HandcraftedBST(domain=songfinder)
    # song_policy = HandcraftedPolicy(domain=domain)
    song_policy = PolicyAPI(domain=songfinder)
    song_nlg = load_nlg(backchannel=backchannel, domain=songfinder)
    return songfinder, [song_nlu, song_bst, song_policy, song_nlg]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="conDUCKtor - ADVISER-based Dialog System"
    )
    parser.add_argument(
        "domains",
        nargs="+",
        choices=["songfinder"],
        help="Chat domain(s). For multidomain type as list: domain1 domain 2 .. \n",
        default="songfinder",
    )
    parser.add_argument("--debug", action="store_true", help="enable debug mode")
    parser.add_argument(
        "--log_file",
        choices=["dialogs", "results", "info", "errors", "none"],
        default="none",
        help="specify file log level",
    )
    parser.add_argument(
        "--log",
        choices=["dialogs", "results", "info", "errors", "none"],
        default="results",
        help="specify console log level",
    )
    args = parser.parse_args()

    num_dialogs = 100
    domains = []
    services = []

    # setup logger
    file_log_lvl = LogLevel[args.log_file.upper()]
    log_lvl = LogLevel[args.log.upper()]
    conversation_log_dir = "./conversation_logs"
    speech_log_dir = None
    if file_log_lvl == LogLevel.DIALOGS:
        # log user audio, system audio and complete conversation
        import time
        from math import floor

        print("This conDUCKtor call will log all your interactions to files.\n")
        if not os.path.exists(f"./{conversation_log_dir}"):
            os.mkdir(f"./{conversation_log_dir}/")
        conversation_log_dir = (
            "./" + conversation_log_dir + "/{}/".format(floor(time.time()))
        )
        os.mkdir(conversation_log_dir)
        speech_log_dir = conversation_log_dir
    logger = DiasysLogger(
        file_log_lvl=file_log_lvl,
        console_log_lvl=log_lvl,
        logfile_folder=conversation_log_dir,
        logfile_basename="full_log",
    )

    # load domain specific services
    if "songfinder" in args.domains:
        song_domain, song_services = load_songfinder_domain()
        domains.append(song_domain)
        services.extend(song_services)

    services.extend(load_console())

    # setup dialog system
    services.append(DomainTracker(domains=domains))
    debug_logger = logger if args.debug else None
    ds = DialogSystem(services=services, debug_logger=debug_logger)
    error_free = ds.is_error_free_messaging_pipeline()
    if not error_free:
        ds.print_inconsistencies()
    if args.debug:
        ds.draw_system_graph()

    # run dialogs in terminal
    try:
        for _ in range(num_dialogs):
            ds.run_dialog({"gen_user_utterance": ""})
        # free resources
        ds.shutdown()
    except:
        import traceback

        print("##### EXCEPTION #####")
        traceback.print_exc()
