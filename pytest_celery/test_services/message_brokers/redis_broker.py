from __future__ import annotations

from functools import cached_property

from kombu import Queue
from redis.client import Redis
from testcontainers.redis import RedisContainer

from pytest_celery.nodes.message_brokers import RedisNode
from pytest_celery.test_services.message_brokers import MessageBroker
from pytest_celery.utils.compat import List


class RedisBroker(MessageBroker):
    @property
    def url(self):
        pass

    def __init__(
        self, test_session_id: str, port: int = None, container: RedisContainer = None
    ):
        self._vhost_counter = 0
        container = container or RedisContainer(port_to_expose=port or 6379)

        super().__init__(container, test_session_id)

    @property
    def queues(self) -> List[Queue]:
        pass

    @cached_property
    def client(self) -> Redis:
        return self.container.get_client()

    def ping(self) -> None:
        self.client.ping()

    def to_node(self) -> RedisNode:
        self._vhost_counter += 1
        return RedisNode(self, vhost_name=self._vhost_counter)

    def __repr__(self):
        # todo add configuration details to repr once they are added to this class
        return f"Redis Broker <port={self.container.port_to_expose}>"
