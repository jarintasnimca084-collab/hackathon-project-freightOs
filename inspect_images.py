import os

print("Files in workspace:")
for f in os.listdir('.'):
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        print(f, os.path.getsize(f))

print("\nFiles in freightos:")
for f in os.listdir('freightos'):
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        print(f, os.path.getsize(os.path.join('freightos', f)))
