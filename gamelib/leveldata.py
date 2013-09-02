# leveldata.py

"""All the required information for each level."""

L1DATA = {'gravity' : [0.2, 0.4, 0.6, 0.8, 1.0],
          'startbox' : [0, 0],
          'rocketpos' : (0.2, 0.2),
          'endbox' : [0, 0],
          'allowedbox' : [[0, 0]],
          'moonpos' : (0.8, 0.5),
          'asteroids' : {'00': [(0.5, 0.5),(0.3, 0.7)]}
          }

L2DATA = {'gravity' : [0.2, 0.4, 0.8, 2.0, 4.0],
          'startbox' : [0, 0],
          'rocketpos' : (0.2, 0.2),
          'endbox' : [0, 1],
          'allowedbox' : [[0, 0], [0,1]],
          'moonpos' : (0.8, 0.2),
          'asteroids' : {'00': [(0.2, 0.1),(0.3, 0.7)],
                         '01' : [(0.2, 0.5)]}
          }

ALLDATA = [L1DATA, L2DATA]
