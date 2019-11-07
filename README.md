# Check-Kubernetes-CronJobs

## Table of Contents

1. [Overview](#overview)
1. [Usage](#usage)
1. [Development](#development)
1. [Versioning](#versioning)
1. [Authors](#authors)
1. [License](#license)

## Overview

Dockerized Python Utility To Check The Status Of Kubernetes CronJobs

## Usage

```
docker run --rm -it -v ~/.kube:/root/.kube \
smbambling/check-kubernetes-cronjobs:1.0.0 --namespace stage
```

### Example Output

Normal output when 1 or more CronJobs have failed

```
CRITICAL:[1/2] CronJobs failed in Kubernetes Namespace = default

+-------------+---------------------+---------------------+--------+
|   CronJob   |        Start        |        Finish       | Status |
+-------------+---------------------+---------------------+--------+
| delete-orgs | 10/31/2019 11:00:04 | 10/31/2019 11:04:13 | failed |
+-------------+---------------------+---------------------+--------+
```

Verbose output when 1 or more CronJobs have failed

 * Note: Failed jobs will be sorted at the top of the table

```
CRITICAL:[1/2] CronJobs failed in Kubernetes Namespace = default

+------------------+---------------------+---------------------+-----------+
|     CronJob      |        Start        |        Finish       |   Status  |
+------------------+---------------------+---------------------+-----------+
|   delete-orgs    | 10/31/2019 11:00:04 | 10/31/2019 11:04:13 |   failed  |
| delete-customers | 10/31/2019 11:00:04 | 10/31/2019 11:02:42 | succeeded |
+------------------+---------------------+---------------------+-----------+
```

Normal output when ALL CronJobs have succeeded

```
OK: [1/1] CronJobs ran successfully in Kubernetes Namespace = default
```

Verbose output when ALL CronJobs have succeeded

```
OK: [1/1] CronJobs ran successfully in Kubernetes Namespace = default

+------------------+---------------------+---------------------+-----------+
|     CronJob      |        Start        |        Finish       |   Status  |
+------------------+---------------------+---------------------+-----------+
| delete-customers | 10/31/2019 11:00:03 | 10/31/2019 11:02:41 | succeeded |
+------------------+---------------------+---------------------+-----------+
```

## Development

References:
  [branching-strategy](https://github.com/mobify/branching-strategy/blob/master/release-deployment.md)


## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/smbambling/check-kubernetes-cronjobs/tags). 

## Authors

* **Steven Bambling** - *Initial work*

See also the list of [contributors](https://github.com/smbambling/check-kubernetes-cronjobs/contributors) who participated in this project.

## License
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details