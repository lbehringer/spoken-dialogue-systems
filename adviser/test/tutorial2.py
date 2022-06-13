from services.service import Service, PublishSubscribe, DialogSystem
from utils.topics import Topic
from utils.domain.jsonlookupdomain import JSONLookupDomain


class ServiceA(Service):

    def __init__(self, domain):  # we add an init method:
        Service.__init__(self, domain=domain)

    @PublishSubscribe(sub_topics=['start'])
    def start_system(self, start):
        self.send_message()

    @PublishSubscribe(pub_topics=['topic1'])
    def send_message(self):
        return {'topic1': 'Hello'}


class ServiceB(Service):
    @PublishSubscribe(sub_topics=['topic1'], pub_topics=['topic2'])
    def subpub(self, topic1):
        return {'topic2': 'World!'}


class ServiceC(Service):
    def __init__(self, domain):  # we add an init method:
        Service.__init__(self, domain=domain)

    @PublishSubscribe(sub_topics=['topic1', 'topic2'], pub_topics=[Topic.DIALOG_END])
    def concatenate(self, topic1, topic2):
        print(f"{topic1} {topic2}")
        return {Topic.DIALOG_END: True}


domain = JSONLookupDomain('songfinder')  # we give the domain name

a = ServiceA(domain=domain)  # here we added our domains
b = ServiceB(domain=domain)
c = ServiceC(domain=domain)

ds = DialogSystem(services=[a, b, c])
if not ds.is_error_free_messaging_pipeline():
    ds.print_inconsistencies()
ds.draw_system_graph(name="tutorial2", show=True)

ds.run_dialog(start_signals={'start': True})

ds.shutdown()

