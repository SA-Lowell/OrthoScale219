"""
    Configuration file for pytest in OrthoScale219 testing.
    
    This conftest.py file defines pytest fixtures for managing the OrthoScale219 add-on during end-to-end (E2E) testing sessions.
    It automates the installation and disabling of the add-on to ensure a clean testing environment.
    
    Fixtures:
        manage_addons: Session-scoped fixture for handling add-on lifecycle.
    
    Notes:
        Requires Blender's Python environment with pytest installed.
        Uses helper fixtures install_addons_from_dir and disable_addons provided by the pytest-blender plugin.
        This file is automatically discovered by pytest when running tests in the root ortho_Scale_219 directory.
    
    Author: S.A. Lowell
    Version: 2.1.9+109092.1756709219
"""
import os
from typing import Callable, List
import pytest

@pytest.fixture(
    scope = "session",
    autouse = True,
)

def manage_addons(install_addons_from_dir:Callable[..., List[str]], disable_addons:Callable[[List[str]], None]):
    """
        Fixture to manage the installation and disabling of the OrthoScale219 add-on for the test session.
        
        This session-scoped fixture automatically installs the OrthoScale219 add-on from the parent directory at the start of the
        testing session and disables it at the end. It uses provided callable helpers for installation and disabling, ensuring
        the add-on is active only during tests for isolation and cleanup.
        
        Args:
            install_addons_from_dir (Callable[..., List[str]]): A callable that installs add-ons from a directory and returns a
                list of installed add-on IDs.
            disable_addons (Callable[[List[str]], None]): A callable that disables a list of add-on IDs.
        
        Yields:
            None: Yields control back to the test session after installation, allowing tests to run with the add-on enabled.
        
        Notes:
            The fixture determines the parent directory and add-on name dynamically based on the current working directory. It is
            autouse=True, so it runs automatically for all tests in the session without needing explicit invocation. Errors
            during installation or disabling may propagate from the helper callables.
    """
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(tests_dir)
    parent_dir = os.path.dirname(repo_root)
    #addon_name = os.path.basename(repo_root)
    
    addons_ids: List[str] = install_addons_from_dir(
        parent_dir,
        #addons_ids = [addon_name],
    )
    
    yield
    
    disable_addons(addons_ids)
