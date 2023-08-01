import signal

from robot.Conversation import Conversation
from robot.LifeCycleHandler import LifeCycleHandler

from robot import config, logging, utils

logger = logging.getLogger(__name__)

class Assisstant(object):
    
    _profiling = False
    
    def __init__(self):
        self.conversation = Conversation(self._profiling)
        self.conversation.say(f"{config.get('first_name', '主人')} 你好！我是你的智能客服助手", True)
        self.lifeCycleHandler = LifeCycleHandler(self.conversation)
        self.lifeCycleHandler.onInit()
    
    def _signal_handler(self, signal, frame):
        self._interrupted = True
        utils.clean()
        self.lifeCycleHandler.onKilled()
        
    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        logger.info("Assisstant Running", stack_info=False)
        self.conversation.activeListen(silent=False)
        
if __name__ == "__main__":
    assisstant = Assisstant()
    assisstant.run()