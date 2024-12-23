import streamlit as st
import pandas as pd

def bubble_sort(data, key_index, ascending=True):
    """Fungsi Bubble Sort yang dapat diurutkan berdasarkan indeks key (penjualan atau harga)"""
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if (ascending and data[j][key_index] > data[j+1][key_index]) or (not ascending and data[j][key_index] < data[j+1][key_index]):
                data[j], data[j+1] = data[j+1], data[j]
    return data

def main():
    st.title("Mengurutkan Data Terlaris di Restoran")

    st.write(
        "Program ini mengurutkan daftar menu restoran berdasarkan jumlah penjualan atau harga per item, "
        "baik secara menaik (ascending) maupun menurun (descending) menggunakan metode Bubble Sort."
    )

    menu_data = st.text_area(
        "Masukkan data menu (format: nama_menu,jumlah_penjualan,harga_per_item per baris):",
        ""
    )

    if menu_data:
        lines = menu_data.splitlines()
        if len(lines) > 20:
            st.error("Jumlah data yang dimasukkan melebihi batas maksimal 20 baris. Mohon kurangi jumlah data.")
            return

    sort_by = st.radio(
        "Pilih kriteria pengurutan:",
        ("Jumlah Penjualan", "Harga")
    )

    sort_order = st.radio(
        "Pilih urutan pengurutan:",
        ("Descending", "Ascending")
    )

    ascending = sort_order == "Ascending"

    if menu_data:
        try:
            menu_list = []

            for line in menu_data.splitlines():
                name, sales, price = line.split(",")
                menu_list.append((name.strip(), int(sales.strip()), float(price.strip())))

            if sort_by == "Jumlah Penjualan":
                key_index = 1
            else:
                key_index = 2

            sorted_menu = bubble_sort(menu_list, key_index, ascending)

            df = pd.DataFrame(sorted_menu, columns=["Nama Menu", "Jumlah Penjualan", "Harga Per Item"])

            df['Harga Per Item'] = df['Harga Per Item'].apply(lambda x: f"Rp {x:,.0f}")

            st.write("### Hasil Pengurutan:")
            st.dataframe(df.style.hide(axis="index"), use_container_width=True)

            st.write("### Grafik Jumlah Penjualan:")
            st.bar_chart(df.set_index("Nama Menu")["Jumlah Penjualan"])

            st.write("### Grafik Harga Per Item:")
            df["Harga Per Item (Angka)"] = df["Harga Per Item"].apply(lambda x: float(x.replace('Rp ', '').replace(',', '')))
            st.line_chart(df.set_index("Nama Menu")["Harga Per Item (Angka)"])

        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses data: {e}")

if __name__ == "__main__":
    main()
