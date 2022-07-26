import asyncio
import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from typing import Protocol

from event import Event, EventType


class Subscriber(Protocol):
    async def listen(self, event: Event) -> None:
        raise NotImplementedError


@dataclass(kw_only=True, slots=True)
class Topic:
    name: str
    subscribers: list[Subscriber] = field(default_factory=list)
    events: deque[Event] = field(default_factory=deque)

    def __init__(self, name: str):
        self.name = name
        self.subscribers = []
        self.events = deque()
        loop_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        loop_thread.start()

    def register_subscriber(self, subscriber: Subscriber) -> None:
        self.subscribers.append(subscriber)

    def publish(self, event: Event) -> None:
        self.events.append(event)

    def _broadcast_loop(self) -> None:
        loop = asyncio.new_event_loop()
        loop.create_task(self._broadcast_event())
        loop.run_forever()

    async def _broadcast_event(self) -> None:
        while True:
            # print("loop")
            if len(self.events) > 0:
                print("remaining events:", len(self.events))
                event = self.events.popleft()
                task_list = [
                    subscriber.listen(event) for subscriber in self.subscribers
                ]
                results = await asyncio.gather(*task_list, return_exceptions=True)
                for idx, res in enumerate(results):
                    if isinstance(res, Exception):
                        print(f"Error in subscriber {idx}: {res}")
            time.sleep(0.1)

        # asyncio.set_event_loop(loop)

    async def test(self, event: Event):
        print("test1", event.id)
        await asyncio.sleep(5)
        if event.message["dice_1"] == 3:
            raise Exception("dllm")
        print("test2", event.id)


class Publisher(ABC):
    topic: Topic

    def register_topic(self, topic: Topic) -> None:
        self.topic = topic

    @abstractmethod
    def publish(self, event: Event) -> None:
        ...


class LocalPublisher(Publisher):
    def publish(self, event: Event) -> None:
        self.topic.publish(event)


async def main():
    print("START")
    topic = Topic("test")
    # topic.register_subscriber(1)
    # topic.register_subscriber(2)
    publisher = LocalPublisher()
    print("YOLO")
    publisher.register_topic(topic)

    publisher.publish(Event(EventType.dice_roll, {"dice_1": 1, "dice_2": 2}))
    print("add1")
    publisher.publish(Event(EventType.dice_roll, {"dice_1": 3, "dice_2": 4}))
    print("add2")
    publisher.publish(Event(EventType.dice_roll, {"dice_1": 5, "dice_2": 6}))
    print("add3")


if __name__ == "__main__":
    asyncio.run(main())
