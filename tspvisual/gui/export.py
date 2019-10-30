import csv
import os

from tspvisual.tsplib import TSPLibTour


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


def export_tour(file, path, tsp):
    """Exports given path to TSPLIB .tour file.

    :param str file: Destination file.
    :param Path path: Path to export.
    :param TSP tsp: TSP instance in which exported Path is found.
    """

    tour = TSPLibTour.from_path(path)
    tour.specification['TYPE'] = 'TOUR'
    tour.specification['DIMENSION'] = tsp.specification['DIMENSION']
    tour.specification['COMMENT'] = 'Path in {} instance.'\
        .format(tsp.specification['NAME'])
    tour.specification['NAME'] = os.path.basename(file)
    tour.write(file)
