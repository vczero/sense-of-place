import asyncio
import aiohttp
import pandas as pd
from urllib.parse import quote
from tqdm.asyncio import tqdm_asyncio
import time

amap_key = pd.read_csv('./amap_key.csv')['key'].tolist()[0]

semaphore = asyncio.Semaphore(15)
QPS = 15

async def get_lnglat_async(session, placename):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={quote(placename)}&key={amap_key}'
    try:
        async with semaphore:  
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['status'] == '1':
                        loc = data['geocodes'][0]['location'].split(',')
                        longitude = loc[0]
                        latitude = loc[1]
                        return longitude, latitude
                    else:
                        print(f"Error: {data['info']} (Code: {data['infocode']}) for {placename}")
                        return 0, 0
                else:
                    print(f"HTTP Error: {response.status} for {placename}")
                    return 0, 0
    except Exception as e:
        print(f"Network error for {placename}: {e}")
        return 0, 0


async def process_poi(session, row):
    poi_name = row['poi_name']
    cords = await get_lnglat_async(session, poi_name)
    if cords[0] != 0:
        result = [[row['city'], poi_name, cords[0], cords[1]]]
        pd.DataFrame(result, columns=['city', 'poi_name', 'longitude', 'latitude']).to_csv(
            './results/landmark/landmarks_temp_pois_lnglat.csv', mode='a', index=False, header=False)


async def process_with_rate_limit(session, row):
    await process_poi(session, row)
    await asyncio.sleep(1 / QPS)  


async def tans_name2lnglat_async():
    temp = pd.read_csv('./results/landmark/landmarks_temp_poi_names.csv')
    async with aiohttp.ClientSession() as session:
        tasks = [
            process_with_rate_limit(session, row)
            for _, row in temp.iterrows()
        ]
        await tqdm_asyncio.gather(*tasks, desc="Processing POIs")


if __name__ == "__main__":
    with open('./results/landmark/landmarks_temp_pois_lnglat.csv', 'w') as f:
        f.write('city,poi_name,longitude,latitude\n')

    asyncio.run(tans_name2lnglat_async())
