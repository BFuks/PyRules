import cmath

# User-defined parameters.
cabi = Parameter(name = 'cabi',
                 nature = 'external',
                 type = 'real',
                 value = 0.227736,
                 lhablock = 'CKMBLOCK',
                 lhacode = [ 1 ])

aEWM1 = Parameter(name = 'aEWM1',
                  nature = 'external',
                  type = 'real',
                  value = 127.9,
                  lhablock = 'SMINPUTS',
                  lhacode = [ 1 ])

Gf = Parameter(name = 'Gf',
               nature = 'external',
               type = 'real',
               value = 0.0000116637,
               lhablock = 'SMINPUTS',
               lhacode = [ 2 ])

aS = Parameter(name = 'aS',
               nature = 'external',
               type = 'real',
               value = 0.1184,
               lhablock = 'SMINPUTS',
               lhacode = [ 3 ])

ymdo = Parameter(name = 'ymdo',
                 nature = 'external',
                 type = 'real',
                 value = 0.00504,
                 lhablock = 'YUKAWA',
                 lhacode = [ 1 ])

ymup = Parameter(name = 'ymup',
                 nature = 'external',
                 type = 'real',
                 value = 0.00255,
                 lhablock = 'YUKAWA',
                 lhacode = [ 2 ])

yms = Parameter(name = 'yms',
                nature = 'external',
                type = 'real',
                value = 0.101,
                lhablock = 'YUKAWA',
                lhacode = [ 3 ])

ymc = Parameter(name = 'ymc',
                nature = 'external',
                type = 'real',
                value = 1.27,
                lhablock = 'YUKAWA',
                lhacode = [ 4 ])

ymb = Parameter(name = 'ymb',
                nature = 'external',
                type = 'real',
                value = 4.7,
                lhablock = 'YUKAWA',
                lhacode = [ 5 ])

ymt = Parameter(name = 'ymt',
                nature = 'external',
                type = 'real',
                value = 172,
                lhablock = 'YUKAWA',
                lhacode = [ 6 ])

yme = Parameter(name = 'yme',
                nature = 'external',
                type = 'real',
                value = 0.000511,
                lhablock = 'YUKAWA',
                lhacode = [ 11 ])

ymm = Parameter(name = 'ymm',
                nature = 'external',
                type = 'real',
                value = 0.10566,
                lhablock = 'YUKAWA',
                lhacode = [ 13 ])

ymtau = Parameter(name = 'ymtau',
                  nature = 'external',
                  type = 'real',
                  value = 1.777,
                  lhablock = 'YUKAWA',
                  lhacode = [ 15 ])

MZ = Parameter(name = 'MZ',
               nature = 'external',
               type = 'real',
               value = 91.1876,
               lhablock = 'MASS',
               lhacode = [ 23 ])

Me = Parameter(name = 'Me',
               nature = 'external',
               type = 'real',
               value = 0.000511,
               lhablock = 'MASS',
               lhacode = [ 11 ])

MMU = Parameter(name = 'MMU',
                nature = 'external',
                type = 'real',
                value = 0.10566,
                lhablock = 'MASS',
                lhacode = [ 13 ])

MTA = Parameter(name = 'MTA',
                nature = 'external',
                type = 'real',
                value = 1.777,
                lhablock = 'MASS',
                lhacode = [ 15 ])

MU = Parameter(name = 'MU',
               nature = 'external',
               type = 'real',
               value = 0.00255,
               lhablock = 'MASS',
               lhacode = [ 2 ])

MC = Parameter(name = 'MC',
               nature = 'external',
               type = 'real',
               value = 1.27,
               lhablock = 'MASS',
               lhacode = [ 4 ])

MT = Parameter(name = 'MT',
               nature = 'external',
               type = 'real',
               value = 172,
               lhablock = 'MASS',
               lhacode = [ 6 ])

MD = Parameter(name = 'MD',
               nature = 'external',
               type = 'real',
               value = 0.00504,
               lhablock = 'MASS',
               lhacode = [ 1 ])

MS = Parameter(name = 'MS',
               nature = 'external',
               type = 'real',
               value = 0.101,
               lhablock = 'MASS',
               lhacode = [ 3 ])

MB = Parameter(name = 'MB',
               nature = 'external',
               type = 'real',
               value = 4.7,
               lhablock = 'MASS',
               lhacode = [ 5 ])

