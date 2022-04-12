"""
This demo aims to help player running system quickly by using the pypi library simple-emualtor https://pypi.org/project/simple-emulator/.

This is the template for CS5700 Term Project 1

We will change directory to sxxxxx (your directory) as specified in TA_eval.py
You MUST use "relative path" for loading your additonal modules/files

Any runtime error raised will heavily impact your scores
"""
from simple_emulator import BlockSelection, CongestionControl

# import yout side modules
import sideModule

# with open('a.txt', 'r') as f:
#     pass

EVENT_TYPE_FINISHED='F'
EVENT_TYPE_DROP='D'
EVENT_TYPE_TEMP='T'

# see https://github.com/AItransCompetition/simple_emulator#config
config = {
    'USE_CWND': True, # bool
    # 'ENABLE_LOG': True # bool
}

# Your solution should include block selection and bandwidth estimator.
# We recommend you to achieve it by inherit the objects we provided and overwritten necessary method.
class MySolution(BlockSelection, CongestionControl):

    def __init__(self):
        # base parameters in CongestionControl
        super().__init__()

        # init
        # add your code here

    def select_block(self, cur_time, block_queue):
        '''
        The alogrithm to select the block which will be sended in next.
        :param cur_time: float
        :param block_queue: the list of Block.
            You can get more detail about Block in https://github.com/AItransCompetition/simple_emulator/blob/mmgc_stable/objects/block.py
        :return: int (index in the block_queue)
        '''
        # you may overwrite this
        # print(f'len={len(block_queue)}')
        return 0 if len(block_queue) > 0 else -1

    def on_packet_sent(self, cur_time):
        """
        The part of solution to update the states of the algorithm when sender need to send packet.
        :param cur_time: float
        :return {"cwnd": int, "send_rate":int}
        """
        # you may overwrite this
        return {
            "cwnd" : 0,
            "send_rate" : 10,
        }

    def cc_trigger(self, cur_time, event_info):
        """
        The part of algorithm to make congestion control, which will be call when sender get an event about acknowledge or lost from reciever.
        See more at https://github.com/AItransCompetition/simple_emulator/tree/master#congestion_control_algorithmpy.
        :param cur_time: float
        :param event_info: seen at https://github.com/AItransCompetition/Meet-Deadline-Requirements-Challenge#:~:text=method%20is%20called.-,event_info,-event_type
        """

        event_type = event_info["event_type"]
        event_time = cur_time

        # set cwnd or sending rate in sender, you may overwrite this
        return {
            "cwnd" : 0,
            "send_rate" : 10,
        }