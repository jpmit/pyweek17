# leveldata.py

"""All the required information for each level."""

L0DATA = {'startbox' : [0, 0],
          'endbox' : [0, 0],
          'allowedbox' : [[0, 0]],
          'moonpos' : (0.8, 0.2),
          'asteroids' : {'00': [(0.4, 0.7)]}
          }
L1DATA = {'startbox' : [0, 0],
          'endbox' : [0, 0],
          'allowedbox' : [[0, 0]],
          'moonpos' : (0.8, 0.5),
          'asteroids' : {'00': [(0.5, 0.5),(0.3, 0.7)]}
          }
L2DATA = {'startbox' : [0, 0],
          'endbox' : [0, 1],
          'allowedbox' : [[0, 0], [0,1]],
          'moonpos' : (0.8, 0.2),
          'asteroids' : {'00': [(0.2, 0.3),(0.3, 0.7)],
                         '01' : [(0.2, 0.5)]}
          }
L3DATA = {'startbox' : [0, 0],
          'endbox' : [1, 1],
          'allowedbox' : [[0, 0], [1,0], [0,1], [1,1]],
          'moonpos' : (0.8, 0.2),
          'asteroids' : {'00': [(0.2, 0.8),(0.3, 0.7)],
                         '01' : [(0.2, 0.5)]}
          }
L4DATA = {'startbox' : [0, 0],
          'endbox' : [1, 0],
          'allowedbox' : [[0, 0], [1,0], [0,1], [1,1]],
          'moonpos' : (0.8, 0.2),
          'asteroids' : {'00': [(0.2, 0.4),(0.3, 0.7),(0.3, 0.7),(0.3, 0.7)],
                         '01' : [(0.2, 0.5)]}
          }
L5DATA = {'startbox' : [0, 0],
          'endbox' : [0, 0],
          'allowedbox' : [[0, 0], [0,1], [0,2]],
          'moonpos' : (0.8, 0.1),
          'asteroids' : {'00': [(0.5, 0.1),(0.5, 0.3),
                                (0.5, 0.5), (0.5, 0.7)],
                         '01' : [(0.5, 0.9), (0.5, 0.7),
                                 (0.5, 0.5)]}
          }

ALLDATA = [L0DATA, L1DATA, L2DATA]#, L3DATA, L4DATA, L5DATA]
