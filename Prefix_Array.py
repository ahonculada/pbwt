from Haplotype import Haplotype
import sys
from typing import List
import webbrowser

class Prefix_Array:
    def __init__(self, haplotypes: Haplotype):
        self.haplotypes = haplotypes.matrix
        self.num_seq = haplotypes.rows
        self.seq_len = haplotypes.cols
        self.prefix_array = self.BuildPrefixArray()

    # Algorithm 1
    def BuildPrefixArray(self) -> List[List[int]]:
        # initialize positional prefix array
        PPA = list(range(self.num_seq))
        for k in range(self.seq_len-1):
            a, b = [], []
            for idx in PPA:
                haplotype = self.haplotypes[idx]
                allele = haplotype[k]
                if not allele:
                    a.append(idx)
                else:
                    b.append(idx)
            a.extend(b)
            PPA = a
            # print PPA of current timestep
            self.snapshot(PPA)
        return PPA

    # Build HTML for display
    def snapshot(self, PPA: list):
        html = '<pre style="line-height: 100%">'
        for idx in PPA:
            haplotype = self.haplotypes[idx]
            html += str(idx) + '|' + ''.join(str(allele) for allele in haplotype[:-1]) + '</br>'
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

