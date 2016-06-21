#!/usr/bin/env python

from tabulate import tabulate
from itertools import zip_longest


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class APioModule(Dashboard.Module):
    """Parallel Input/Output display module"""

    def label(self):
        return 'PIO'

    def __init__(self):
        self.table = {}

    def lines(self, style_changed):
        out = []
        # fetch registers status
        # AT91C_PIOA_PDSR = 0xFFFFF400+0x0000003C
        # AT91C_PIOB_PDSR = 0xFFFFF600+0x0000003C
        nametab = list(range(28, -1, -4))
        pioatab = self.groupby(self.mem2regstr('0xFFFFF43C'), 4)
        piobtab = self.groupby(self.mem2regstr('0xFFFFF63C'), 4)

        table = tabulate(
            [nametab, pioatab, piobtab],
            tablefmt="orgtbl", headers="firstrow", numalign="right")

        for line in table.split('\n'):
            out.append(line)

        return out

    @staticmethod
    def mem2regstr(address):
        """Returns an array from a 32 bit memory address"""
        memstr = run('x/t '+address).split(':\t')[-1].strip('\n')
        return list(memstr)

    @staticmethod
    def groupby(grplist, grpsize):
        """Groups by grpszize elements a list"""
        return list([''.join(list(x)) for x in grouper(grplist, grpsize)])
