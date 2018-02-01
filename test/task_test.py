import asyncio
import random
async def fac():
	i = random.randint(1, 3)
	print("Sleep %d" % (i,))
	await asyncio.sleep(i)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
	fac("A", 2),
	fac("B", 3),
	fac("C", 4),
))
loop.close()