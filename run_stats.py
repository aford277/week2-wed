"""
run_stats.py -- statistics helpers for a nightly test-run report.

The QE team uses these functions to turn raw results and timings into the
numbers on the morning dashboard. The dashboard numbers are wrong.
Your job in Part A is to find out why. (Open the tickets in README.md.)

Data shapes used here:
  results    a list of dicts like {"test": "t1", "suite": "login", "status": "pass"}
             status is one of "pass", "fail", "skip"
  durations  a list of test durations in milliseconds, in the order they ran

Written lessons that help: debugging-techniques.md, mutability-and-memory.md,
scope-and-namespaces.md, built-in-python-functions.md.
"""
import logging

logger = logging.getLogger(__name__)

run_counter = 0

def next_run_id():
    """Return a new id for each report: "RUN-0001", "RUN-0002", ...

    The counter lives at module level so ids keep increasing for as long as
    the program runs.
    """
    global run_counter
    run_counter += 1
    result = f"RUN-{run_counter:04d}"
    logger.debug("test id when there have been %d test cases = %s", run_counter, result)
    return result


def median(values):
    """Median (middle value) of a list of numbers.

    Odd count: the middle value of the sorted numbers.
    Even count: the mean of the two middle values of the sorted numbers.
    Empty list: raise ValueError("median() needs at least one value").
    """
    if not values:
        raise ValueError("median() needs at least one value")
    ordered = sorted(values)
    if len(ordered) % 2 != 0:
        result = ordered[len(ordered) // 2]
    else:
        result = (ordered[len(ordered) // 2] + ordered[(len(ordered) // 2) - 1]) / 2
    logger.debug("median of %d values = %s", len(ordered), result)
    return result


def slowest(durations, n):
    """Return the n largest durations, biggest first.

    If there are fewer than n durations, return them all.
    n == 0 returns an empty list.
    The caller's list must not be changed.
    """
    sorted_durations = sorted(durations, reverse=True)
    if len(sorted_durations) < n:
        result = sorted_durations
    elif n == 0:
        result = []
    else:
        result = sorted_durations[:n]
    logger.debug("slowest of %d values = %s", len(durations) if durations else 0, str(result))
    return result
    


def group_by_suite(results):
    """Count outcomes per suite.

    Returns a dict of dicts, for example:
        {"login": {"pass": 2, "fail": 1}, "search": {"pass": 1}}
    A status that never happened in a suite is simply absent (no zero entries).
    A result with no "suite" key is counted under the suite name "unknown".
    """
    grouped = {}
    for result in results:
        if "suite" not in result:
            logger.warning("%s has no 'suite', marking as unknown", str(result))
        suite = result.get("suite", "unknown")
        status = result["status"]
        if suite not in grouped:
            grouped[suite] = {}
        grouped[suite][status] = grouped[suite].get(status, 0) + 1
    return grouped


def note_flaky(test_name, flaky=None):
    """Add test_name to a list of flaky tests and return that list.

    If the caller passes its own list, add to that list.
    If the caller passes nothing, start a NEW empty list for this call.
    """
    if flaky is None:
        flaky = []
    flaky.append(test_name)
    logger.info("%s flagged, %d flagged in total", test_name, len(flaky))
    return flaky


def summarise_run(results, durations):
    """Build the summary dict that the dashboard shows.

    Keys:
      run_id      from next_run_id()
      total       number of results
      by_suite    from group_by_suite(results)
      median_ms   median of durations, or None if there are no durations
      slowest_ms  the 3 slowest durations, biggest first
      latest_ms   the duration of the most recent test (the LAST item
                  of durations as it was passed in)
    """
    summary = {
        "run_id": next_run_id(),
        "total": len(results),
        "by_suite": group_by_suite(results),
        "median_ms": median(durations) if durations else None,
        "slowest_ms": slowest(durations, 3),
        "latest_ms": durations[-1] if durations else None,
    }
    logger.info("got summary, id: %s, number of results: %d, number of suites: %d", summary["run_id"], summary["total"], len(summary["by_suite"]))
    return summary
