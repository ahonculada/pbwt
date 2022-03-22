from Haplotype import Haplotype
import sys
from typing import List
import webbrowser

class Prefix_Array:
    def __init__(self, haplotypes: Haplotype):
        self.haplotypes = haplotypes.matrix
        self.num_seq = haplotypes.rows
        self.seq_len = haplotypes.cols
        self.snapshot_default()
        self.prefix_array, self.div_array = self.BuildPrefixArray()
        self.display_long_matches(3)

    # Algorithm 1 and 2
    def BuildPrefixArray(self) -> (list, list):
        # initialize positional prefix array
        PPA = list(range(self.num_seq))
        DIV = [0 for _ in range(self.num_seq)]
        for k in range(self.seq_len):
            a, b = [], []
            d, e = [], []
            p, q = k + 1, k + 1
            for idx, match_start in zip(PPA, DIV):
                haplotype = self.haplotypes[idx]
                allele = haplotype[k]
                if match_start > p:
                    p = match_start
                if match_start > q:
                    q = match_start
                if not allele:
                    a.append(idx)
                    d.append(p)
                    p = 0
                else:
                    b.append(idx)
                    e.append(q)
                    q = 0
            a.extend(b)
            d.extend(e)
            PPA = a
            DIV = d
            # print PPA of current timestep
            self.snapshot(PPA, DIV, k)
        #self.snapshot(PPA, DIV, self.seq_len-1)
        return PPA, DIV

    # Build HTML for display
    def snapshot_default(self):
        html = '<pre style="line-height: 100%">'
        for idx in range(self.num_seq):
            haplotype = self.haplotypes[idx]
            html += str(idx) + '|' + ''.join(str(allele) for allele in haplotype) + '</br>'
        html += '</pre>'
        with open('/tmp/sample.html', 'a') as sample:
            sample.write(html)

    # Build HTML for display
    def snapshot(self, PPA: list, DIV: list, step: int):
        html = '<pre style="line-height: 100%">'
        if step == self.seq_len - 1:
            for idx, match_start in zip(PPA, DIV):
                haplotype = self.haplotypes[idx]
                html += str(idx) + '|'
                for k, allele in enumerate(haplotype):
                    if match_start == k:
                        html += '<strong><u>'
                    html += str(allele)
                html += '</u></strong>'
                html += '<br/>'
        else:
            for idx, match_start in zip(PPA, DIV):
                haplotype = self.haplotypes[idx]
                html += str(idx) + '|'
                for k, allele in enumerate(haplotype[:step+1]):
                    if match_start == k:
                        html += '<strong><u>'
                    html += str(allele)
                if match_start < len(haplotype) - 1:
                    html += '</u></strong>'
                html += '  ' + str(haplotype[step+1]) + '  ' 
                for k, allele in enumerate(haplotype[step+2:]):
                    html += str(allele)
                html += '<br/>'

        html += '</pre>'
        with open('/tmp/sample.html', 'a') as sample:
            sample.write(html)

    # Algorithm 3
    def report_long_matches(self, min_length: int) -> (int, list, list):
        M = self.num_seq
        N = self.seq_len
        PPA = list(range(M))
        DIV = [0 for _ in range(M)]
        for k in range(N):
            a, b, d, e = list(), list(), list(), list()
            p, q = k + 1, k + 1
            ma, mb = list(), list()
            for idx, match_start in zip(PPA, DIV):
                if match_start > k - min_length:
                    if ma and mb:
                        yield k, ma, mb
                    ma, mb = [], []
                haplotype = self.haplotypes[idx]
                allele = haplotype[k]
                if match_start > p:
                    p = match_start
                if match_start > q:
                    q = match_start
                if not allele:
                    a.append(idx)
                    d.append(p)
                    p = 0
                    ma.append(idx)
                else:
                    b.append(idx)
                    e.append(q)
                    q = 0
                    mb.append(idx)
            if ma and mb:
                yield k, ma, mb
            if k < N - 1:
                a.extend(b)
                PPA = a
                d.extend(e)
                DIV = d

    def display_long_matches(self, min_length: int):
        html = '<pre style="line-height: 100%">'
        for match in self.report_long_matches(min_length):
            k, ma, mb = match
            for i in sorted(ma):
                for j in sorted(mb):
                    html += f'match ending at position {k} between haplotypes {i} and {j}:<br/><br/>'
                    h1 = self.haplotypes[i][k-min_length:k+1]
                    h2 = self.haplotypes[j][k-min_length:k+1]
                    html += str(i) + '|' + ''.join(str(allele) for allele in h1[:-1]) 
                    html += str(h1[-1]) + '<br/>'
                    html += str(j) + '|<strong><u>' + ''.join(str(allele) for allele in h2[:-1]) + '</u></strong>'
                    html += str(h2[-1]) + '<br/><br/>'
        html += '</pre>'
        with open('/tmp/sample.html', 'a') as sample:
            sample.write(html)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Error')
        print('Must include number of sequences and sequence length')
        print('Optional: write test case to file')
        exit()

    num_seq = int(sys.argv[1])
    seq_len = int(sys.argv[2])

    # create input haplotypes
    H = Haplotype(num_seq, seq_len)
    H.write_out()
    # Create Prefix Array
    P = Prefix_Array(H)
    filename = 'file:///tmp/sample.html'
    webbrowser.open_new_tab(filename)

