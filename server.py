import asyncio
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

clients = []


async def handle_client(reader, writer):
    client_address = writer.get_extra_info('peername')
    print(f'New connection from {client_address}')
    clients.append(writer)

    try:
        while True:
            data = await reader.read(4096)
            if not data:
                break

            decrypted_data = decrypt_message(data)
            message = decrypted_data.decode()
            print(f'Received message from {client_address}: {message}')

            # Broadcast the message to all clients
            for client_writer in clients:
                if client_writer != writer:
                    encrypted_message = encrypt_message(message)
                    client_writer.write(encrypted_message)
                    await client_writer.drain()

    except Exception as e:
        print(f'Exception occurred for {client_address}: {e}')

    finally:
        clients.remove(writer)
        print(f'Connection from {client_address} closed')
        writer.close()
        await writer.wait_closed()


def decrypt_message(encrypted_data):
    # Replace with your decryption logic
    # In a real application, you'd securely load your private key
    # and decrypt the data.
    return encrypted_data


def encrypt_message(message):
    # Replace with your encryption logic
    # In a real application, you'd securely load the recipient's
    # public key and encrypt the message.
    return message.encode()


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
