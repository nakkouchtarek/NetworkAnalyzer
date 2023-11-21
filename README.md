# NetworkAnalyzer

Packages needed: scapy psutil :
```
pip install scapy psutil
```

## Analyzer ##

Analyzes network(s) bandwidth, to use :
<br/>
Client Machine:
```
python clientanalyzer.py $IP $PORT
```

Server Machine:
```
python serveranalyzer.py $IP $PORT
```

## Sniffer ##

Sniffs packets network(s) packets, to use :
<br/>
Client Machine:
```
sudo python -E clientsniffer.py $IP $PORT
```

Server Machine:
```
python serveranalyzer.py $IP $PORT
```

## SoloSniffer ##

Sniffs packets on machine, to use :
```
sudo python -E singlesniffer.py
```



# Packet Sniffer:
![image](https://user-images.githubusercontent.com/98561646/235476814-99eff0f5-0ba9-495c-8742-46f5e98ef930.png)

# Client analyzer:
![image](https://user-images.githubusercontent.com/98561646/235477182-9b15c681-2e17-463c-84c0-99e7d2a28c3d.png)

# Server analyzer:
![image](https://user-images.githubusercontent.com/98561646/235477503-41d6711c-eb12-4393-8437-3eb5f46c9e53.png)

