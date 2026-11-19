with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "if (networkResponse && networkResponse.status === 200) {",
    "if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {"
)

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated opaque handling in SW!")
