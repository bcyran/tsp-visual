import csv


def export_results(file, results):
    """Exports given list of results to a CSV file.

    :param str file: CSV file to write.
    :param list results: List of solver results.
    """

    with open(file, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Time [ns]', 'Best distance', 'Current distance'))
        for r in results:
            best_distance = r.best.distance if r.best else -1
            current_distance = r.current.distance if r.current else -1
            writer.writerow((r.time, best_distance, current_distance))
