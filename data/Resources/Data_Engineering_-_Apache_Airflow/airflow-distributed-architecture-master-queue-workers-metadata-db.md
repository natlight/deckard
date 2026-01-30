---
category: Resources
date: '2026-01-30 04:35:40'
subcategory: Data Engineering - Apache Airflow
tags:
- airflow
- architecture
- scheduler
- executor
- workers
- message-queue
- redis
- rabbitmq
- metadata-database
- webserver
- distributed-systems
title: 'Airflow Distributed Architecture: Master Node, Queue, Workers, and Metadata
  DB'
---

# Airflow Distributed Architecture: Master Node, Queue, Workers, and Metadata DB

> Diagram shows a distributed Apache Airflow setup where users interact with the webserver on a master node; the scheduler triggers tasks via an executor that enqueues work to a message broker; multiple worker nodes pull tasks from the queue and execute them while state is stored in a metadata database.

## What the diagram depicts
A distributed [[Apache Airflow]] deployment with a central “master” node coordinating task scheduling and a pool of worker nodes executing tasks.

## Components
- **Users**: Interact with the Airflow UI/API.
- **Master node**
  - **Webserver**: Serves the UI; receives user actions and displays DAG/task status.
  - **Scheduler**: Determines what tasks should run and when.
  - **Executor**: Converts scheduled tasks into executable work items and hands them off for execution.
- **Metadata database (MySQL/Postgres)**: Persists DAG runs, task instances, states, logs metadata pointers, connections, variables, etc.
- **Message queue (Redis/RabbitMQ)**: Buffers task messages for asynchronous distribution.
- **Worker nodes (1..N)**: Pull tasks from the queue and execute them in parallel.

## Flow (high level)
1. **Users → Webserver**: Users trigger/monitor DAGs via the UI.
2. **Scheduler → Executor**: Scheduler identifies runnable tasks; executor prepares them for dispatch.
3. **Executor → Queue**: Tasks are pushed to the message broker (e.g., Redis/RabbitMQ).
4. **Workers → Queue**: Workers consume queued tasks.
5. **Workers ↔ Metadata DB**: Execution state and results are recorded (and read) via the metadata database.
6. **Webserver ↔ Metadata DB**: UI reads persisted state to display progress and history.

> [!INFO] Key idea
> The master node coordinates scheduling and orchestration, while horizontal scaling happens by adding more worker nodes that consume tasks from the shared queue.
