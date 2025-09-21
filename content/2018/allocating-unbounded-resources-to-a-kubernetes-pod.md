Title: Allocating unbounded resources to a kubernetes pod
Date: 2018-09-29
Category: Programming

Note: this article assumes that the reader is familiar with [Kubernetes](https://kubernetes.io) and Linux [cgroups](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/resource_management_guide/ch01).

---

When deploying a pod in a Kubernetes cluster, you normally have 2 choices when it comes to [resources](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container) allotment:

- defining CPU/memory resource requests and limits [at the pod level](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#resource-requests-and-limits-of-pod-and-container)
- defining default CPU/memory requests and limits at the [namespace level](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/) using a `LimitRange`

However, what if circumstances allowed you to allocate unbounded resources to your pod? While that would go against the idea of bin-packing pods by using resource bounded cgroups, it could still useful if you ran no other pods that the unbounded one on your node. In that case, wouldn't be interested in protecting your pod against any noisy neighbour, and you'd want it to be able to use all the available node resources.

This (while not strictly documented) can be accomplished by using the following resource limits and requests:

```
resources:
  limits:
    cpu: 0
    memory: 0
  requests:
    cpu: 0
    memory: 0
```

In our case, we also have a defined `LimitRange` in our namespace, so we want to make sure that our request for unbounded resources does not get overridden by the default values.

```
$ kubectl describe limitrange my-limit-range
Name:       my-limit-range
Namespace:  default
Type        Resource  Min  Max  Default Request  Default Limit
----        --------  ---  ---  ---------------  -------------
Container   memory    -    -    512Mi            1Gi
Container   cpu       -    -    500m             1

$ kubectl get pod my-pod -o jsonpath='{.spec.containers[0].resources}'
map[limits:map[cpu:0 memory:0] requests:map[cpu:0 memory:0]]
```

It seems that the `LimitRange` has not overridden our request. However, we see a different picture when we inspect the node running our pod:

```
$ kubectl get pod my-pod -o jsonpath='{.spec.nodeName}'
my-node
$ kubectl describe node my-node
...
Non-terminated Pods:         (6 in total)
  Namespace    Name     CPU Requests  CPU Limits  Memory Requests  Memory Limits
  ---------    ----     ------------  ----------  ---------------  -------------
  datadog      my-pod   500m (13%)    1 (26%)     512Mi (2%)       1Gi (4%)
...
```

Who should we believe? When different parts of the control plane disagree on the resource allotment, there's really one place to get the truth from: the container cgroup itself.

To do so, we need to exec into the pod, and inspect the CPU quota and memory limit values.

```
$ kubectl exec -it my-pod
user@my-pod:/$ cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us
-1
```

As detailed on the [Linux kernel documentation](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt), or the Red Hat [documentation portal](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/resource_management_guide/sec-cpu)

> A value of -1 for `cpu.cfs_quota_us` indicates that the group does not have any
bandwidth restriction in place, such a group is described as an unconstrained
bandwidth group.  This represents the traditional work-conserving behavior for
CFS.

Now, the memory.

```
user@my-pod:/$ cat /sys/fs/cgroup/memory/memory.limit_in_bytes
9223372036854771712
```

That looks odd. This would indicate that the process has a limit of ... 8191TB of memory!

Digging [a bit further](https://unix.stackexchange.com/questions/420906/what-is-the-value-for-the-cgroups-limit-in-bytes-if-the-memory-is-not-restricte), we learn that `9223372036854771712` is a kind of "magic" number in the memory management layer of the kernel, meaning that the process gets unbounded memory.

## Conclusion
Looking at the cgroup itself showed that a value of `0` for cpu/memory requests/limits is not intercepted by the `LimitRange` in place, and is translated to an unbounded cgroup in the end. It also showed that the pod resource requests and limits reported at the node level are inaccurate.