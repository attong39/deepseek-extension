"""Base classes for common initialization patterns.

This module provides base classes to reduce __init__ method duplication
across the codebase, following Clean Architecture principles. It includes
integrated logging, comprehensive type hints, and robust error handling.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar
import Exception
import RuntimeError
import ValueError
import bool
import default
import dependencies
import e
import getattr
import isinstance
import list
import name
import property
import self
import str
import type

logger = logging.getLogger(__name__)  # Local logger to avoid circular imports

T = TypeVar('T')  # Generic type for dependency retrieval


class BaseService(ABC):
    """Base class for services with zero-argument initialization.

    This class provides a common pattern for services that initialize
    without external dependencies, typically setting up internal state.
    It enforces implementation of the _setup method and includes logging
    for initialization tracking.

    Attributes:
        _initialized (bool): Flag indicating if the service is initialized.
        logger (logging.Logger): Project's standard logger instance.

    Example:
        class UserService(BaseService):
            def _setup(self) -> None:
                self._users = {}
                self.logger.info("UserService initialized.")
    """

    def __init__(self) -> None:
        """Initialize the service with default configuration.

        Raises:
            RuntimeError: If initialization fails due to setup errors.
        """
        self.logger = logger
        self._initialized = False
        try:
            self._setup()
            self._initialized = True
            self.logger.info(f"{self.__class__.__name__} initialized successfully.")
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Initialization failed for {self.__class__.__name__}") from e

    @abstractmethod
    def _setup(self) -> None:
        """Template method for service-specific setup.

        Subclasses must implement this method to perform service-specific
        initialization. This method is called during __init__ and should
        not raise exceptions unless critical.

        Raises:
            NotImplementedError: If not overridden in subclass.
        """
        pass

    @property
    def is_initialized(self) -> bool:
        """Check if service is properly initialized.

        Returns:
            bool: True if initialized, False otherwise.
        """
        return getattr(self, "_initialized", False)


class BaseDependentService(ABC):
    """Base class for services that require dependency injection.

    This class provides a common pattern for services that need
    external dependencies injected during initialization. It validates
    dependencies and includes logging for tracking.

    Attributes:
        _dependencies (Dict[str, Any]): Injected dependencies.
        _initialized (bool): Flag indicating if the service is initialized.
        logger (logging.Logger): Project's standard logger instance.

    Example:
        class PaymentService(BaseDependentService):
            def _setup(self) -> None:
                self._gateway = self.get_dependency("payment_gateway")
                if not self._gateway:
                    raise ValueError("Payment gateway dependency required.")
    """

    def __init__(self, **dependencies: Any) -> None:
        """Initialize service with injected dependencies.

        Args:
            **dependencies: Service dependencies to be injected. Must be non-empty.

        Raises:
            ValueError: If no dependencies are provided.
            RuntimeError: If initialization fails due to setup errors.
        """
        if not dependencies:
            raise ValueError("At least one dependency must be provided.")
        self.logger = logger
        self._dependencies = dependencies
        self._initialized = False
        try:
            self._setup()
            self._initialized = True
            self.logger.info(f"{self.__class__.__name__} initialized with dependencies: {list(dependencies.keys())}")
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Initialization failed for {self.__class__.__name__}") from e

    @abstractmethod
    def _setup(self) -> None:
        """Template method for service-specific setup.

        Subclasses must implement this method to perform service-specific
        initialization using injected dependencies.

        Raises:
            NotImplementedError: If not overridden in subclass.
        """
        pass

    def get_dependency(self, name: str, default: Optional[T] = None) -> Optional[T]:
        """Get an injected dependency by name.

        Args:
            name: Name of the dependency. Must be a non-empty string.
            default: Default value if dependency not found.

        Returns:
            The requested dependency or default value.

        Raises:
            ValueError: If name is empty or invalid.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Dependency name must be a non-empty string.")
        return self._dependencies.get(name, default)


class BaseRepository(ABC):
    """Base class for repository pattern implementations.

    This class provides a common pattern for repositories that manage
    data persistence and retrieval operations. It handles session management
    and includes logging.

    Attributes:
        _session (Any): Database session or connection object.
        _initialized (bool): Flag indicating if the repository is initialized.
        logger (logging.Logger): Project's standard logger instance.

    Example:
        class UserRepository(BaseRepository):
            def _setup(self) -> None:
                if not self._session:
                    raise ValueError("Database session required.")
                self.logger.info("UserRepository connected to database.")
    """

    def __init__(self, session: Optional[Any] = None) -> None:
        """Initialize repository with optional session.

        Args:
            session: Database session or connection object. If None, subclasses
                     must handle session creation in _setup.

        Raises:
            RuntimeError: If initialization fails due to setup errors.
        """
        self.logger = logger
        self._session = session
        self._initialized = False
        try:
            self._setup()
            self._initialized = True
            self.logger.info(f"{self.__class__.__name__} initialized with session: {session is not None}")
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Initialization failed for {self.__class__.__name__}") from e

    @abstractmethod
    def _setup(self) -> None:
        """Template method for repository-specific setup.

        Subclasses must implement this method to perform repository-specific
        initialization, such as validating the session.

        Raises:
            NotImplementedError: If not overridden in subclass.
        """
        pass

    @property
    def session(self) -> Optional[Any]:
        """Get the current session.

        Returns:
            The current session object or None.
        """
        return self._session


