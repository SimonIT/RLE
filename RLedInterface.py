##########################################################################################
#  Namen:      Simon Bullik                                                              #
#  Prog-Name:  RLedInterface.py                  Klasse DQI16                            #
#  Version:    1.0                                                                       #
#  Python:     3.6                               Datum:      2017.12.17                  #
#  OS:         Windows 10                                                                #
##########################################################################################


class RL(object):

    def __init__(self):
        """Voreinstelllungen"""
        self.chunk_size = 4096
        self.MAXBYTES = 0

    def compress(self, sourcefile, destinationfile):
        """runlength compressing for any type of file
                @param sourcefile: The file including path that should be compressed
                @param destinationfile: The new file including path that should be created
                @type sourcefile: string
                @type destinationfile: string
                @return: Nothing

                It contains two paragraphs."""
        pass

    def expand(self, sourcefile):
        """runlength expanding for files which were\
                   compressed with compress method
                @param sourcefile: The file including path that should be compressed
                @type sourcefile: string
                @return: Nothing"""
        pass
