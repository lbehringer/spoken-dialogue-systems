# Importing everything we need for a dialog system
from utils.domain.jsonlookupdomain import JSONLookupDomain
from utils.logger import DiasysLogger, LogLevel

from services.hci import ConsoleInput, ConsoleOutput
from services.nlu import HandcraftedNLU
from services.bst import HandcraftedBST
from services.policy import HandcraftedPolicy
from services.nlg import HandcraftedNLG
from services.domain_tracker import DomainTracker

from services.service import DialogSystem

# create domain
song_domain = JSONLookupDomain(name="songfinder")

# create domain specific modules
nlu = HandcraftedNLU(domain=song_domain)
bst = HandcraftedBST(domain=song_domain)
policy = HandcraftedPolicy(domain=song_domain)
nlg = HandcraftedNLG(domain=song_domain)
d_tracker = DomainTracker(domains=[song_domain])

# Input modules (just allow access to terminal for text based dialog)
user_in = ConsoleInput(domain="")
user_out = ConsoleOutput(domain="")

logger = DiasysLogger(console_log_lvl=LogLevel.DIALOGS)
ds = DialogSystem(services=[d_tracker, user_in, user_out, nlu, bst, policy, nlg], debug_logger=logger)

error_free = ds.is_error_free_messaging_pipeline()
if not error_free:
    ds.print_inconsistencies()

ds.draw_system_graph(name='system', show=False)

# start dialog
for _ in range(1):
    ds.run_dialog({'gen_user_utterance': ""})
ds.shutdown()