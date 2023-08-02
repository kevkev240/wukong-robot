import signal

from robot.Conversation import Conversation
from robot.LifeCycleHandler import LifeCycleHandler
from server import server

from robot import config, logging, utils

logger = logging.getLogger(__name__)

class Assisstant(object):
    
    _profiling = False
    
    def __init__(self, init_message):
        self.init_message = init_message
        self.first_message = f"您好{config.get('first_name', '')}, 我是你的智能客服助手。{self.init_message}"
        self.conversation = Conversation(self._profiling)
        self.conversation.say(self.first_message, False)
        self.lifeCycleHandler = LifeCycleHandler(self.conversation)
        self.lifeCycleHandler.onInit()
    
    def _signal_handler(self, signal, frame):
        print("signal: " + signal)
        self._interrupted = True
        utils.clean()
        self.lifeCycleHandler.onKilled()
        
    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        server.run(self.conversation, self, debug=False)
        logger.info("Assisstant Running", stack_info=False)
        self.conversation.activeListen(silent=False)
        
if __name__ == "__main__":
    init_message = ""
    # init_message = "您于7月11日欠费200元。请及时还款。"
    assisstant = Assisstant(init_message)
    assisstant.run()