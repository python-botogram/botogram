# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

import collections
import hashlib


def _is_inline_update(job):
    """This returns true if the job contains an inline update"""
    if not job.metadata.get('update'):
        return False
    return job.metadata["update"].inline_query


def _inline_assign_worker(update, workers_number):
    """Internal assignment of workers for handling inline updates"""
    # The same query from the same sender will be handled by the same worker
    # this will avoid pagination issues
    return (update.inline_query.sender.id +
            int(hashlib.md5(update.inline_query.query.encode())
                .hexdigest()[-3:], 16)) % workers_number


class JobsCommands:
    """This object will manage the IPC jobs.* commands"""

    def __init__(self):
        self.queue = collections.deque()
        self.waiting = dict()

        self._seen_workers = list()

        self.stop = False

    def _put(self, job):
        """Internal implementation of putting a job into the queue"""
        # Directly send the job to the processes wanting it

        if len(self.waiting) > 0:
            if _is_inline_update(job):
                update = job.metadata["update"]
                worker_id = _inline_assign_worker(update,
                                                  len(self._seen_workers))
                if worker_id not in self.waiting:
                    self.queue.appendleft(job)
                    return
            else:
                worker_id = list(self.waiting)[0]
            try:
                self.waiting[worker_id](job)
                del self.waiting[worker_id]
            except EOFError:
                pass
            else:
                return
        self.queue.appendleft(job)

    def bulk_put(self, jobs, reply):
        """Put multiple jobs in the queue"""
        if self.stop:
            reply("No more jobs accepted", ok=False)

        # Add each provided job
        for job in jobs:
            self._put(job)
        reply(None)

    def get(self, worker_id, reply):
        """Get a job from the queue"""
        def _reply_with(_job_id):
            """Reply to a jobs.get request with a job"""
            _job = self.queue[_job_id]
            del self.queue[_job_id]
            reply(_job)

        if worker_id not in self._seen_workers:
            self._seen_workers.append(worker_id)

        # If there is something in the queue return it, else append the request
        # to the new jobs' waiting deque
        if len(self.queue) > 0:
            for job_id in range(len(self.queue)):
                job = self.queue[job_id]
                # If the job is an inline update assign it
                # to the designated worker
                if _is_inline_update(job):
                    assigned_worker = _inline_assign_worker(
                        job.metadata["update"],
                        len(self._seen_workers)
                    )
                    if worker_id == assigned_worker:
                        return _reply_with(job_id)
                    continue
                return _reply_with(job_id)

        if self.stop:
            reply("__stop__")

        self.waiting[worker_id] = reply

    def shutdown(self, _, reply):
        """Shutdown the queue"""
        self.stop = True

        # Stop all the waiting workers
        if len(self.waiting) > 0:
            for worker in self.waiting:
                self.waiting[worker]("__stop__")

        reply(None)


class Job:
    """A job processed by workers"""

    def __init__(self, bot_id, func, metadata):
        self.bot_id = bot_id
        self.func = func
        self.metadata = metadata

    def process(self, bots):
        bot = bots[self.bot_id]
        return self.func(bot, self.metadata)


def process_update(bot, metadata):
    """Process an update received from Telegram"""
    update = metadata["update"]

    # Restore the removed API object
    update.set_api(bot.api)
    bot.process(update)


def process_task(bot, metadata):
    """Process a generic task"""
    task = metadata["task"]
    bot.logger.debug("Processing task %s..." % task.hook.name)

    task.process(bot)
