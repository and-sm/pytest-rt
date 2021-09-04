# pytest-rt - pytest data collector for Testgr

Plugin sends pytest data to Testgr server.

### Setup

```pip install pytest-rt```

### Launch
```
pytest --rt --rtu="http://your_testgr_url/loader" -> will launch pytest with pytest-rt plugin.
```
Additional parameters: 

* --rte "your_environment" -> Send your environment name as additional data to the Testgr server. 
* --rt-job-report - Enable email sending after job finish.
* --rt-return-job - Write last finished job UUID in testgr_last_job.txt file.
* --rt-custom-data - Send any custom data to the Testgr in dict format. Example:
```
--rt-custom data='{"Git":"dev-branch"}'
```
* --rt-custom-id - requirement for pytest-xdist plugin. Use with random ID. 
```
--rt-custom-id="unique_id"
```

## Authors
[**Andrey Smirnov**](https://github.com/and-sm)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

