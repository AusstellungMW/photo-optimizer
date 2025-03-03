import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import face_recognition


def process_image():
    # Открываем диалог выбора файла
    input_path = filedialog.askopenfilename(filetypes=[("Bilder", "*.jpg;*.jpeg;*.png;*.webp;*.tiff;*.tif")])

    if not input_path:
        return  # Если файл не выбран, выходим

    directory, filename = os.path.split(input_path)
    output_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}_komprimiert.jpg")

    # Открываем изображение
    image = Image.open(input_path)

    # Проверяем, есть ли у TIFF несколько страниц (слоев)
    if hasattr(image, "n_frames") and image.n_frames > 1:
        image.seek(0)  # Берем первую страницу

    # Конвертируем в RGB, если изображение в другом формате (TIFF часто бывает CMYK или с прозрачностью)
    image = image.convert("RGB")

    # Преобразуем в numpy-массив для face_recognition
    image_np = face_recognition.load_image_file(input_path)

    # Ищем лица на фото
    face_locations = face_recognition.face_locations(image_np)

    if face_locations:
        # Берем первое найденное лицо
        top, right, bottom, left = face_locations[0]

        # Определяем центр лица
        face_center_y = (top + bottom) // 2

        # Определяем размеры изображения
        original_width, original_height = image.size
        target_ratio = 16 / 9

        # Если изображение слишком широкое – обрезаем по бокам
        if original_width / original_height > target_ratio:
            new_width = int(original_height * target_ratio)
            new_height = original_height
            left = (original_width - new_width) // 2
            top = 0
        else:
            # Если изображение слишком высокое – обрезаем сверху/снизу
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = max(0, face_center_y - new_height // 2)

        # Обрезаем изображение
        image_cropped = image.crop((left, top, left + new_width, top + new_height))
    else:
        # Если лиц нет – центрируем как обычно
        original_width, original_height = image.size
        target_ratio = 16 / 9
        if original_width / original_height > target_ratio:
            new_width = int(original_height * target_ratio)
            new_height = original_height
            left = (original_width - new_width) // 2
            top = 0
        else:
            new_width = original_width
            new_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - new_height) // 2
        image_cropped = image.crop((left, top, left + new_width, top + new_height))

    # Масштабируем до 1920x1080
    image_resized = image_cropped.resize((1920, 1080), Image.LANCZOS)

    # Сохраняем с компрессией до 350 KB
    quality = 95
    while quality >= 10:
        image_resized.save(output_path, "JPEG", quality=quality)
        if os.path.getsize(output_path) <= 350 * 1024:
            break
        quality -= 5

    # Выводим сообщение пользователю
    messagebox.showinfo("Готово!", f"Изображение сохранено:\n{output_path}")


# Создаем GUI
root = tk.Tk()
root.title("Фото Оптимизатор")
root.geometry("400x200")

# Кнопка выбора и обработки изображения
btn = tk.Button(root, text="Выбрать изображение", command=process_image, font=("Arial", 14))
btn.pack(pady=50)

# Запуск GUI
root.mainloop()















































