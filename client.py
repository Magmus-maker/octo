import asyncio


async def send_message():
    reader, writer = await asyncio.open_connection(
        '127.0.0.1', 8888)

    try:
        while True:
            message = input("Enter message to send: ")
            writer.write(message.encode())
            await writer.drain()

    except Exception as e:
        print(f'Exception occurred: {e}')

    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    await send_message()


if __name__ == '__main__':
    asyncio.run(main())
