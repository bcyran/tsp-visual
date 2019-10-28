import csv


def export_results(file, results):
    """Exports given list of results to a CSV file.

    :param str file: CSV file to write.
    :param list results: List of solver results.
    """

    with open(file, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Time [ns]', 'Best path', 'Best distance',
                         'Current path', 'Current distance'))
        for r in results:
            best_distance = r.best.distance if r.best else -1
            current_distance = r.current.distance if r.current else -1
            writer.writerow((r.time,
                             r.best.path if r.best else '',
                             best_distance,
                             r.current.path if r.current else '',
                             current_distance))
