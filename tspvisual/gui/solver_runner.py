import time
from threading import Event, Thread

import wx
from pubsub import pub


class SolverRunner(Thread):
    """Separate thread for running solver without interfering with other tasks.
    This thread regularly sends pubsub messages with new solver state.
    """

    def __init__(self, solver, tsp):
        """Creates new SolverRunner for given solver and TSP instance.

        :param Solver solver: TSP solver instance.
        :param TSP tsp: TSP instance.
        """

        Thread.__init__(self)

        # Solver and TSP instance
        self._solver = solver
        self._tsp = tsp

        # Event signalling thread to stop
        self._stop_event = Event()

        # Delay between solver iterations
        self.delay = 0
        # Limit of solver state messages per second
        self.message_limit = 60

    def run(self):
        """Runs the solver in step mode and publishes new states.
        """

        # Time after next message can be sent
        next_message_time = time.time()

        # Run the solver
        state = None
        for state in self._solver.solve(self._tsp):
            # Stop the solver is stop event is set
            if self._stop_event.is_set():
                return

            # Send message if it's the time
            if time.time() > next_message_time:
                wx.CallAfter(pub.sendMessage, 'SOLVER_STATE_CHANGE',
                             state=state)
                next_message_time = time.time() + 1 / self.message_limit

            # Sleep for spcified time
            time.sleep(self.delay)

        # Always send message about the final state
        wx.CallAfter(pub.sendMessage, 'SOLVER_STATE_CHANGE', state=state)

    def stop(self):
        """Sets the stop event in the thread causing it to end.
        """

        self._stop_event.set()
