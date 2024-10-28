"""Test QtInProcessKernel"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import unittest
import inspect
import asyncio
from qtconsole.inprocess import QtInProcessKernelManager
import ipykernel


class InProcessTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Open an in-process kernel."""
        self.kernel_manager = QtInProcessKernelManager()
        if ipykernel.version_info >= (7,):
            self.task = asyncio.create_task(self.kernel_manager.start_kernel())
        else:
            self.kernel_manager.start_kernel()
        self.kernel_client = self.kernel_manager.client()

    async def asyncTearDown(self):
        """Shutdown the in-process kernel. """
        self.kernel_client.stop_channels()
        self.kernel_manager.shutdown_kernel()
        await self.task

    async def test_execute(self):
        """Test execution of shell commands."""
        # check that closed works as expected
        assert not self.kernel_client.iopub_channel.closed()
        
        # check that running code works
        await self.kernel_client.execute("a=1")
        assert self.kernel_manager.kernel is not None
        assert self.kernel_manager.kernel.shell.user_ns.get('a') == 1
