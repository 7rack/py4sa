#!/usr/bin/env python
#A command line tool that will grab total memory in a machine

import netsnmp
import optparse
from IPy import IP


class SnmpSession(object):
    """A basic snmp session"""
    def __init__(self,
                oid = "hrMemorySize",
                Version = 2,
                DestHost = "localhost",
                Community = "public"):
        self.oid = oid
        self.version = Version
        self.destHost = DestHost
        self.community = Community

    def query(self):
        """Creates SNMP query session"""
        try:
            result = netsnmp.snmpwalk(self.oid,
                                    Version = self.version,
                                    DestHost = self.destHost,
                                    Community = self.community)
        except Exception, err:
            print err
            result = None
        return result

class SnmpController(object):
    """Uses optparse to control snmpsession"""

    def run(self):
        results = {}

        p = optparse.OptionParser(description="A tool that determines memory installed",
                            prog = "memorator",
                            version = "memorator 0.1.0a",
                            usage = "%prog [subnet range] [options]")
        p.add_option('--community', '-c', help = 'community string', default = 'public')
        p.add_option('--oid', '-o', help = 'object identifier', default = 'hrMemorySize')
        p.add_option('--verbose', '-v', action = 'store_true', help = 'increase verbosity')
        p.add_option('--quiet', '-q', action = 'store_true',help = 'suppresses most messages')
        p.add_option('--threshold', '-t', action='store',type="int",help = 'a number to filter queries with')
        options, arguments = p.parse_args()
        if arguments:
            for arg in arguments:
                try:
                    ips = IP(arg)
                except:
                    if not options.quiet:
                        print 'Ignoring %s, not a valid IP address' % arg
                    continue
                
                for i in ips:
                    ipAddr = str(i)
                    if not options.quiet:
                        print 'Running snmp query for: ', ipAddr

                    session = SnmpSession(options.oid,
                            DestHost = ipAddr,
                            Community = options.community)

                    if options.oid == "hrMemorySize":
                        try:
                            memory = int(session.query()[0])/1024
                        except:
                            memory = None
                        output = memory

                    else:
                        #Non-memory related SNMP query results
                        output = session.query()
                        if not options.quiet:
                            print "%s returns %s" % (ipAddr,output)

                    #Put everything into an IP/result dictionary
                    #But only if it is a valid response
                    if output != None:
                        if options.threshold: #ensures a specific threshold
                            if output < options.threshold:
                                results[ipAddr] = output
                            #allow printing to standard out
                                if not options.quiet:
                                    print "%s returns %s" % (ipAddr,output)
                        else:
                            results[ipAddr] = output
                            if not options.quiet:
                                print output
                print "Results from SNMP Query %s for %s:\n" % (options.oid, arguments),results
        else:
            p.print_help() #note if nothing is specified on the command line, help is printed


def _main():
	"""
        Runs memorator.
        """
        start = SnmpController()
        start.run()

if __name__ =='__main__':
        try:
            import IPy
        except:
            print "Please install the IPy module to use this tool"
        _main()
