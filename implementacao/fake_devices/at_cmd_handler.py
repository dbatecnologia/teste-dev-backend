#!/usr/bin/env python3
#
# References:
#  AT Commands Manual
#   (http://ftp.icpdas.com/pub/cd/usbcd/napdos/3g_modem/gtm-203m-3gwa/manual/GTM-203M-3GWA_ATCommands_Manual.pdf)
#  atcmd (https://github.com/collab-project/atcmd)

from atcmd.parser import ATParser, ATCommandHandler, ATCommandResult

class AtEHandler(ATCommandHandler):
    """
    https://doc.qt.io/archives/qtopia4.3/modememulator-controlandstatus.html

    The ATE command can be used to turn command echo on (ATE1) or off (ATE0).
    """
    def __init__(self):
        self.value = 0

    def handleBasicCommand(self, arg):
        try:
            arg = int(arg)
            if arg == 0 or arg == 1:
                self.value = arg
                return ATCommandResult(ATCommandResult.OK)
        except:
            pass
        return ATCommandResult(ATCommandResult.ERROR)


class AtCopsHandler(ATCommandHandler):
    """
    The set command selects a mobile network automatically or manually.
    (To simplify, only <mode> has been implemented)
    """
    def __init__(self):
        self.mode = 0

    def handleTestCommand(self):
        """
        Searches the mobile network and returns a(fake) list
        of operators found.
        """
        res = '+COPS: (2,"","","0"),(1,"","","1")'
        return ATCommandResult(ATCommandResult.OK, res)

    def handleSetCommand(self, args):
        """
        AT+COPS=[<mode>]
        mode:
            0 automatic
            1 manual
            2 deregister from network
        """
        try:
            mode = args[0]
            if mode < 0 or mode > 2:
                raise
            self.mode = mode
            return ATCommandResult(ATCommandResult.OK)
        except:
            return ATCommandResult(ATCommandResult.ERROR)

    def handleReadCommand(self):
        """
        Get mode.
        """
        res = '+COPS: ' + str(self.mode)
        return ATCommandResult(ATCommandResult.OK, res)


class AtCgdcontHandler(ATCommandHandler):
    """
    Define the connection parameters for a PDP context.
    """
    def __init__(self):
        self.cid = 0
        self.PDP_type = 'IP'
        self.APN = ''
        self.PDP_addr = ''
        self.d_cmp = 0
        self.h_cmp = 0

    def handleTestCommand(self):
        """
        Return the connection parameters range.
        """
        res = '+CGDCONT: (1-3),"IP",,,(0-2),(0-2)'
        return ATCommandResult(ATCommandResult.OK, res)

    def handleSetCommand(self, args):
        """
        AT+CGDCONT=[<cid>[,<PDP_type>[,<APN>[,<PDP_addr>[,<d_cmp>[,<h_cmp>]]]]]]
        cid:
            PDP context identifier. A numeric parameter specifying a particular
            PDP context definition. The maximum number of active PDP contexts
            is 3.
        PDP_type:
            The Packet Data Protocol (PDP) type is a string parameter which
            specifies the type of packet data protocol:
                IP: Internet Protocol (IETF STD 5)
                PPP: Point to Point Protocol
        APN:
            The Access Point Name (APN) is a string parameter, which is a
            logical name, valid in the current PLMN's domain, used to select
            the GGSN (Gateway GPRS Support Node) or the external packet data
            network to be connected to.
        PDP_addr:
            String parameter identifying the MT in the IP-address space
            applicable to the PDP service.
        d_cmp:
            Numeric parameter specifying the PDP data compression; it can have
            the values:
                0 (default value): off
                1: on(predefined compression type i.e. V.42bis data compression)
                2: V.42bis data compression
        h_cmp:
            Numeric parameter specifying the PDP header compression; it can have
            the values:
                0 (default value): off
                1: on (predefined compression type, i.e. RFC1144)
                2: RFC1144
        """
        try:
            self.__check_set_params(args[0], args[1], args[2], args[3], args[4],
                    args[5])
            return ATCommandResult(ATCommandResult.OK)
        except:
            return ATCommandResult(ATCommandResult.ERROR)

    def handleReadCommand(self):
        """
        Get mode.
        """
        res = '+CGDCONT: ' + str(self.cid) + ', "' + self.PDP_type + '",' \
                + '"' + self.APN + '",' + '"' +self.PDP_addr + '",' + \
                str(self.d_cmp) + ',' + str(self.h_cmp)
        return ATCommandResult(ATCommandResult.OK, res)

    def __check_set_params(self, cid, PDP_type, APN, PDP_addr, d_cmp, h_cmp):
        if cid < 0 or cid > 3:
            raise
        if PDP_type != 'IP' and PDP_type != 'PPP':
            raise
        if type(APN) is not str:
            raise
        if type(PDP_addr) is not str:
            raise
        if d_cmp < 0 or d_cmp > 2:
            raise
        if h_cmp < 0 or h_cmp > 2:
            raise

        self.cid       = cid
        self.PDP_type  = PDP_type
        self.APN       = APN.lower()
        self.PDP_addr  = PDP_addr.lower()
        self.d_cmp     = d_cmp
        self.h_cmp     = h_cmp
