xterm -hold -title "Peer 1" -e "python cdht.py 1 2 3" &
xterm -hold -title "Peer 2" -e "python cdht.py 2 3 4" &
xterm -hold -title "Peer 3" -e "python cdht.py 3 4 1" &
xterm -hold -title "Peer 4" -e "python cdht.py 4 1 2" &