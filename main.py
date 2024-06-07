import requests
from pypresence import Presence
import time
from datetime import datetime, timedelta

def fetch_data_from_api():
    api_url = "https://idn-api-live-jkt48.vercel.app/api/jkt48"
    response = requests.get(api_url)
    data = response.json()

    if len(data) > 0:
        user = data[0]['user']
        image = data[0]['image']
        stream_url = data[0]['stream_url']
        title = data[0]['title']
        view_count = data[0]['view_count']
        live_at = data[0]['live_at']
        slug = data[0]['slug']
        return user, image, stream_url, title, view_count, live_at, slug
    else:
        return None

def create_rich_presence(user, image, stream_url, title, view_count, live_at, slug):
    client_id = 'CLIENT_ID'  # Ganti dengan client ID aplikasi Discord Anda
    RPC = Presence(client_id)
    RPC.connect()

    # Konversi live_at dari UTC ke WIB
    live_at_utc = datetime.strptime(live_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    live_at_wib = live_at_utc + timedelta(hours=7)
    start_time = int(time.mktime(live_at_wib.timetuple()))

    # Siapkan data untuk Rich Presence
    state = f"Live: {title}"
    details = f"Views: {view_count}"
    large_image = user['avatar']
    large_text = user['name']

    # URL tombol "Watch Stream"
    watch_stream_url = f"https://www.idn.app/{user['username']}/live/{slug}"

    # Set Rich Presence
    RPC.update(
        state=state,
        details=details,
        start=start_time,
        large_image=large_image,
        large_text=large_text,
        buttons=[{"label": "Watch Stream", "url": watch_stream_url}]
    )

    print("Rich Presence updated!")

def main():
    while True:
        data = fetch_data_from_api()
        if data:
            user, image, stream_url, title, view_count, live_at, slug = data
            create_rich_presence(user, image, stream_url, title, view_count, live_at, slug)
        else:
            print("No live stream found.")
        
        # Tunggu 60 detik sebelum memperbarui lagi
        time.sleep(60)

if __name__ == "__main__":
    main()
