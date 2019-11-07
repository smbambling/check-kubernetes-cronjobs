#!/usr/bin/env python
"""
Check failed Kubernets CronJobs
"""

# Import Standard Modules
import argparse
import logging
import sys
from operator import itemgetter


try:
    from kubernetes import config
    import kubernetes.config
    import kubernetes.client
    from kubernetes.client.rest import ApiException
except ImportError:
    print("Please install kubernetes:")
    print("$ sudo pip install kubernetes")
    sys.exit(3)


try:
    from prettytable import PrettyTable
except ImportError:
    print("Please install prettytable:")
    print("$ sudo pip install prettytable")
    sys.exit(3)


def kube_test_credentials():
    """
    Testing function.
    If you get an error on this call don't proceed.
    Something is wrong on your connectivty to K8s API.
    Check Credentials, permissions, keys, etc.
    """
    try:
        api_instance.get_api_resources()
    except ApiException as e:
        print("Exception when calling API: %s\n" % e)


def get_jobs(namespace=None):
    jobs = {}

    try:
        data = api_instance.list_namespaced_job(namespace=namespace,
                                                pretty=True,
                                                watch=False,
                                                timeout_seconds=60)
    except ApiException as e:
        print("Exception when calling \
BatchV1Api->list_namespaced_job: %s\n" % e)

    for item in data.items:
        cronjob_name = None

        # Determine job name from CronJob name, skip non CronJob jobs
        if item.metadata.owner_references:
            owner_reference = item.metadata.owner_references[0]
            if owner_reference.kind == "CronJob":
                cronjob_name = owner_reference.name
                job_name = item.metadata.name

        if not cronjob_name:
            continue

        if item.status.start_time:
            start_timestamp = item.status.start_time. \
                                  strftime("%m/%d/%Y %H:%M:%S")
        else:
            # Skip because the job is created, but not started yet
            continue

        cronjob_namespace = item.metadata.namespace

        if cronjob_name not in jobs:
            jobs[cronjob_name] = {}

        if item.status.completion_time:
            end_timestamp = item.status.completion_time. \
                                strftime("%m/%d/%Y %H:%M:%S")
        else:
            end_timestamp = None

        if item.status.succeeded == 1:
            status = "succeeded"
        elif item.status.failed == 1:
            status = "failed"
            try:
                end_timestamp = item.status.conditions[0]. \
                                    last_transition_time. \
                                    strftime("%m/%d/%Y %H:%M:%S")
            except (TypeError, KeyError):
                pass
        else:
            status = "unknown"

        if item.status.active == 1:
            active = True
            status = "running"
        else:
            active = False

        jobs[cronjob_name] = {
            "job_name": job_name,
            "cronjob_name": cronjob_name,
            "cronjob_namespace": cronjob_namespace,
            "start_timestamp": start_timestamp,
            "status": status,
            "active": active
        }
        if end_timestamp:
            jobs[cronjob_name]["end_timestamp"] = end_timestamp

    return jobs


def main(args, loglevel):
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)

    global configuration
    global api_instance
    config.load_kube_config(config_file=args.kubeconfig)
    configuration = kubernetes.client.Configuration()
    api_instance = kubernetes.client.BatchV1Api(
        kubernetes.client.ApiClient(configuration))

    # kube_test_credentials()
    jobs = get_jobs(namespace=args.namespace)
    failed_jobs = []
    count_total_jobs = len(jobs)

    for key, job in jobs.items():
        if job["status"] == "failed":
            failed_jobs.append(job["cronjob_name"])
        # Remove succeeded Cronjobs unless verbose output
        # called with -v(v)(v)
        elif (loglevel >= 30 and job["status"] == "succeeded"):
            jobs.pop(key)

    sorted_jobs = sorted(jobs.values(), key=itemgetter("status"))

    table = PrettyTable(["CronJob", "Start", "Finish", "Status"])
    for job in sorted_jobs:
        table.add_row([job["cronjob_name"], job["start_timestamp"],
                       job["end_timestamp"], job["status"]])

    if failed_jobs:
        count_failed_jobs = len(failed_jobs)
        print("CRITICAL:[{count_failed_jobs}/{count_total_jobs}] CronJobs \
failed in Kubernetes Namespace = {args.namespace} \n".format(**locals()))
        print(table)
        exit(2)
    else:
        print("OK: [{count_total_jobs}/{count_total_jobs}] CronJobs \
ran successfully in Kubernetes Namespace = \
{args.namespace} \n".format(**locals()))
        if loglevel < 30:
            print(table)
        exit(0)


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Check failed Kubernets CronJobs",
        epilog=""
    )
    parser.add_argument(
        "--kubeconfig",
        type=str,
        required=False,
        default="~/.kube/config",
        help="Kubeconfig File",
        metavar="kubeconfig"
    )
    parser.add_argument(
        "--namespace",
        type=str,
        required=True,
        help="Kubernetes Namesapce",
        metavar="namespace"
    )
    loglevel_group = parser.add_mutually_exclusive_group(required=False)
    loglevel_group.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="count",
        default=0)
    loglevel_group.add_argument(
        "-q",
        "--quiet",
        help="decrease output verbosity",
        action="count",
        default=0)
    args = parser.parse_args()

    # Setup logging
    # script -vv -> DEBUG or 50
    # script -v -> INFO or 40
    # script -> WARNING or 30
    # script -q -> ERROR or 20
    # script -qq -> CRITICAL or 10
    # script -qqq -> no logging at all
    loglevel = logging.WARNING + 10*args.quiet - 10*args.verbose
    # Set 'max'/'min' levels for logging
    if loglevel > 50:
        loglevel = 50
    elif loglevel < 10:
        loglevel = 10

    main(args, loglevel)
