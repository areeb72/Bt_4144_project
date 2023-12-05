import cv2
import hashlib

def block_hash(image, block_size=(8, 8)):
    hash_values = []
    
    for y in range(0, image.shape[0], block_size[0]):
        for x in range(0, image.shape[1], block_size[1]):
            block = image[y:y + block_size[0], x:x + block_size[1]]
            hash_value = hashlib.md5(block.tobytes()).hexdigest()
            hash_values.append(hash_value)
    return hash_values

def image_hash(image_path, block_size=(8, 8)):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError("Image not found at {image_path}")

    hash_values = block_hash(image, block_size)
    return hash_values

def compare_hashes(hash1, hash2):
    similarity = sum(x == y for x, y in zip(hash1, hash2)) / len(hash1)
    return similarity

def main():
    # Provide the paths to the original and potentially forged images
    original_image_path = "Planet9_3840x2160.jpg"
    forged_image_path = "Screenshot (3).png"

    # Adjust block_size according to your preference (smaller values increase sensitivity)
    block_size = (8, 8)

    # Calculate hash values for original and forged images
    original_hash = image_hash("Planet9_3840x2160.jpg", block_size)
    forged_hash = image_hash("20scse1010362.jpeg", block_size)

    # Compare the hash values
    similarity = compare_hashes(original_hash, forged_hash)

    # You can set a threshold for similarity below which you consider the image forged
    threshold = 0.95

    if similarity < threshold:
        print("Forgery detected! The images are significantly different.")
    else:
        print("Images are similar. Likely not a forgery.")

if __name__ == "__main__":
    main()
