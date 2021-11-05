# CBZ resizer

A (not-so) convenient Python script that help you mass resize images in CBZ file.

# Prerequisite

1. Install Python 3 (3.6+ is recommended).
2. Run `pip3 install requirements.txt`.

# Usage

```
python3 main.py [-h] --max_width MAX_WIDTH --max_height MAX_HEIGHT --output_dir OUTPUT_DIR file [file ...]
```

* `file`: path to file
* `--max_width MAX_WIDTH`: max destination width
* `--max_height MAX_HEIGHT`: max destination height
* `--output_dir OUTPUT_DIR`: path to save file(s)
* `-h`: show help (optional)