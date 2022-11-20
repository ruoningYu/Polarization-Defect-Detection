# Copyright (c) OpenMMLab. All rights reserved.
import inspect
import threading
from collections import OrderedDict
from typing import Type, TypeVar

_lock = threading.RLock()
T = TypeVar('T')


def _accquire_lock() -> None:
    """Acquire the module-level lock for serializing access to shared data.

    This should be released with _release_lock().
    """
    if _lock:
        _lock.acquire()


def _release_lock() -> None:
    """Release the module-level lock acquired by calling _accquire_lock()."""
    if _lock:
        _lock.release()


class ManagerMeta(type):

    def __init__(cls, *args):
        cls._instance_dict = OrderedDict()
        params = inspect.getfullargspec(cls)
        params_names = params[0] if params[0] else []
        assert 'name' in params_names, f'{cls} must have the `name` argument'
        super().__init__(*args)


class ManagerMixin(metaclass=ManagerMeta):

    def __init__(self, name: str = '', **kwargs):
        assert isinstance(name, str) and name, \
            'name argument must be an non-empty string.'
        self._instance_name = name

    @classmethod
    def get_instance(cls: Type[T], name: str, **kwargs) -> T:

        _accquire_lock()
        assert isinstance(name, str), \
            f'type of name should be str, but got {type(cls)}'
        instance_dict = cls._instance_dict  # type: ignore
        # Get the instance by name.
        if name not in instance_dict:
            instance = cls(name=name, **kwargs)  # type: ignore
            instance_dict[name] = instance  # type: ignore
        else:
            assert not kwargs, (
                f'{cls} instance named of {name} has been created, the method '
                '`get_instance` should not access any other arguments')
        # Get latest instantiated instance or root instance.
        _release_lock()
        return instance_dict[name]

    @classmethod
    def get_current_instance(cls):

        _accquire_lock()
        if not cls._instance_dict:
            raise RuntimeError(
                f'Before calling {cls.__name__}.get_current_instance(), you '
                'should call get_instance(name=xxx) at least once.')
        name = next(iter(reversed(cls._instance_dict)))
        _release_lock()
        return cls._instance_dict[name]

    @classmethod
    def check_instance_created(cls, name: str) -> bool:
        """Check whether the name corresponding instance exists.

        Args:
            name (str): Name of instance.

        Returns:
            bool: Whether the name corresponding instance exists.
        """
        return name in cls._instance_dict

    @property
    def instance_name(self) -> str:
        """Get the name of instance.

        Returns:
            str: Name of instance.
        """
        return self._instance_name
