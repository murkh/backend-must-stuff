import asyncio


class RequestCoalescer:
    def __init__(self):
        self._in_flight = {}
        self._lock = asyncio.Lock()

    async def execute(self, key: str, fetch_fnc):
        async with self._lock:
            if key in self._in_flight:
                return await self._in_flight[key]

            future = asyncio.get_event_loop().create_future()
            self._in_flight[key] = future

        try:
            result = await fetch_fnc()
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        finally:
            async with self._lock:
                self._in_flight.pop(key, None)

        return await future
