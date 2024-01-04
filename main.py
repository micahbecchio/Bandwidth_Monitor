#**********************#
#                      #
# ..:: STATUS BAR ::.. #
#                      #
#**********************#
# via Rumps.
#NOTE: Put thread-stop logic at beginning of monitoring functions 
#.. to stop previous thread when another .rumps.clicked() is called.

#***********#
# Libraries #
#***********#
import rumps
import threading
from bandwidth_logic import BandwidthMonitor

#***********#
# Let's Go. #
#***********#

class BandwidthStatusBar( rumps.App ):
    
    def __init__( self ):
        super().__init__( "Becchio" )
        self.menu = ["Monitor Bandwidth",  
                     "Total Bandwidth",
                     "Stop Monitor",
                     {"Scale":[
                         rumps.MenuItem("Bytes", callback = self.method1),
                         rumps.MenuItem("MB", callback = self.method1),
                         rumps.MenuItem("GB", callback = self.method1)
                         ]
                      }
                    ]
        self.scale = "Bytes"
        self.bandwidth_monitor = BandwidthMonitor()
        self.default_title = "Becchio" 
        self.monitoring_thread = None 
        self.monitoring = False
        # We're making another thread so time.sleep(), while loops, 
        # #.. etc. don't interfere with main app function.

    def method1( self, sender ):
        '''Method via submenu (MenuItem).
            Set scale (B, MB, GB)'''
        self.scale = sender.title   
        
# -- MONITOR --------------       
    def monitor_bandwidth( self ):
        '''MONITOR BANDWIDTH: TRUE.'''
        # 1.) Monitoring True
        # 2.) While loop.
        # 3.) Call Bandwidth
        # 4.) Consider requested scale.
        # 5.) Print to 
        
        self.monitoring = True #1
        
        while self.monitoring: #2
        
            if self.monitoring:
                rcv, snt = self.bandwidth_monitor.current_bandwidth_sec() #3 # RCV, SNT
                if self.scale == "Bytes": #4
                    self.title = f" Rcv: {rcv:.1f}, Snt: {snt:.1f} B/s" #5  
                else:
                    snt_scaled = self.bandwidth_monitor.convert_bytes( total_bytes = snt, scale = self.scale ) #4
                    rcv_scaled = self.bandwidth_monitor.convert_bytes( total_bytes = rcv, scale = self.scale ) #4
                    self.title = f" Rcv: {rcv_scaled:.3f}, Snt: {snt_scaled:.3f} {self.scale}/s" #5  
                

# -- START --------------  
    @rumps.clicked("Monitor Bandwidth")
    def start_monitoring( self, _ ):
        '''START MONITOR BANDWIDTH'''
        
        # 1.) If a thread is going.
        # 2.) Stop Thread. (if going from: e.g.  Total Bandwidth to Monitor Bandwidth, vice vr.)
        # 3.) .join(): wait for current running thread to finish.Programs will stop here and wait for the thread to finish before continuing program.
        
        if self.monitoring_thread and self.monitoring_thread.is_alive(): #1
            self.monitoring = False #2
            self.monitoring_thread.join() #3
            
        # 1.) If thread isn't taken, 
        # 2.) Assign monitor_bandwidth method to thread
        # 3.) Start thread
        
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive(): #1
            self.monitoring_thread = threading.Thread( target = self.monitor_bandwidth ) #2
            self.monitoring_thread.start() #3
            
# -- STOP --------------        
    @rumps.clicked("Stop Monitor")
    def stop_monitoring( self, _ ):
        '''STOP MONITOR BANDWIDTH'''
        # 1.) If thread is going.
        # 2.) Stop Thread.
        # 3.) .join(): wait for thread to finish before printing (default) title. Programs will stop here and wait for the thread to finish before continuing program.
        # 4.) print title.
        
        if self.monitoring_thread and self.monitoring_thread.is_alive(): #1
            self.monitoring = False #2
            self.monitoring_thread.join() #3
            self.title = self.default_title # then, update title

# -- TOTAL BANDWIDTH --------------  

    def update_total_bandwidth( self ):
        '''Update total bandwidth.'''
        # 1.) self.monitoring = True
        # 2.) While loop monitoring = True (stop_monitoring sets monitoring = False)
        # 2.) Gather current bandwith. psutil gathers bytes since program open.
        # 3.) Allow 'scale' submenu logic (self.scale)
        # 4.) Update title.
        
        self.monitoring = True #1
        
        while self.monitoring: #2
        
            total_bytes = self.bandwidth_monitor.total_bandwidth() #2
            total_bytes = self.bandwidth_monitor.convert_bytes( total_bytes = total_bytes, scale = self.scale ) #3
            self.title = f"{total_bytes:.03f} {self.scale}" #4
        
    @rumps.clicked("Total Bandwidth")
    def total_bandwidth( self, _ ):
        '''START MONITOR BANDWIDTH'''
        
        # 1.) If a thread is going.
        # 2.) Stop Thread.
        # 3.) .join(): wait for current running thread to finish.Programs will stop here and wait for the thread to finish before continuing program.
        
        if self.monitoring_thread and self.monitoring_thread.is_alive(): #1
            self.monitoring = False #2
            self.monitoring_thread.join() #3
            
        # 1.) If thread is going, Stop Thread.
        # 1.) If thread isn't taken, 
        # 2.) Assign monitor_bandwidth method to thread
        # 3.) Start thread
        
        if self.monitoring_thread is None or not self.monitoring_thread.is_alive(): #1
            self.monitoring_thread = threading.Thread( target = self.update_total_bandwidth ) #2
            self.monitoring_thread.start() #3
        
if __name__ == "__main__":
    BandwidthStatusBar().run()