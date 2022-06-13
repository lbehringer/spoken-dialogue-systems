from services.service import Service, PublishSubscribe, DialogSystem
from utils.topics import Topic


class ServiceA(Service):  # each servives should be inherited from services
    @PublishSubscribe(sub_topics=['start'])
    def start_system(self,
                     start):  # we added that later, because of the start signal at the end --> to start and publish the message
        self.send_message()

    @PublishSubscribe(pub_topics=[
        'topic1'])  # 2 - we create a method for sending messages --> # we can see the number of arguments in the service.py for example in PublishSucribe -->
    # we should decorated with  @PublishSubscribe(sub_topics=['start']) in order to let it to publish or suscribe. As convention we return a dictionary, we want to see what is the output for each topic
    def send_message(self):  # Dictionary helps to know which value we want to publish for each topic.
        return {'topic1': 'Hello'}


class ServiceB(Service):
    @PublishSubscribe(sub_topics=['topic1'],
                      pub_topics=['topic2'])  # here we choose which topic we want to subscribe to
    def subpub(self, topic1):  # we add topic 1 as argument  --> if we add a value in pub-topics, here we add it too
        return {'topic2': 'World!'}


class ServiceC(Service):
    @PublishSubscribe(sub_topics=['topic1', 'topic2'], pub_topics=[Topic.DIALOG_END])  # that concatenate two topics
    def concatenate(self, topic1, topic2):
        print(f"{topic1} {topic2}")
        return {Topic.DIALOG_END: True}  # once we concatenate everything here, we want to be done with the system
    # that's why we import Topic from utils.topic  --> if we publish False, the system will continue to run --> True here


a = ServiceA()  # we instantiate topics
b = ServiceB()
c = ServiceC()

ds = DialogSystem(
    services=[a, b, c])  # we create the dialog system  --> we can get the infor from service --> class DialogSystem
if not ds.is_error_free_messaging_pipeline():  # to debug it  --> look at service file  -> there are different functions there
    ds.print_inconsistencies()
ds.draw_system_graph(name="tutorial", show=True)  # we want to draw it --> the graph of the slides

ds.run_dialog(
    start_signals={'start': True})  # in order to run our dialog system, we can define any start signal we want.
# we should always shutdowm at the end
ds.shutdown()

# there were some explanation about the potational errors


