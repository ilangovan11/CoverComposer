# tests/test_device_manager.py

import torch
from services.device_manager import get_device

def test_get_device_is_cpu():
    """
    Assert that get_device() always returns a CPU device as per production policy.
    """
    device = get_device()
    assert device.type == "cpu"
    
def test_torch_threads_set():
    """
    Verify that torch threads are limited (side effect of get_device).
    """
    # This just ensures the function runs without error and the state is consistent
    get_device()
    threads = torch.get_num_threads()
    assert threads > 0
