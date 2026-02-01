---
category: Resources
date: '2026-01-30 04:31:52'
subcategory: Apache Airflow
tags:
- airflow
- architecture
- distributed-systems
- scheduler
- executor
- webserver
- workers
- message-queue
- redis
- rabbitmq
- mysql
- postgres
title: 'Airflow Distributed Architecture: Webserver, Scheduler/Executor, Queue, Workers,
  Metadata DB'
---

# Airflow Distributed Architecture: Webserver, Scheduler/Executor, Queue, Workers, Metadata DB

> Diagram shows a typical distributed Apache Airflow setup: users access a webserver on a master node; the scheduler/executor reads/writes metadata in a SQL database, enqueues tasks to a message broker (Redis/RabbitMQ), and multiple worker nodes pull from the queue to execute tasks.

## High-level overview
- **Users** interact with the **Airflow Webserver**.
- A **Master node** runs:
  - **Webserver** (UI/API)
  - **Scheduler** (decides *what* tasks should run and *when*)
  - **Executor** (submits runnable tasks for execution)
- A shared **metadata database** (e.g., **MySQL/Postgres**) stores DAG runs, task states, configs, etc.
- A **message queue / broker** (e.g., **Redis/RabbitMQ**) buffers tasks to be executed.
- Multiple **Worker nodes** pull tasks from the queue and execute them in parallel.

## Data & control flow (as depicted)
1. **Users → Webserver**: users view/trigger DAGs and monitor runs.
2. **Webserver ↔ Metadata DB**: UI reads/writes state and configuration.
3. **Scheduler/Executor ↔ Metadata DB**: scheduler updates task/run state; executor coordinates submissions.
4. **Scheduler/Executor → Queue**: runnable tasks are placed onto the broker.
5. **Workers ← Queue**: workers consume tasks and execute them.

> [!INFO] Key idea
> The **master coordinates**, the **database records state**, the **queue distributes work**, and **workers scale horizontally** to run tasks concurrently.

## Components (Wikilinks)
- [[Airflow Webserver]]
- [[Airflow Scheduler]]
- [[Airflow Executor]]
- [[Airflow Metadata Database]]
- [[Message Broker]] (Redis/RabbitMQ)
- [[Airflow Workers]]