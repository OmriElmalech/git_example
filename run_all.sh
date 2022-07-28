rm -f nohup.out
touch run_output.log
nohup python3 data_collection.py NFLX &
nohup python3 data_collection.py INTC &
nohup python3 data_collection.py AAPL &
nohup python3 data_collection.py GOOG &
nohup python3 data_collection.py AMZN &
nohup python3 data_collection.py TSLA &