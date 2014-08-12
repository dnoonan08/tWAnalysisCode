#!/usr/bin/env python



















SFb_error = [[20,   2*0.0624031],
             [30,   0.0624031  ],
             [40,   0.034023   ],
             [50,   0.0362764  ],
             [60,   0.0341996  ],
             [70,   0.031248   ],
             [80,   0.0281222  ],
             [100,  0.0316684  ],
             [120,  0.0276272  ],
             [160,  0.0208828  ],
             [210,  0.0223511  ],
             [260,  0.0224121  ],
             [320,  0.0261939  ],
             [400,  0.0268247  ],
             [500,  0.0421413  ],
             [600,  0.0532897  ],
             [800,  0.0506714  ],
             [99999,2*0.0506714]]

def BtagSF(jetPt, syst=''):

    error = 0.0
    if syst == 'Up':
        for val in SFb_error:
            if jetPt < val[0]:
                error = val[1]
                break
    if syst == 'Down':
        for val in SFb_error:
            if jetPt < val[0]:
                error = -1*val[1]
                break

    if syst == 'Data':
        return 1.

    if jetPt < 20:
        x = 20
    elif jetPt > 800:
        x = 800
    else:
        x = jetPt
    
    SFb = 0.703389*((1.+(0.088358*x))/(1.+(0.0660291*x))) + error
#     SFb = (0.938887+(0.00017124*x))+(-2.76366e-07*(x*x)) + error

    return SFb