class BaseEntity:
    """Base class for simple entities with minimal initialization.

    This class provides a common pattern for entities that only need
    basic initialization without complex setup. Entities are distinguished
    by their identity rather than attributes. Subclasses should implement
    business logic and validation rules.

    Attributes:
        _created (bool): Flag indicating if the entity was created.
        logger (logging.Logger): Project's standard logger instance.

    Example:
        class User(BaseEntity):
            def __init__(self, user_id: str):
                super().__init__()
                if not user_id:
                    raise ValueError("User ID cannot be empty.")
                self.user_id = user_id
                self.logger.info(f"User entity created with ID: {user_id}")
    """

    def __init__(self) -> None:
        """Initialize entity with default state.

        Raises:
            RuntimeError: If initialization fails.
        """
        self.logger = logger
        self._created = False
        try:
            # Minimal setup for entities
            self._created = True
            self.logger.debug(f"{self.__class__.__name__} entity created.")
        except Exception as e:
            self.logger.error(f"Failed to create {self.__class__.__name__} entity: {e}")
            raise RuntimeError(f"Entity creation failed for {self.__class__.__name__}") from e

    @property
    def is_created(self) -> bool:
        """Check if entity was properly created.

        Returns:
            bool: True if created, False otherwise.
        """
        return getattr(self, "_created", False)


class BaseManager:
    """Base class for manager objects that coordinate operations.

    This class provides a common pattern for managers that orchestrate
    multiple services or handle complex workflows. It supports context
    manager protocol for safe activation/deactivation.

    Attributes:
        _active (bool): Flag indicating if the manager is active.
        _initialized (bool): Flag indicating if the manager is initialized.
        logger (logging.Logger): Project's standard logger instance.

    Example:
        class OrderManager(BaseManager):
            def __init__(self, order_service: OrderService):
                super().__init__()
                self._order_service = order_service

            def process_order(self, order: Order) -> None:
                with self:  # Uses context manager
                    self._order_service.validate(order)
                    self._order_service.process(order)
    """

    def __init__(self) -> None:
        """Initialize manager with default state.

        Raises:
            RuntimeError: If initialization fails due to setup errors.
        """
        self.logger = logger
        self._active = False
        self._initialized = False
        try:
            self._setup()
            self._initialized = True
            self.logger.info(f"{self.__class__.__name__} initialized.")
        except Exception as e:
            self.logger.error(f"Failed to initialize {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Initialization failed for {self.__class__.__name__}") from e

    @abstractmethod
    def _setup(self) -> None:
        """Template method for manager-specific setup.

        Subclasses must implement this method to perform manager-specific
        initialization.

        Raises:
            NotImplementedError: If not overridden in subclass.
        """
        pass

    @property
    def is_active(self) -> bool:
        """Check if manager is active.

        Returns:
            bool: True if active, False otherwise.
        """
        return self._active

    def activate(self) -> None:
        """Activate the manager.

        Raises:
            RuntimeError: If activation fails.
        """
        try:
            self._active = True
            self.logger.info(f"{self.__class__.__name__} activated.")
        except Exception as e:
            self.logger.error(f"Failed to activate {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Activation failed for {self.__class__.__name__}") from e

    def deactivate(self) -> None:
        """Deactivate the manager.

        Raises:
            RuntimeError: If deactivation fails.
        """
        try:
            self._active = False
            self.logger.info(f"{self.__class__.__name__} deactivated.")
        except Exception as e:
            self.logger.error(f"Failed to deactivate {self.__class__.__name__}: {e}")
            raise RuntimeError(f"Deactivation failed for {self.__class__.__name__}") from e

    def __enter__(self) -> BaseManager:
        """Enter context manager, activating the manager.

        Returns:
            Self for use in with statement.
        """
        self.activate()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        """Exit context manager, deactivating the manager.

        Args:
            exc_type: Exception type if raised.
            exc_val: Exception value if raised.
            exc_tb: Exception traceback if raised.
        """
        self.deactivate()
