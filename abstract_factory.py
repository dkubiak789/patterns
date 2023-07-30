"""
Senior dev: Implement an "abstract factory" in Python

Assume the following:
* That we have the need of a mechanism to run queries against various NoSQL
  databases. They are so different that simply replacing a driver won’t work
  and instead, we need totally different implementations.
* We want to run queries to different kinds of servers to fill dashboards
  with metrics, but it’s up to the end-user to configure them. This
  means that the user will select and implementation as a string value,
  for instance “mongodb”, “mysql” or “bigquery”, but other values may be used.
* The system has to follow the open-close-principle well, to ensure that it’s
  easy to add new implementations to the same functionality. We might want to
  implement a “couchdb” in the future, or even “http_json”.
* the functionality that all these implementations require is
  `def get_number(configuration: tg.Dict) -> tg.Union[int,float]`
* the configuration is just a json-like datastructure that the database
  connectors an use to connect / run the query and return a result.

Requirements:
* the names “mongodb”, “mysql”, “bigquery” are not strict; you’re allowed
  to give them another name if that suits you better.
* You do not need to actually talk to a database. Just return 1 from
  the mongodb code, 2 form the mysql code and 3 from the bigquery code,
  because the actual implementation is not relevant for implementation
  of the design pattern.
* implement an abstract factory that will be called from a web application
  and will be used like:
```
# the user selected these values in webpage
query_runner_name = "bigquery"
query_options = {
"sql_statemant": "select count(*) as the_number from `orders`",
"return_value": "the_number"
}

# then the application van use this code to query for a number
factory = AbstractFactory()
query_runner = factory.get_dao(query_runner_name)
result = query_runner.get_number(query_options)
# the value of result would then be 2
assert result == 2
```
* follow the open-close principle
* apply the AbstractFactory pattern as described by the Gang of Four
  [https://en.wikipedia.org/wiki/Abstract_factory_pattern],
  as you see fits best in Python

Bonus:
* It appears that people that use this software want to be able
  to install implementations of other databases. We don’t know which ones
  though. Make it possible to ship new implementations in separate libraries.
  This last one is more difficult than it seems, because you’ll probably need
  dependency-inversion.
  [https://en.wikipedia.org/wiki/Dependency_inversion_principle]

Not important:
* documentation: readable code is enough
* unit tests: it’s about the class structure
* implementations of the various concrete query runners
"""
from abc import ABC, abstractmethod
from typing import Dict, Union


# Abstract base classes for query runner and factory
class QueryRunner(ABC):

    @abstractmethod
    def get_number(self, configuration: Dict) -> Union[int, float]:
        pass


class AbstractQueryRunnerFactory(ABC):

    @abstractmethod
    def get_query_runner(self, name: str) -> QueryRunner:
        pass


# Concrete query runner classes for different database implementations
class MongoDBQueryRunner(QueryRunner):

    def get_number(self, configuration: Dict) -> int:
        # Actual implementation code to query MongoDB
        return 1


class MySQLQueryRunner(QueryRunner):

    def get_number(self, configuration: Dict) -> int:
        # Actual implementation code to query MySQL
        return 2


class BigQueryQueryRunner(QueryRunner):

    def get_number(self, configuration: Dict) -> int:
        # Actual implementation code to query BigQuery
        return 3


# Concrete factory class for creating database-specific query runners
class QueryRunnerFactory(AbstractQueryRunnerFactory):

    def get_query_runner(self, name: str) -> QueryRunner:
        if name == "mongodb":
            return MongoDBQueryRunner()
        elif name == "mysql":
            return MySQLQueryRunner()
        elif name == "bigquery":
            return BigQueryQueryRunner()
        else:
            raise ValueError(f"Invalid query runner name: {name}.")


if __name__ == "__main__":
    query_runner_name = "bigquery"
    query_options = {
        "sql_statement": "select count(*) as the_number from `orders`",
        "return_value": "the_number"
    }

    factory = QueryRunnerFactory()
    query_runner = factory.get_query_runner(query_runner_name)
    result = query_runner.get_number(query_options)
    assert result == 3
    print("Query result:", result)
