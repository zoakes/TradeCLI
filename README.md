# TradeCLI
The general idea is a cloud based admin CLI, to manage, monitor, and override existing trade client. 
Can provide order status, balance, basis, position, and configuration details (anything written from trade client to SQL).

Also set up to add commands, via services, like flatten, halt, etc.

Save password in config, update SQL.py to fit your respective sql connection. FormatSql may need updating, to have proper columns for respective returns (depending on sql).

Standard Usage (as is)

To Run: 
```python
>>> python main.py
```

![Usage](https://github.com/zoakes/TradeCLI/blob/master/imgs/usage2.png)


