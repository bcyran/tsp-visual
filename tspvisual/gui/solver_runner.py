import multiprocessing
import threading
import time

import wx
from pubsub import pub


class SolverRunner(threading.Thread):
    """Separate thread for running solver. It spawns SolverProcess, reads
    solver states from the queue respecting set delay and send pubsub messages
    to the GUI with new states.
    """

    def __init__(self, solver, tsp):
        """Creates new SolverRunner for given solver and TSP instance.

        :param Solver solver: TSP solver instance.
        :param TSP tsp: TSP instance.
        """

        threading.Thread.__init__(self)

        # Results queue
        self.results = multiprocessing.Queue()

        # Solver and TSP instance
        self._solver = solver
        self._tsp = tsp

        # Event signalling this thread to stop
        self._stop_event = threading.Event()

        # Delay between messages to GUI
        self.delay = 0

    def run(self):
        """Creates a process wich runs the solver.
        """

        # Start solver process
        self.solver_process = SolverProcess(
            self._solver, self._tsp, self.results)
        self.solver_process.start()

        # Start reading SolverState objects from the queue
        while not self._stop_event.is_set():
            state = self.results.get()

            # Send message with the new state to GUI
            wx.CallAfter(pub.sendMessage, 'SOLVER_STATE_CHANGE', state=state)

            # Break out of the loop if it's the final state
            if state.final:
                break

            # Sleep specified amount of itme
            time.sleep(self.delay)

        # Wait for the solver process
        self.solver_process.join()

    def stop(self):
        """Terminates the solver process.
        """

        self._stop_event.set()
        self.solver_process.stop()


class SolverProcess(multiprocessing.Process):
    """Separate process for running solver so it can have as much CPU power as
    it wants without interfering with GUI.
    """

    def __init__(self, solver, tsp, queue):
        multiprocessing.Process.__init__(self)

        # Queue for storing results
        self._solver = solver
        self._tsp = tsp
        self._queue = queue

        # Signal to stop the process
        self._stop_event = multiprocessing.Event()

    def run(self):
        """Runs the solver in loop, stops on event.
        """

        for state in self._solver.solve(self._tsp):
            self._queue.put_nowait(state)

            if self._stop_event.is_set():
                break

    def stop(self):
        """Sets the stop event.
        """

        self._stop_event.set()
