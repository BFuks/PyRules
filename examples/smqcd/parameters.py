# User-defined parameters.
aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1184,
               lhablock = 'FRBlock',
               lhacode = [ 1 ])

MU = Parameter(name = 'MU',
               nature = 'external',
               type = 'real',
               value = 0.00255,
               lhablock = 'MASS',
               lhacode = [ 2 ])

MD = Parameter(name = 'MD',
               nature = 'external',
               type = 'real',
               value = 0.00255,
               lhablock = 'MASS',
               lhacode = [ 1 ])

MC = Parameter(name = 'MC',
               nature = 'external',
               type = 'real',
               value = 1.42,
               lhablock = 'MASS',
               lhacode = [ 3 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 172,
               lhablock = 'MASS',
               lhacode = [ 5 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.50833649,
               lhablock = 'DECAY',
               lhacode = [ 6 ])

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)')

