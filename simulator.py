"""
simulator.py

This file contains the core logic for the Page Replacement Algorithms:
    1. FIFO      -> fifo()
    2. LRU       -> lru()
    3. Optimal   -> optimal()

Each function takes:
    reference_string : list of integers (the page reference string)
    num_frames        : integer (number of available frames)

Each function returns a dictionary with:
    steps       -> list of step-by-step results (page, frame contents, status)
    hits        -> total number of page hits
    faults      -> total number of page faults
    hit_ratio   -> hits / total references
    fault_ratio -> faults / total references

All three algorithms use a fixed-size list called `frame_array` to represent
the memory frames. Empty frames are represented as None internally, and
converted to "-" when building the step result (so the frontend can display
a dash for empty frames).
"""


def _snapshot(frame_array):
    """Convert the internal frame_array (using None for empty slots)
    into a display-friendly list (using '-' for empty slots)."""
    return [page if page is not None else "-" for page in frame_array]


def fifo(reference_string, num_frames):
    """
    FIFO (First In First Out) Page Replacement Algorithm.

    The oldest page loaded into memory is the first one to be replaced.
    We achieve this using a circular pointer that always points to the
    next frame slot to be replaced once all frames are full.
    """
    frame_array = [None] * num_frames
    pointer = 0  # points to the next frame slot to replace (FIFO order)

    steps = []
    hits = 0
    faults = 0

    for page in reference_string:
        if page in frame_array:
            status = "Hit"
            hits += 1
        else:
            status = "Fault"
            faults += 1

            if None in frame_array:
                # There is a free frame slot available, fill it first.
                empty_index = frame_array.index(None)
                frame_array[empty_index] = page
            else:
                # All frames are full, replace the oldest page (FIFO order).
                frame_array[pointer] = page
                pointer = (pointer + 1) % num_frames

        steps.append({
            "page": page,
            "frames": _snapshot(frame_array),
            "status": status
        })

    total = len(reference_string)
    return {
        "steps": steps,
        "hits": hits,
        "faults": faults,
        "hit_ratio": round(hits / total, 4) if total else 0,
        "fault_ratio": round(faults / total, 4) if total else 0
    }


def lru(reference_string, num_frames):
    """
    LRU (Least Recently Used) Page Replacement Algorithm.

    Replaces the page that has not been used for the longest time.
    We keep a dictionary `last_used` that stores the last index (time)
    at which each page was referenced.
    """
    frame_array = [None] * num_frames
    last_used = {}  # page -> last reference index

    steps = []
    hits = 0
    faults = 0

    for i, page in enumerate(reference_string):
        if page in frame_array:
            status = "Hit"
            hits += 1
        else:
            status = "Fault"
            faults += 1

            if None in frame_array:
                empty_index = frame_array.index(None)
                frame_array[empty_index] = page
            else:
                # Find the page in frame_array that was used least recently.
                lru_page = min(frame_array, key=lambda p: last_used.get(p, -1))
                lru_index = frame_array.index(lru_page)
                frame_array[lru_index] = page

        # Update the "last used" time for the current page.
        last_used[page] = i

        steps.append({
            "page": page,
            "frames": _snapshot(frame_array),
            "status": status
        })

    total = len(reference_string)
    return {
        "steps": steps,
        "hits": hits,
        "faults": faults,
        "hit_ratio": round(hits / total, 4) if total else 0,
        "fault_ratio": round(faults / total, 4) if total else 0
    }


def optimal(reference_string, num_frames):
    """
    Optimal Page Replacement Algorithm.

    Replaces the page that will not be used for the longest time in the
    future (or will never be used again). This requires knowledge of the
    full reference string in advance, so it is mainly used as a
    theoretical benchmark.
    """
    frame_array = [None] * num_frames

    steps = []
    hits = 0
    faults = 0

    n = len(reference_string)

    for i, page in enumerate(reference_string):
        if page in frame_array:
            status = "Hit"
            hits += 1
        else:
            status = "Fault"
            faults += 1

            if None in frame_array:
                empty_index = frame_array.index(None)
                frame_array[empty_index] = page
            else:
                future = reference_string[i + 1:]
                farthest_distance = -1
                index_to_replace = 0

                for idx, existing_page in enumerate(frame_array):
                    if existing_page not in future:
                        # This page is never used again -> best candidate.
                        index_to_replace = idx
                        farthest_distance = n  # force this choice
                        break
                    else:
                        next_use_distance = future.index(existing_page)
                        if next_use_distance > farthest_distance:
                            farthest_distance = next_use_distance
                            index_to_replace = idx

                frame_array[index_to_replace] = page

        steps.append({
            "page": page,
            "frames": _snapshot(frame_array),
            "status": status
        })

    total = len(reference_string)
    return {
        "steps": steps,
        "hits": hits,
        "faults": faults,
        "hit_ratio": round(hits / total, 4) if total else 0,
        "fault_ratio": round(faults / total, 4) if total else 0
    }
