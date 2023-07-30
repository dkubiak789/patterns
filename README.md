# Python design patterns
## Abstract Factory

We want to run queries to different kinds of servers to fill dashboards
with metrics, but it’s up to the end-user to configure them. This
means that the user will select and implementation as a string value,
for instance “mongodb”, “mysql” or “bigquery”, but other values may be used.

Follow the open-close-principle to ensure that it’s easy to add new implementations to the same functionality.
