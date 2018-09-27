
# pytest-rt - Real-time status update plugin via HTTP

Using following plugin you can send HTTP POST requests with test status updates to your API endpoint.

### Installing

Put pytest-rt near your conftest.py file.

In conftest.py enable following settings:
```
pytest_plugins = "pytest_rt"  
endpoint = "http://127.0.0.1/loader"  # Your API endpoint
show_errors = True  # show POST errors
```

### Launch
```
pytest --rt -> will launch pytest with pytest-rt plugin.
pytest --rt --rte=DEV -> will launch pytest with pytest-rt and send your environment name as additional info to the API server. 
```

### POST requests examples produced by pytest-rt

#### startTestRun
```
{
	"fw": "2",
	"type": "startTestRun",
	"tests": [{
		"location": "test_demo_sample",
		"nodeid": "test_positive.py::test_demo_sample"
	}],
	"env": "STAGE",
	"startTime": 1538080435.9450781,
	"job_id": "815c5b2d-d3b5-4425-91d1-22df2e032be8"
}
```
#### startTestItem
```
{
	"fw": "2",
	"type": "startTestItem",
	"job_id": "815c5b2d-d3b5-4425-91d1-22df2e032be8",
	"test": "test_positive.py::test_demo_sample",
	"startTime": "1538080435.9785562"
}
```
#### stopTest
```
{
	"type": "stopTest",
	"job_id": "07942d9c-03e8-4164-8709-2314119ad60b",
	"test": "project.folder.test_something.TestSomething.test_something",
	"stopTime": "1536775311.1239314",
	"status": "error",
	"msg": [
          "<class 'AttributeError'>",
          "'NoneType' object has no attribute 'location'",
          "<traceback object at 0x7ffac0a10f89>"
          ]
}
```
#### stopTestItem
```
{
	"fw": "2",
	"type": "stopTestItem",
	"job_id": "815c5b2d-d3b5-4425-91d1-22df2e032be8",
	"test": "test_positive.py::test_demo_sample",
	"status": "passed",
	"msg": "",
	"stopTime": "1538080435.996512"
}
```      

#### stopTestRun
```
{
	"fw": "2",
	"type": "stopTestRun",
	"job_id": "815c5b2d-d3b5-4425-91d1-22df2e032be8",
	"stopTime": "1538080436.009181"
}
```  

## Authors

[**Andrey Smirnov**](https://github.com/and-sm)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


