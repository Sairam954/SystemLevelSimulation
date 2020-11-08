
from executecommand import ExecuteCommand
from os.path import isfile, join
from os import listdir

benchmarkfilespath = "/home/sairam/Desktop/SOS/Clos_Code_DP4/etc/benchmark6/"
swiftcodelocation ="/home/sairam/Desktop/SOS/Clos_Code_DP4/"

benchmarkfiles = [f for f in listdir(benchmarkfilespath) if isfile(join(benchmarkfilespath, f))]

exeCommand = ExecuteCommand()
for benchmark in benchmarkfiles:
    exeCommand.executeCommand("cd "+swiftcodelocation+" && "+"export SC_SIGNAL_WRITE_CHECK=DISABLE"+" && "+"./dp410M ./etc/benchmark6/"+benchmark+">./output/"+benchmark)

