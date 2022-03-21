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
        print(self.div_array)
        self.print_final()

    # Algorithm 1
    def BuildPrefixArray(self) -> (list, list):
        # initialize positional prefix array
        PPA = list(range(self.num_seq))
        DIV = [0 for _ in range(self.num_seq)]
        for k in range(self.seq_len-1):
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

    def print_final(self):
        html = '<pre style="line-height: 100%">'
        for i, pair in enumerate(zip(self.prefix_array, self.div_array)):
            idx, match_start = pair
            haplotype = self.haplotypes[idx]
            html += str(idx) + '|'
            for k, allele in enumerate(haplotype):
                if match_start == k and i:
                    html += '<strong><u>'
                html += str(allele)
            html += '</u></strong>'
            html += '<br/>'
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