MH = Parameter(name = 'MH',
               nature = 'external',
               type = 'real',
               value = 125,
               lhablock = 'MASS',
               lhacode = [ 25 ])

WZ = Parameter(name = 'WZ',
               nature = 'external',
               type = 'real',
               value = 2.4952,
               lhablock = 'DECAY',
               lhacode = [ 23 ])

WW = Parameter(name = 'WW',
               nature = 'external',
               type = 'real',
               value = 2.085,
               lhablock = 'DECAY',
               lhacode = [ 24 ])

WT = Parameter(name = 'WT',
               nature = 'external',
               type = 'real',
               value = 1.50833649,
               lhablock = 'DECAY',
               lhacode = [ 6 ])

WH = Parameter(name = 'WH',
               nature = 'external',
               type = 'real',
               value = 0.00407,
               lhablock = 'DECAY',
               lhacode = [ 25 ])

aEW = Parameter(name = 'aEW',
                nature = 'internal',
                type = 'real',
                value = '1/aEWM1')

G = Parameter(name = 'G',
              nature = 'internal',
              type = 'real',
              value = '2*cmath.sqrt(aS)*cmath.sqrt(cmath.pi)')

CKM = Parameter(name = 'CKM',
                 nature = 'internal',
                 indices = [Index('generation'), Index('generation')],
                 type = 'complex',
                 value = {(0,0):'cmath.cos(cabi)', {0,1}:'cmath.sin(cabi)', {1:0}:'-cmath.sin(cabi)',\
                          (1,1):'cmath.cos(cabi)', {2,2}:'1'})

MW = Parameter(name = 'MW',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(MZ**2/2. + cmath.sqrt(MZ**4/4. - (aEW*cmath.pi*MZ**2)/(Gf*cmath.sqrt(2))))')

ee = Parameter(name = 'ee',
               nature = 'internal',
               type = 'real',
               value = '2*cmath.sqrt(aEW)*cmath.sqrt(cmath.pi)')

sw2 = Parameter(name = 'sw2',
                nature = 'internal',
                type = 'real',
                value = '1 - MW**2/MZ**2')

cw = Parameter(name = 'cw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(1 - sw2)')

sw = Parameter(name = 'sw',
               nature = 'internal',
               type = 'real',
               value = 'cmath.sqrt(sw2)')

g1 = Parameter(name = 'g1',
               nature = 'internal',
               type = 'real',
               value = 'ee/cw')

gw = Parameter(name = 'gw',
               nature = 'internal',
               type = 'real',
               value = 'ee/sw')

vev = Parameter(name = 'vev',
                nature = 'internal',
                type = 'real',
                value = '(2*MW*sw)/ee')

lam = Parameter(name = 'lam',
                nature = 'internal',
                type = 'real',
                value = 'MH**2/(2.*vev**2)')

yb = Parameter(name = 'yb',
               nature = 'internal',
               type = 'real',
               value = '(ymb*cmath.sqrt(2))/vev')

yc = Parameter(name = 'yc',
               nature = 'internal',
               type = 'real',
               value = '(ymc*cmath.sqrt(2))/vev')

ydo = Parameter(name = 'ydo',
                nature = 'internal',
                type = 'real',
                value = '(ymdo*cmath.sqrt(2))/vev')

ye = Parameter(name = 'ye',
               nature = 'internal',
               type = 'real',
               value = '(yme*cmath.sqrt(2))/vev')

ym = Parameter(name = 'ym',
               nature = 'internal',
               type = 'real',
               value = '(ymm*cmath.sqrt(2))/vev')

ys = Parameter(name = 'ys',
               nature = 'internal',
               type = 'real',
               value = '(yms*cmath.sqrt(2))/vev')

yt = Parameter(name = 'yt',
               nature = 'internal',
               type = 'real',
               value = '(ymt*cmath.sqrt(2))/vev')

ytau = Parameter(name = 'ytau',
                 nature = 'internal',
                 type = 'real',
                 value = '(ymtau*cmath.sqrt(2))/vev')

yup = Parameter(name = 'yup',
                nature = 'internal',
                type = 'real',
                value = '(ymup*cmath.sqrt(2))/vev')

muH = Parameter(name = 'muH',
                nature = 'internal',
                type = 'real',
                value = 'cmath.sqrt(lam*vev**2)')

