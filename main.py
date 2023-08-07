# Standard
import argparse

# Pip
# None

# Custom
from dp_np_kongru import quick_analysis

parser = argparse.ArgumentParser(description="DeNp Kongru")

# Add an optional argument for the name
parser.add_argument(
    "--einfach", action="store_true", help="Eine einfache Analyse durchfuehren"
)

args = parser.parse_args()

if __name__ == "__main__":

    if args.einfach:
        quick_analysis.run_quick_analysis()
