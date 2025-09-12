import pandas as pd
from xml.sax.saxutils import escape

DATA_FILE = "data.csv"
AIML_FILE = "symptoms.aiml"

# Load raw CSV
df = pd.read_csv(DATA_FILE)

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Clean and standardize
df["symptom"] = df["symptom"].str.strip().str.lower()
df["conditions"] = df["conditions"].astype(str).str.replace(";", ",").str.replace("/", ",")
df["conditions"] = df["conditions"].apply(
    lambda x: ", ".join(sorted({c.strip() for c in x.split(",") if c.strip()}))
)

# Drop duplicates
df = df.drop_duplicates(subset=["symptom"])

# Write AIML
with open(AIML_FILE, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<aiml version="2.0">\n')

    for _, row in df.iterrows():
        symptom = row["symptom"].upper()
        response = escape(row["conditions"])
        f.write(f"  <category>\n    <pattern>{symptom}</pattern>\n")
        f.write(f"    <template>{response}</template>\n  </category>\n")

    # Fallback
    f.write("  <category>\n    <pattern>*</pattern>\n")
    f.write("    <template>🤖 I’m not sure. Please consult a doctor.</template>\n")
    f.write("  </category>\n</aiml>\n")

print(f"✅ AIML file generated: {AIML_FILE}")