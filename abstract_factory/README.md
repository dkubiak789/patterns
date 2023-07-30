# Assignment

## Senior dev: Implement an "abstract factory" in Python

### Assume the following:

* We have the need for a mechanism to run queries against various NoSQL databases. They are so different that simply replacing a driver won’t work and instead, we need totally different implementations.
* We want to run queries to different kinds of servers to fill dashboards with metrics, but it’s up to the end-user to configure them. This means that the user will select an implementation as a string value, for instance “mongodb”, “mysql” or “bigquery”, but other values may be used.
* The system has to follow the open-close-principle well, to ensure that it’s easy to add new implementations to the same functionality. We might want to implement a “couchdb” in the future, or even “http\_json”.
* The functionality that all these implementations require is:

  ```python
  def get_number(configuration: tg.Dict) -> tg.Union[int, float]
  ```
* The configuration is just a JSON-like data structure that the database connectors can use to connect / run the query and return a result.

### Requirements:

* The names “mongodb”, “mysql”, “bigquery” are not strict; you’re allowed to give them another name if that suits you better.
* You do not need to actually talk to a database. Just return 1 from the mongodb code, 2 from the mysql code and 3 from the bigquery code, because the actual implementation is not relevant for implementation of the design pattern.
* Implement an abstract factory that will be called from a web application and will be used like:

  ```python
  # the user selected these values in webpage
  query_runner_name = "bigquery"
  query_options = {
      "sql_statemant": "select count(*) as the_number from `orders`",
      "return_value": "the_number"
  }

  # then the application can use this code to query for a number
  factory = AbstractFactory()
  query_runner = factory.get_dao(query_runner_name)
  result = query_runner.get_number(query_options)
  # the value of result would then be 2
  assert result == 2
  ```
* Follow the open-close principle.
* Apply the AbstractFactory pattern as described by the Gang of Four \[[https://en.wikipedia.org/wiki/Abstract\_factory\_pattern](https://en.wikipedia.org/wiki/Abstract_factory_pattern)], as you see fits best in Python.

### Bonus:

* It appears that people who use this software want to be able to install implementations of other databases. We don’t know which ones though. Make it possible to ship new implementations in separate libraries.
* This last one is more difficult than it seems, because you’ll probably need dependency-inversion.
  \[[https://en.wikipedia.org/wiki/Dependency\_inversion\_principle](https://en.wikipedia.org/wiki/Dependency_inversion_principle)]

### Not important:

* Documentation: readable code is enough
* Unit tests: it’s about the class structure
* Implementations of the various concrete query runners
