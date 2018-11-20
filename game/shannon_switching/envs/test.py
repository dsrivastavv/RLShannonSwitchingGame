from ShannonGraph import ShannonGraph
gameGraph = ShannonGraph('graph', 1, 1)
gameGraph.playHumanMove([3,4])
computerMove = gameGraph.getNewComputerMove()
computerMove