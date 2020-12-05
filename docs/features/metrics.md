# Metrics

{% hint style="info" %}
**Supported connections:** BigQuery, Postgres, Presto, Redshift, Snowflake
{% endhint %}

Whale supports automatic barebones metric definition and scheduled calculation. Metrics are defined by creating a ```````metrics```` block, as explained below. Any metric defined in this way will automatically be scheduled alongside the metadata scraping job. Metric definitions support Jinja2 templating -- for more information on how to set this up, see [Jinja2 templating](jinja2-templating.md).

## Basic usage

A metric is simply a named SQL statement that **returns a single value**, defined in plain yaml in a table stub, as shown below:

```text
```metrics
metric-name:
  sql: |
    select statement
```

For example, below two metrics, `null-registrations` and `distinct-registrations` are defined:

```
```metrics
null-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is null
distinct-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is not null
```

The same block is shown within the context of a full table stub, below:

```text
schema.table

## Column details

## Partition info

------------------------------------------------------
*Do not make edits above this line.*

```metrics
null-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is null
distinct-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is not null
```

These metrics will be scheduled, with the latest calculations injected into the programmatic portion of the table stub. An example is shown below:

```text
schema.table

## Column details

## Partition info

## Metrics
null-registrations: 103 @ 2020-04-01 05:12:15
distinct-registrations: 30104 @ 2020-04-01 05:12:18

------------------------------------------------------
*Do not make edits above this line.*

```metrics
null-registrations:
  sql: |
    select
      count(*)
    from mart.user_signups
    where user_id is null
distinct-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is not null
```

A full list of all historical values are saved in `~/.whale/metrics`.


## Slack alerts

Metrics can be enhanced with Slack alerts. These will send a message to you or your channel if a certain condition is met.
The syntax is as follows:

```text
```metrics
metric-name:
  sql: |
    select statement
  alerts:
    - condition: "condition"
      message: "message"
    - slack: ["channel"]
```

Using the earlier example we could set an alert every time we find a null in column `user_id` like this:

```
```metrics
null-registrations:
  sql: |
    select
      count(*)
    from mart.user_signups
    where user_id is null
  alerts:
    - condition: "> 0"
      message: "Nulls found in column 'user_id' of mart.user_signups."
      channel: ["#data-monitoring", "@bob"]
```

As you can see, you can send a message on Slack to _individuals_ as well as Slack _channels_.
In case you are interested, it's also possible to attach several conditions and messages to one metric.


All in all your `table.md` file with metrics and corresponding alerts could look like this:

```text
schema.table

## Column details

## Partition info

## Metrics
null-registrations: 103 @ 2020-04-01 05:12:15
distinct-registrations: 30104 @ 2020-04-01 05:12:18

------------------------------------------------------
*Do not make edits above this line.*

```metrics
null-registrations:
  sql: |
    select
      count(*)
    from mart.user_signups
    where user_id is null
  alerts:
    - condition: ">0"
      message: "Nulls found in column 'id' of mart.user_signups."
      channel: ["#data-monitoring", "@bob"]
    - condition: "> 100"
      message: "More than 100 nulls found in column 'id' of mart.user_signups."
      channel: ["#incident-room", "@joseph"]

distinct-registrations:
  sql: |
    select
      count(distinct user_id)
    from mart.user_signups
    where user_id is not null
  alerts:
    - condition: "<10"
      message: "Less than 10 users in mart.user_signups."
      channel: ["#data-monitoring", "@bob"]
```
