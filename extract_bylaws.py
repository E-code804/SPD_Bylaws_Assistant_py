import pdfplumber

# Extract text from pdf.
# text = ""
# with pdfplumber.open("bylaws.pdf") as pdf:
#     for page in pdf.pages:
#         text += page.extract_text() + "\n"

# with open("bylaws_raw.txt", "w") as f:
#     f.write(text)

# Give articles and section the === delimiter.
# print("Starting wrapping...")
# with open("bylaws_raw2.txt", "r") as fin, open("bylaws_wrapped.txt", "w") as fout:
#     for line in fin:
#         stripped = line.rstrip("\n")
#         parts = stripped.split()
#         if parts and parts[0] in ("Article", "Section"):
#             fout.write(f"==={stripped}===\n")
#         else:
#             fout.write(f"{stripped}\n")

# Dealing with text wrapping
lines = open("bylaws_raw.txt").readlines()
joined = " ".join([line.strip() for line in lines if line.strip()])

with open("bylaws_joined.txt", "w") as fout:
    fout.write(joined)
