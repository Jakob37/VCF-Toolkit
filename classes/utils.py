def chromosome_sort(raw_val: str) -> int:

    val = raw_val.replace("chr", "")

    remaining = {
        "x": 23,
        "y": 24,
        "m": 25
    }

    try:
        val_int = int(val)
        return val_int
    except:
        val_int = remaining.get(val.lower())
        if val_int:
            return val_int
        return 26



