import sys

def encrypt_file(input_file_path: str, output_file_path: str, key: str) -> None:
    # קריאת התוכן של הקובץ הבינארי
    with open(input_file_path, 'rb') as f:
        data = f.read()

    # יצירת מערך בינארי עבור הנתונים המוצפנים
    encrypted_data = bytearray(data)
    
    # הצפנה באמצעות המפתח
    key_length = len(key)
    for i in range(len(encrypted_data)):
        encrypted_data[i] ^= ord(key[i % key_length])

    # כתיבת הנתונים המוצפנים לקובץ פלט
    with open(output_file_path, 'wb') as f:
        f.write(encrypted_data)

if __name__ == "__main__":
    # בדיקת קלט מהשורה הפקודה
    if len(sys.argv) != 4:
        print("Usage: python encrypt.py <input_file> <output_file> <key>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    encryption_key = sys.argv[3]

    encrypt_file(input_file, output_file, encryption_key)
    print(f"File '{input_file}' has been encrypted and saved as '{output_file}' using key '{encryption_key}'")

# Usage: python encrypt.py <input_file> <output_file> <key>
# python encrypt.py input.bin encrypted.bin MySecretKey
