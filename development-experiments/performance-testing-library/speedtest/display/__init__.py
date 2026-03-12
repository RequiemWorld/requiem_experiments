from .. import LoadRunResult
from tabulate import tabulate


def print_load_run_result(result: LoadRunResult):
    headers = ["executions", "errors", "minimum", "maximum", "p99.9999"]
    data = [
        [result.execution_count, result.error_count, result.minimum_execution_ms, result.maximum_execution_ms, result.percentile_99_9999],
    ]

    print(tabulate(data, headers=headers, tablefmt="grid"))
