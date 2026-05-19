import asyncio
import inspect
from typing import Type, Callable, Union, Awaitable, Any, Dict, List, TypeVar, Generic
import logging
from src.events.base import DomainEvent
from src.enums.enums import EventType

logger = logging.getLogger(__name__)
E = TypeVar("E", bound=DomainEvent)

Handler = Union[
    Callable[[E], Awaitable[Any]],   # async handler
    Callable[[E], Any] 
]


class EventBus(Generic[E]):
    def __init__(self):
        self._subscribers: Dict[Type[E], List[Handler]] = {}

    def subscribe(self, event_type: Type[E], handler: Handler):
        self._subscribers.setdefault(event_type, []).append(handler)

    
    async def publish_event(self, event: E):
        handlers = self._subscribers.get(type(event), [])
        
        async_tasks = []
        sync_tasks = []

        for handler in handlers:
            if inspect.iscoroutinefunction(handler):
                async_tasks.append(handler(event))
            else:
                sync_tasks.append(handler)
        
        for handler in sync_tasks:
            try:
                handler(event)
            except Exception:
                logger.exception("Sync handler failed for event %s", event)
        
        if async_tasks:
            try:
                await self._run_async_handlers(async_tasks)
            except Exception:
                logger.exception("Error during async handler execution")

    async def _run_async_handlers(self, coros):
        await asyncio.gather(*coros, return_exceptions=True)

event_bus = EventBus()


