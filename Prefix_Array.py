from Haplotype import Haplotype
import sys
from typing import List

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
        return PPA

    def display_prefix_array(self):
        for idx in self.prefix_array:
            haplotype = self.haplotypes[idx]
            pass


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
    print(P.prefix_array)

