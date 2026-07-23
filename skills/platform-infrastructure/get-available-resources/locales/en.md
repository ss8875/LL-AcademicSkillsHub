# Get Available Resources

This skill should be used at the start of any computationally intensive scientific task to detect and report available system resources (CPU cores, GPUs, memory, disk space). It creates a JSON file with resource information and strategic recommendations that inform computational approach decisions such as whether to use parallel processing (joblib, multiprocessing), out-of-core computing (Dask, Zarr), GPU acceleration (PyTorch, JAX), or memory-efficient strategies. Use this skill before running analyses, training models, processing large datasets, or any task where resource constraints matter.

## Main capabilities

- Inspect runtime resources and dependencies
- Organize compute and platform configuration
- Record environment limits and reproducibility conditions

## Inputs

- Execution goal, resource needs, and environment information

## Outputs

- Environment reports, deployment configuration, or run results

## Local-use note

Read the root `SKILL.md` and its referenced files first, then check the catalog record for runtime, credential, network, risk, and license status. This profile does not replace upstream instructions for third-party skills.

Quality status: `cataloged`; source kind: `pinned-third-party`.
