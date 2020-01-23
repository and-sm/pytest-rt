# pytest-rt - pytest data collector for Testgr

Plugin sends pytest data to Testgr server.

### Setup

```pip install pytest-rt```

### Launch
```
pytest --rt --rtu="http://127.0.0.1/loader" -> will launch pytest with pytest-rt plugin.
```
Additional arguments:
\-\-rte="your_environment_or_version_etc" -> will send your environment name to the Testgr server. 

## Authors
[**Andrey Smirnov**](https://github.com/and-sm)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

