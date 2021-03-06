# implements a helper to start and interact with a linux instance

import scripts.helpers.target_helper
import scripts.helpers.process_helper
import commands
import os
import signal
import time

class LinuxHelper(scripts.helpers.target_helper.TargetHelper):
    def __init__(self,instance_id):
        scripts.helpers.helper.Helper.__init__(self)
        self.instance_id = instance_id
        self.started = False
        if os.environ.has_key("DUAL_RCE"):
            self.max_session_id_char = 24
        else:
            self.max_session_id_char = 30


    def start_target(self):
        if (self.instance_id == None):
            xterm_name = os.environ["session_id"][0:self.max_session_id_char]
        else:
            xterm_name = self.instance_id  + "-" + os.environ["session_id"][0:self.max_session_id_char] 

        spawn_cmd = os.environ["XTERM_LOG"]
        arg_list = "-l","-lf"
        if (self.instance_id == None):
            arg_list += os.path.abspath(os.curdir+"/linux.log"),
        else:
            arg_list += os.path.abspath(os.curdir+"/linux." + self.instance_id + ".log"),

        title = xterm_name
        arg_list += "-sl","20000","-title",title,"-n",title
            
        if os.environ.has_key("vxsim_geometry"):
            arg_list += "-geometry",os.environ["vxsim_geometry"]

        #TBD fsw_file = os.environ["BUILD_ROOT"] + "/fsw/" + os.environ["COMPILER_dir"]+"/fsw"

        fsw_file = os.environ["BUILD_ROOT"] + "/fsw/" + os.environ["COMPILER_dir"] + "/fsw"
        if os.environ.has_key("LINUX_BIN_PRE"):
            arg_list += "-e",os.environ["LINUX_BIN_PRE"],fsw_file
        else:
            arg_list += "-e",fsw_file
                
        # This is a bit of a hack...
        string = "A"
        session_prefix = ""
        if (self.instance_id != None):
            if (self.instance_id == "RCE_B"):
                string = "B"
                session_prefix = "RCE_B_"


        arg_list += os.environ["TARGET_us_per_slice"],os.environ["TARGET_tickRate"],string,session_prefix + os.environ["session_id"][0:self.max_session_id_char]

                #TBD: NVMRAM, MEMSIZE, etc...

                # Start 
        self.linux_helper = scripts.helpers.process_helper.BackgroundProcess()
        self.linux_helper.start(spawn_cmd,arg_list,os.path.abspath(os.curdir+"/linux.stdout"),os.path.abspath(os.curdir+"/linux.stderr"))
        os.environ["TARGET_CONSOLE_STDOUT"]=os.path.abspath(os.curdir+"/linux.stdout")
        os.environ["CMD_STDOUT"] = os.path.abspath(os.curdir+"/cmds.stdouterr")
        self.started = True

    def load_fsw(self, fsw_file):
        print "base load"

    def run_cmd(self, cmd):
        print "base run"

    def reset(self):
        print "base reset"

    def exit(self):
        if self.started:
                        self.linux_helper.kill(signal.SIGKILL)

    def wait(self):
        print "base wait"

    def do_test(self, unit_test):
        print "base do_test"

    def genStdScript(self):
                print "genStdScript"
