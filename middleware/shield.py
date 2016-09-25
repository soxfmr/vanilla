import time

class Shield(object):

    def __init__(self, maxtries=10, seconds=60, filename='blacklist.txt'):
        self.maxtries = maxtries
        self.seconds = seconds
        self.filename = filename

        self.blacklist = self.__load()
        self.logger = dict()

    def __load(self):
        try:
            with open(self.filename, 'r') as handle:
                for ip in handle:
                    self.blacklist.append(ip.strip())
        except IOError, e:
            pass

    def denied(self, client, addr):
        ip, port = addr

        if ip in self.blacklist:
            return True

        if not ip in self.logger:
            info = { 'time'     : time.time(),
                     'counter'  : 0 }
            self.logger[ip] = info

        return self.exceed(ip)

    def exceed(self, ip):
        current = time.time()
        guest = self.logger[ip]

        if current - guest['time'] <= self.seconds and \
            guest['counter'] >= self.maxtries:
            # R.I.P.
            self.blacklist.append(geust[ip])
            # save to file
            with open(self.filename, 'a+') as handle:
                handle.write('{}\n'.format( ip ))
            # remove client
            del self.logger[ip]

            return True

        guest['counter'] += 1
        self.logger[ip] = guest

        return False
