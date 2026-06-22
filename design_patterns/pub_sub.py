import asyncio
import random


class MiddleMan:
    def __init__(self):
        self.pub_sub_mapping = {}

    def add_publisher(self, publisher):
        if publisher not in self.pub_sub_mapping:
            self.pub_sub_mapping[publisher] = []
        return

    def remove_publisher(self, publisher):
        if publisher not in self.pub_sub_mapping:
            raise Exception(f"No such publisher: {publisher}")
        del self.pub_sub_mapping[publisher]
        return

    def add_subscriber(self, publisher, subscriber):
        if publisher not in self.pub_sub_mapping:
            raise Exception(f"No such publisher: {publisher}")
        if subscriber not in self.pub_sub_mapping[publisher]:
            self.pub_sub_mapping[publisher].append(subscriber)
            print(f"Successfully added {subscriber} to {publisher}")
        return

    def remove_subscriber(self, publisher, subscriber):
        if publisher not in self.pub_sub_mapping:
            raise Exception(f"No such publisher: {publisher}")
        if subscriber in self.pub_sub_mapping[publisher]:
            self.pub_sub_mapping[publisher].remove(subscriber)
            print(f"Successfully removed {subscriber} from {publisher}")

    async def publish_message(self, publisher, message):
        if publisher not in self.pub_sub_mapping:
            return
        # use copy() to prevent failure when there are subscriber that get unsubscribed while this is iterating
        for subscriber in self.pub_sub_mapping[publisher].copy():
            await subscriber.queue.put(message)
        return


class Publisher:
    def __init__(self, middleman, name):
        self.middleman = middleman
        self.name = name
        self.middleman.add_publisher(self)

    async def notify(self, message):
        await self.middleman.publish_message(self, message)
        return


class Subscriber:
    def __init__(self, middleman, name):
        # maxsize is to prevent too many messages if the subscriber is not listening at all
        self.queue = asyncio.Queue(maxsize=100)
        self.name = name
        self.middleman = middleman

    def subscribe(self, publisher):
        self.middleman.add_subscriber(publisher, self)
        return
    
    def unsubscribe(self, publisher):
        self.middleman.remove_subscriber(publisher, self)
        return

    async def wait_for_message(self):
        while True:
            message = await self.queue.get()
            print(f"{self.name} Managed to get message: {message}")
            # task_done() is needed to reduce the Q
            self.queue.task_done()


async def generate_messages(publisher, num_messages):
    for i in range(1, num_messages + 1):
        await publisher.notify(f"{publisher.name} Data Payload {i}")
        # Random sleep to simulate real-world chaotic network traffic
        await asyncio.sleep(random.randint(1, 5))

async def random_unsubscribe(subscriber, publisher, min_delay, max_delay):
    """Waits a random amount of time, then unsubscribes."""
    delay = random.uniform(min_delay, max_delay)
    await asyncio.sleep(delay)
    
    print(f"\n[ACTION] Initiating random unsubscribe for {subscriber.name} after {delay:.2f} seconds...")
    try:
        subscriber.unsubscribe(publisher)
    except Exception as e:
        print(f"[ERROR] Failed to unsubscribe: {e}")

async def main():
    middleman = MiddleMan()

    pub_A = Publisher(middleman, "pub_A")
    pub_B = Publisher(middleman, "pub_B")
    pub_C = Publisher(middleman, "pub_C")

    sub_A = Subscriber(middleman, "sub_A")
    sub_A.subscribe(pub_A)
    sub_A.subscribe(pub_B)
    sub_A.subscribe(pub_C)

    sub_B = Subscriber(middleman, "sub_B")
    sub_B.subscribe(pub_A)
    sub_B.subscribe(pub_C)

    sub_C = Subscriber(middleman, "sub_C")
    sub_C.subscribe(pub_C)

    sub_tasks = [
        asyncio.create_task(sub_A.wait_for_message()),
        asyncio.create_task(sub_B.wait_for_message()),
        asyncio.create_task(sub_C.wait_for_message()),
    ]

    await asyncio.sleep(0.5)
    print("\n--- STARTING PUBLISHERS AND RANDOM UNSUBSCRIBE TIMERS ---\n")

    async with asyncio.TaskGroup() as tg:
        # 1. Start all publishers
        tg.create_task(generate_messages(pub_A, 5))
        tg.create_task(generate_messages(pub_B, 5))
        tg.create_task(generate_messages(pub_C, 5))
        
        # 2. Schedule random unsubscribes concurrently!
        # This will happen somewhere between 1 and 4 seconds into the broadcast
        tg.create_task(random_unsubscribe(sub_C, pub_C, 1.0, 4.0))
        
        # FIX: sub_B is only subscribed to A and C, so let's unsubscribe it from C
        tg.create_task(random_unsubscribe(sub_B, pub_C, 1.0, 4.0))
    
    await asyncio.sleep(0.1)

    print("Waiting for subscribers to finish processing remaining messages...")
    await sub_A.queue.join()
    await sub_B.queue.join()
    await sub_C.queue.join()
    
    for sub_task in sub_tasks:
        sub_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
