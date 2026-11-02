import asyncio
import time


async def make_coffee():
	print("Start coffee")
	print("Coffee brewing (3 seconds)...")
	await asyncio.sleep(3)
	#time.sleep(3)
	print("Coffee done")


async def make_toast():
	print("Start toast")
	print("Toast toasting (2 seconds)...")
	await asyncio.sleep(2)
	print("Toast done")


async def main():
	start = time.perf_counter()

	await asyncio.gather(
		make_coffee(),
		make_toast(),
	)

	end = time.perf_counter()

	print(
		f"\nTotal duration: "
		f"{end - start:.2f} seconds"
	)


asyncio.run(main())
