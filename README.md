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

### Manually via Docker run

```
docker run --rm -it -v ~/.kube:/root/.kube \
smbambling/check-kubernetes-cronjobs:latest --namespace default
```

### `check_kubernetes_cronjobs.sh` Shell Script

```bash
$ ./check_kubernetes_cronjobs.sh -n stage -v latest
OK: [0/0] CronJobs ran successfully in Kubernetes Namespace = default
```

```bash
$ ./check_kubernetes_cronjobs.sh --help
Usage: ./check_kubernetes_cronjobs.sh -k -n
where:
    -k Kubeconfig
      [default: /Users/smbambling/.kube/config]
    -n Kubernetes Namespace {required}
    -v check-kubernetes-cronjobs Docker image version
      [default: latest]
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

### Overview

1. Create feature branch of master
1. Make updates in feature branch
1. Create pull request (PR) from feature branch into master
1. Feature branch merged into master
1. Build **latest** artifact (Docker image)
1. Testing is performed on the **latest** artifact
1. Master branch is 'released' into stable
  1. Bump version
  1. Build artifact (Docker image)
  1. Tag + Push artifact (Docker image)
  1. Tag `master` branch
  1. Merge `master` branch into `stable`
  1. Push `master` + `stable` branches

To aid in the build and release steps for development the utility `develop.sh` is used.

To build the **latest** artifact (Docker image) from your current branch pass the `-b` argument 

```bash 
./develop.sh -b
```

To release a tested version of the artifact (Docker image) from the `master` branch pass the `-r` argument with an optional `-v` argument to bump a specific patch level

```bash
./develop.sh -r
```
```bash
$ ./develop.sh --help
Usage: ./develop.sh -b|-r -v
where:
    -b Build Docker image
    -r Build+Release Docker iamge
    -v Version bump level { major, minor, patch(default) 
```

### Branching

See the [BRANCHING.md](./docs/BRANCHING.md) file for details

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/smbambling/check-kubernetes-cronjobs/tags). 

## Authors

* **Steven Bambling** - *Initial work*

See also the list of [contributors](https://github.com/smbambling/check-kubernetes-cronjobs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details
