import tkinter as tk
import sys  # Import sys module to use sys.exit()

# Định nghĩa biến root trong phạm vi toàn cục
root = None

# Hàm khi chọn "Chơi với người"
def play_with_player(game):
    global root
    print("Chơi với người đã được chọn!")
    game.change_gamemode('pvp')  # Thay đổi chế độ chơi thành PvP
    root.quit()  # Thoát vòng lặp chính của Tkinter

# Hàm khi chọn "Chơi với máy"
def play_with_computer(game):
    global root
    print("Chơi với máy đã được chọn!")
    game.change_gamemode('ai')  # Thay đổi chế độ chơi thành AI
    root.quit()  # Thoát vòng lặp chính của Tkinter

# Hàm khi chọn "Thoát"
def exit_game():
    global root
    print("Thoát game...")
    root.quit()  # Thoát vòng lặp chính của Tkinter
    sys.exit()  # Thoát hoàn toàn khỏi chương trình

# Hàm thay đổi màu nút khi hover
def on_enter(e):
    e.widget.config(bg="#4CAF50", fg="white")  # Màu khi hover
    e.widget.config(font=("Arial", 16, "bold"))

def on_leave(e):
    e.widget.config(bg="#f1f1f1", fg="black")  # Màu khi không hover
    e.widget.config(font=("Arial", 16))

# Tạo cửa sổ chính với kích thước lớn hơn và nền đẹp
def create_menu_window(game):
    global root
    root = tk.Tk()
    root.title("Game Menu")
    root.geometry("500x500")  # Đặt kích thước cửa sổ (width x height)
    root.config(bg="#FFEB3B")  # Đặt màu nền cửa sổ

    # Tạo một label cho tiêu đề game với font đẹp và màu sắc
    title_label = tk.Label(root, text="Game Menu", font=("Arial", 30, "bold"), bg="#FFEB3B", fg="darkblue")
    title_label.pack(pady=30)

    # Tạo nút "Chơi với người" với kích thước lớn và màu sắc đẹp
    player_button = tk.Button(root, text="Chơi với người", width=25, height=3, font=("Arial", 16), bg="#f1f1f1", fg="black", relief="flat", bd=0, command=lambda: play_with_player(game))
    player_button.pack(pady=15)
    player_button.bind("<Enter>", on_enter)
    player_button.bind("<Leave>", on_leave)

    computer_button = tk.Button(root, text="Chơi với máy", width=25, height=3, font=("Arial", 16), bg="#f1f1f1", fg="black", relief="flat", bd=0, command=lambda: play_with_computer(game))
    computer_button.pack(pady=15)
    computer_button.bind("<Enter>", on_enter)
    computer_button.bind("<Leave>", on_leave)

    exit_button = tk.Button(root, text="Thoát", width=25, height=3, font=("Arial", 16), bg="#f1f1f1", fg="black", relief="flat", bd=0, command=exit_game)
    exit_button.pack(pady=15)
    exit_button.bind("<Enter>", on_enter)
    exit_button.bind("<Leave>", on_leave)

    root.mainloop()
    root.destroy() 