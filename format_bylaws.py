import re
import json


def normalize_and_structurize(input_path, output_text_path, output_json_path):
    # Read raw text
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Step 1: Normalize delimiters (add spaces around '===' and capitalize keywords)
    def normalize_delimiter(match):
        keyword = match.group(
            1
        ).title()  # 'article' -> 'Article', 'section' -> 'Section'
        content = match.group(2).strip()
        return f"=== {keyword} {content} ===\n"

    normalized_text = re.sub(
        r"===\s*(article|section)\s*([^=]+)\s*===",
        normalize_delimiter,
        raw_text,
        flags=re.IGNORECASE,
    )

    # Write normalized and formatted text for readability
    with open(output_text_path, "w", encoding="utf-8") as f:
        f.write(normalized_text)

    # Step 2: Parse structured JSON
    lines = normalized_text.splitlines()
    structured_data = []
    current_article = None
    current_section = None
    current_content = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Detect article delimiter
        article_match = re.match(r"=== Article ([IVXLCDM]+):\s*(.+?) ===", line)
        if article_match:
            # Save previous section before switching
            if current_section and current_content:
                structured_data.append(
                    {
                        "article": current_article,
                        "section": current_section,
                        "content": " ".join(current_content).strip(),
                    }
                )
                current_content = []
                current_section = None

            roman_numeral = article_match.group(1)
            title = article_match.group(2).strip()
            current_article = f"Article {roman_numeral}: {title}"
            continue

        # Detect section delimiter
        section_match = re.match(r"=== Section (\d+(?:\.\d+)?):\s*(.+?) ===", line)
        if section_match:
            # Save previous section before starting new one
            if current_section and current_content:
                structured_data.append(
                    {
                        "article": current_article,
                        "section": current_section,
                        "content": " ".join(current_content).strip(),
                    }
                )
                current_content = []

            section_num = section_match.group(1)
            section_title = section_match.group(2).strip()
            current_section = f"Section {section_num}: {section_title}"
            continue

        # Otherwise, append line to current content
        if current_article and current_section:
            current_content.append(line)

    # After loop, save any remaining section content
    if current_section and current_content:
        structured_data.append(
            {
                "article": current_article,
                "section": current_section,
                "content": " ".join(current_content).strip(),
            }
        )

    # Write structured JSON
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=2)

    print(f"Formatted text saved to: {output_text_path}")
    print(f"Structured JSON saved to: {output_json_path}")


# Example usage:
normalize_and_structurize(
    "bylaws_joined.txt", "bylaws_formatted.txt", "bylaws_structured.json"
)

# If running as a standalone script, uncomment below:
# if __name__ == "__main__":
#     normalize_and_structurize(
#         "bylaws_joined.txt", "bylaws_formatted.txt", "bylaws_structured.json"
#     )
