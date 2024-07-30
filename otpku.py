import requests
from tabulate import tabulate

def read_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def connect(api_key, url, post_data=None):
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
    }
    try:
        if post_data:
            response = requests.post(url, data=post_data, headers=headers)
        else:
            response = requests.get(url, headers=headers)
        
        response.raise_for_status()  # Memastikan HTTP request berhasil
        print("Status kode:", response.status_code)  # Menampilkan kode status
        return response.json()  # Mengembalikan hasil sebagai JSON
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat menghubungi API: {e}")
        return None

def create_order(api_key, service_id, operator):
    api_url = f'https://otpku.id/api/json.php?api_key={api_key}&action=order&service={service_id}&operator={operator}'
    return connect(api_key, api_url)

def get_sms_otp(api_key):
    api_url = f'https://otpku.id/api/json.php?api_key={api_key}&action=active_order'
    return connect(api_key, api_url)

def check_status(api_key, order_id):
    api_url = f'https://otpku.id/api/json.php?api_key={api_key}&action=status&id={order_id}'
    return connect(api_key, api_url)

def set_status(api_key, order_id, status):
    api_url = f'https://otpku.id/api/json.php?api_key={api_key}&action=set_status&id={order_id}&status={status}'
    return connect(api_key, api_url)

def get_services(api_key):
    api_url = f'https://otpku.id/api/json.php?api_key={api_key}&action=services&country=indo'
    return connect(api_key, api_url)

def display_services(services):
    if services is None or services.get("status") == False:
        print("Status:", services.get("status") if services else "Unknown")
        print("Pesan:", services.get("data", {}).get("msg", "Tidak ada pesan error."))
    else:
        data = services.get("data", [])
        if isinstance(data, list) and data:
            # Mengatur data dalam format tabel
            table = []
            for item in data:
                table.append([
                    item.get("id"),
                    item.get("name"),
                    item.get("price"),
                    item.get("tersedia"),
                    item.get("country"),
                    item.get("status"),
                    item.get("category")
                ])
            headers = ["ID", "Name", "Price", "Tersedia", "Country", "Status", "Category"]
            print(tabulate(table, headers=headers, tablefmt="grid"))
        else:
            print("Tidak ada data untuk ditampilkan.")

def main():
    api_key = read_api_key('api_key.txt')
    
    while True:
        print("\n--- Menu ---")
        print("1. Membuat pesanan")
        print("2. Mendapatkan SMS OTP")
        print("3. Memeriksa status pesanan")
        print("4. Mengubah status pesanan")
        print("5. Mendapatkan layanan")
        print("6. Keluar")
        
        choice = input("Pilih menu (1-6): ")
        
        if choice == '1':
            service_id = input("Masukkan ID layanan: ")
            operator = input("Masukkan operator (telkomsel, axis, indosat, any): ").lower()
            if operator not in ['telkomsel', 'axis', 'indosat', 'any']:
                print("Operator tidak valid. Pilih dari telkomsel, axis, indosat, atau any.")
            else:
                result = create_order(api_key, service_id, operator)
                print("Hasil:", result)
        
        elif choice == '2':
            result = get_sms_otp(api_key)
            print("Hasil:", result)
        
        elif choice == '3':
            order_id = input("Masukkan ID pesanan: ")
            result = check_status(api_key, order_id)
            print("Hasil:", result)
        
        elif choice == '4':
            order_id = input("Masukkan ID pesanan: ")
            status = input("Masukkan status (1=ready, 2=cancel, 3=resend, 4=selesai): ")
            if status not in ['1', '2', '3', '4']:
                print("Status tidak valid. Pilih dari 1=ready, 2=cancel, 3=resend, 4=selesai.")
            else:
                result = set_status(api_key, order_id, status)
                print("Hasil:", result)
        
        elif choice == '5':
            services = get_services(api_key)
            display_services(services)
        
        elif choice == '6':
            print("Keluar dari program.")
            break
        
        else:
            print("Pilihan tidak valid. Silakan pilih antara 1-6.")

if __name__ == "__main__":
    main()
