"""
Implementation of Abstract Factory pattern for database query operations.
Provides a flexible framework for executing queries against various database types.


Example usage:
    factory = AbstractFactory()
    query_runner = factory.get_dao("bigquery")
    result = query_runner.get_number({
        "sql_statement": "select count(*) as the_number from `orders`",
        "return_value": "the_number"
    })

TODO:
    - Add logging configuration for production use
    - Consider adding connection pooling for database runners
    - Add validation for configuration dictionary structure
    - Implement retry mechanism for failed queries
    - Add metrics collection for query performance
"""

from abc import ABC, abstractmethod
import typing as tg
from pkg_resources import iter_entry_points


class QueryRunner(ABC):
    """Base interface for all database query runners.

    All concrete database implementations must inherit from this class
    and implement the get_number method.
    """

    @abstractmethod
    def get_number(self, configuration: tg.Dict) -> tg.Union[int, float]:
        """Execute query and return numeric result.

        Args:
            configuration: Dictionary containing query parameters and connection details

        Returns:
            Numeric result from the query execution

        Raises:
            NotImplementedError: If the concrete class doesn't implement this method
        """
        pass


class MongoDBRunner(QueryRunner):
    """MongoDB query implementation."""

    def get_number(self, configuration: tg.Dict) -> tg.Union[int, float]:
        """Mock implementation returning constant value 1."""
        # TODO: Implement actual MongoDB query execution
        return 1


class MySQLRunner(QueryRunner):
    """MySQL query implementation."""

    def get_number(self, configuration: tg.Dict) -> tg.Union[int, float]:
        """Mock implementation returning constant value 2."""
        # TODO: Implement actual MySQL query execution
        return 2


class BigQueryRunner(QueryRunner):
    """Google BigQuery implementation."""

    def get_number(self, configuration: tg.Dict) -> tg.Union[int, float]:
        """Mock implementation returning constant value 3."""
        # TODO: Implement actual BigQuery query execution
        return 3


class AbstractFactory:
    """Factory for creating database query runners.

    This class manages the creation of query runners and supports
    dynamic loading of implementations from external packages.
    """

    # Registry of available query runners
    _runners = {
        "mongodb": MongoDBRunner,
        "mysql": MySQLRunner,
        "bigquery": BigQueryRunner
    }

    def __init__(self):
        # Load any external implementations during initialization
        self._load_external_runners()

    def _load_external_runners(self):
        """Load query runners from external packages using entry points.

        Discovers and loads QueryRunner implementations from installed packages
        that provide them through the 'query_runners' entry point group.
        """
        for entry_point in iter_entry_points(group='query_runners'):
            try:
                runner_class = entry_point.load()
                if issubclass(runner_class, QueryRunner):
                    self._runners[entry_point.name] = runner_class
            except Exception as e:
                # TODO: Replace print with proper logging
                print(f"Error loading runner {entry_point.name}: {e}")

    def get_dao(self, runner_name: str) -> QueryRunner:
        """Get query runner instance by name.

        Args:
            runner_name: String identifier for the desired query runner

        Returns:
            Instance of the requested QueryRunner

        Raises:
            ValueError: If runner_name is not found in registry
        """
        runner_class = self._runners.get(runner_name)
        if runner_class is None:
            raise ValueError(f"Unknown query runner: {runner_name}")
        return runner_class()

    @classmethod
    def register_runner(cls, name: str, runner_class: tg.Type[QueryRunner]):
        """Register a new query runner implementation.

        Args:
            name: String identifier for the runner
            runner_class: Class implementing QueryRunner interface

        Raises:
            TypeError: If runner_class doesn't inherit from QueryRunner
        """
        if not issubclass(runner_class, QueryRunner):
            raise TypeError("Runner class must inherit from QueryRunner")
        cls._runners[name] = runner_class