#*******************#
#                   #
# BANDWIDTH MONITOR #
#                   #
#*******************#
# Return: Bits rcv/snt
# Return: Total bits rcv/snt
# Display: Upper right-hand menu bar

#***********#
# Libraries #
#***********#
import time
import psutil

# PSUTIL.NET_IO_COUNTERS() will return network i/o stats as a named tuple with the following attributes:
# bytes_sent: number of bytes sent
# bytes_recv: number of bytes received
# packets_sent: number of packets sent
# packets_recv: number of packets received
# errin: total number of errors while sending
# dropin: total number of incoming packets which were dropped
# dropout: total number of outgoing packets which were dropped (always 0 on OSX and BSD)
# pernic = False: return only the sum of all counters since boot
# pernic = True: return all counters for each network interface available


#***********#
# Let's Go. #
#***********#

class BandwidthMonitor:

    def __init__(self):
        self.rcv = 0
        self.snt = 0
        self.initial_rcv, self.initial_snt = self.sent_rcv()
        
    def sent_rcv(self):
        '''RETURN: bytes sent and received.'''
        last_rcv = psutil.net_io_counters().bytes_recv
        last_snt = psutil.net_io_counters().bytes_sent
        return last_rcv, last_snt
        
    def update_snt_rcv(self):
        '''UPDATE: bytes sent and received.'''
        last_rcv, last_snt = self.sent_rcv()
        self.rcv = last_rcv
        self.snt = last_snt
    
    def current_bandwidth_sec(self, sec_delay = 1):
        '''RETURN: BYTES/SEC.
        The difference between current and last bytes sent and received.'''
        # Alright, the idea is: run it, collect the bytes reeceived and sent, and after
        #.. a second, collect the bytes received and sent again. Deduce the difference per second, 
        #.. then scale as desired.
       
        self.update_snt_rcv()                # LAST.
        time.sleep( sec_delay )              # SLEEP.
        last_rcv, last_snt = self.sent_rcv() # CURRENT.
        rcv_diff = last_rcv - self.rcv       # DIFFERENCE.
        snt_diff = last_snt - self.snt       # DIFFERENCE.
        return rcv_diff, snt_diff            # RETURN.
    
    def total_bandwidth( self ):
        '''RETURN: Total data usage since program start.'''
        
        last_rcv, last_snt = self.sent_rcv()
        rcv = last_rcv - self.initial_rcv 
        snt = last_snt - self.initial_snt
        total_bytes = rcv + snt                   
        return total_bytes
        
    def convert_bytes( self, total_bytes, scale = 'Bytes' ):
        '''RETURN: Bytes in desired scale.'''
        
        total_mega_bytes = total_bytes / 1000000
        total_gigabytes = total_mega_bytes / 1000
        
        if scale == 'Bytes':
            return total_bytes
        elif scale == 'MB':
            return total_mega_bytes
        elif scale == 'GB':
            return total_gigabytes
    
    def test_unit( self, module, seconds_to_run=10 ):
        '''UNIT_TEST'''
        
        for i in range( seconds_to_run ):
            
            if module == 'current_bandwidth_sec':
                print(self.current_bandwidth_sec())
            elif module == 'total_bandwidth':
                print(self.total_bandwidth())
            else:
                print('No module selected.')
            time.sleep(.25)
        
if __name__ == "__main__":
    b = BandwidthMonitor()
    b.test_unit('current_bandwidth_sec', 30)
    # print(a)

        
        
    
