import tkinter as tk
from PIL import Image, ImageTk 

# Taş resimlerinin bulunduğu klasör
image_folder = "C:/Users/asus/Desktop/satranç projesi/images"

# Tahtanın kare boyutu
square_size = 64

# Taşların başlangıç pozisyonları
start_positions = {
    'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
    'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
    'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
    'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br',
}

# Seçili taş ve pozisyon
selected_piece = None
selected_pos = None

# Oyun sırası (True: Beyaz, False: Siyah)
turn = True

# GUI oluşturma
root = tk.Tk()
root.title("Satranç")
canvas = tk.Canvas(root, width=8 * square_size, height=8 * square_size)
canvas.pack()

# Resim yükleme
images = {}
def load_images():
    for piece in ['wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'bp', 'br', 'bn', 'bb', 'bq', 'bk']:
        images[piece] = ImageTk.PhotoImage(Image.open(f"{image_folder}/{piece}.png").resize((square_size, square_size)))

# Tahtayı çizme
def draw_board():
    colors = ['#f0d9b5', '#b58863']
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            x1 = col * square_size
            y1 = row * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

# Taşları tahtaya yerleştirme
def draw_pieces():
    for pos, piece in start_positions.items():
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        x = col * square_size
        y = row * square_size
        canvas.create_image(x, y, anchor=tk.NW, image=images[piece])

# Taşların hareket edebileceği yerleri gösteren topçukları çizme
def draw_move_circles(valid_moves):
    for move in valid_moves:
        col = ord(move[0]) - ord('a')
        row = 8 - int(move[1])
        x = col * square_size + square_size // 2
        y = row * square_size + square_size // 2
        color = 'white' if selected_piece[0] == 'w' else 'black'
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color)

# Yol üzerindeki taşları kontrol etme
def is_path_clear(start, end):
    start_col = ord(start[0])
    start_row = int(start[1])
    end_col = ord(end[0])
    end_row = int(end[1])

    col_step = 1 if end_col > start_col else -1 if end_col < start_col else 0
    row_step = 1 if end_row > start_row else -1 if end_row < start_row else 0

    current_col = start_col + col_step
    current_row = start_row + row_step

    while current_col != end_col or current_row != end_row:
        pos = f"{chr(current_col)}{current_row}"
        if pos in start_positions:
            return False
        current_col += col_step
        current_row += row_step

    return True

# Taşların hareketini sağlama
def is_valid_move(piece, start, end):
    start_col = ord(start[0])
    start_row = int(start[1])
    end_col = ord(end[0])
    end_row = int(end[1])

    # Hedef karede kendi taşın varsa hareket geçersiz
    if end in start_positions and start_positions[end][0] == piece[0]:
        return False

    # Piyon hareketi
    if piece[1] == 'p':
        if piece[0] == 'w':  # Beyaz piyon
            if start_row == 2 and end_row == 4 and start_col == end_col and end not in start_positions and is_path_clear(start, end):
                return True  # İlk hamlede iki kare ileri
            if end_row == start_row + 1 and start_col == end_col and end not in start_positions:
                return True  # Bir kare ileri
            if end_row == start_row + 1 and abs(end_col - start_col) == 1 and end in start_positions and start_positions[end][0] == 'b':
                return True  # Diagonal alma
        else:  # Siyah piyon
            if start_row == 7 and end_row == 5 and start_col == end_col and end not in start_positions and is_path_clear(start, end):
                return True  # İlk hamlede iki kare ileri
            if end_row == start_row - 1 and start_col == end_col and end not in start_positions:
                return True  # Bir kare ileri
            if end_row == start_row - 1 and abs(end_col - start_col) == 1 and end in start_positions and start_positions[end][0] == 'w':
                return True  # Diagonal alma
        return False

    # Kale hareketi
    if piece[1] == 'r':
        if (start_col == end_col or start_row == end_row) and is_path_clear(start, end):
            return True
        return False

    # At hareketi
    if piece[1] == 'n':
        if (abs(start_col - end_col) == 2 and abs(start_row - end_row) == 1) or (abs(start_col - end_col) == 1 and abs(start_row - end_row) == 2):
            return True
        return False

    # Fil hareketi
    if piece[1] == 'b':
        if abs(start_col - end_col) == abs(start_row - end_row) and is_path_clear(start, end):
            return True
        return False

    # Vezir hareketi
    if piece[1] == 'q':
        if (start_col == end_col or start_row == end_row or abs(start_col - end_col) == abs(start_row - end_row)) and is_path_clear(start, end):
            return True
        return False

    # Şah hareketi
    if piece[1] == 'k':
        if abs(start_col - end_col) <= 1 and abs(start_row - end_row) <= 1:
            return True
        return False

    return False

# Seçili taşın tüm geçerli hareketlerini bulma
def get_valid_moves(piece, start):
    valid_moves = []
    for col in range(8):
        for row in range(8):
            end = f"{chr(col + ord('a'))}{8 - row}"
            if is_valid_move(piece, start, end):
                valid_moves.append(end)
    return valid_moves

# Taşların hareketini sağlama
def on_square_click(event):
    global selected_piece, selected_pos, turn

    col = event.x // square_size
    row = event.y // square_size
    pos = f"{chr(col + ord('a'))}{8 - row}"

    if selected_piece:
        if is_valid_move(selected_piece, selected_pos, pos):
            # Eğer taş seçildiyse ve geçerli hareketse, yeni pozisyona taşı
            del start_positions[selected_pos]
            start_positions[pos] = selected_piece
            turn = not turn  # Sıra değiştir
        selected_piece = None
        selected_pos = None
        draw_board()
        draw_pieces()
    else:
        # Eğer taş seçilmediyse, bu karedeki taşı seç
        if pos in start_positions and ((turn and start_positions[pos][0] == 'w') or (not turn and start_positions[pos][0] == 'b')):
            selected_piece = start_positions[pos]
            selected_pos = pos
            valid_moves = get_valid_moves(selected_piece, selected_pos)
            draw_board()
            draw_pieces()
            draw_move_circles(valid_moves)

# Tahtaya tıklama işlemi
canvas.bind("<Button-1>", on_square_click)

# Tahtayı çiz ve taşları yükle
draw_board()
load_images()
draw_pieces()

root.mainloop()
