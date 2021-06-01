'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% COPYRIGHT NOTICE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Permission is granted for anyone to copy, use, modify, or distribute the
accompanying programs and documents for any purpose, provided this copyright
notice is retained and prominently displayed, along with a complete citation of
the published version of the paper:
 ______________________________________________________________________________
| G. Carleo, and M. Troyer                                                     |
| Solving the quantum many-body problem with artificial neural-networks        |
|______________________________________________________________________________|

The programs and documents are distributed without any warranty, express or
implied.

These programs were written for research purposes only, and are meant to
demonstrate and reproduce the main results obtained in the paper.

All use of these programs is entirely at the user's own risk.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

import numpy as np
from typing import Any, Tuple, List

class Ising1DHamiltonian:
    '''
    This class implements the transverse-field Ising (TFI) model Hamiltonian in one dimension. 
    The TFI Hamiltonian has the form 

    H_{TFI} = -h \sum_{i}\sigma^x_i - \sum_{ij}\sigma^z_i \sigma^z_j
    
    where \sigma^i are the Pauli matrices in the i-th direction and $h$ is the value of the transverse field. 

    '''

    def __init__(self, nSpins, hField, isPBC) -> None:
        self.nSpins = nSpins
        self.hField = hField
        self.isPBC = isPBC

        self.minSpinFlips = 1
        self.matElements = np.full(shape=self.nSpins + 1, fill_value=-self.hField, dtype=np.cdouble)
        self.spinFlips = np.vstack((np.empty(shape=[1,1]), np.arange(start=0, stop=self.nSpins).reshape(self.nSpins, 1)))
    
    def findNonZeroElements(self, state) -> Tuple[Any, List]:
        '''
        Finda all the non-zero matrix elements of the Hamiltonian on the given state, state. In other words,
        all state' such that <state'|H|state> is not zero

        state' is encoded as the sequence of spin flips to be performed on the state

        inputs: 
            state: A list of integers
        
        returns:
            matElements: A ndarray <state'|H|state> for each state' in spinFlips
            spinFlips: Stores the list of states corresponding to spin flips
        '''

        matElements = self.matElements
    
        # Find the Sz*Sz interaction
        matElements[0] = 0

        for i in range(self.nSpins - 1):
            matElements[0] -= state[i] * state[i + 1]
        
        if self.isPBC:
            matElements[0] -= state[self.nSpins - 1] * state[0]

        return matElements, self.spinFlips