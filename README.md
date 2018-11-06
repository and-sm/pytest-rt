# pytest-rt - pytest data collector for Testgr

Plugin for sending HTTP POST pytest updates to your Testgr service

### Installing

```pip install pytest-rt```

### Launch
```
pytest --rt --rtu="http://127.0.0.1/loader" -> will launch pytest with pytest-rt plugin.
```
Additional arguments:
\-\-rte="your_environment" -> will launch pytest and send your environment name as additional info to the Tesgr server. 

## Authors
[**Andrey Smirnov**](https://github.com/and-sm)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

