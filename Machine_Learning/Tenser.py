"""
TensorFlow "Hello, world" example.

Notes (PowerShell):
    - Activate your venv/conda env first.
    - Ensure TensorFlow is installed: `pip install tensorflow`
"""

from __future__ import annotations
def main() -> None:
    try:
        import tensorflow as tf
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "TensorFlow is not installed. Install it with: pip install tensorflow"
        ) from exc

    hello = tf.constant("Hello, TensorFlow!")

    # TF2 runs in eager mode by default; print the value cleanly.
    value = hello.numpy()
    if isinstance(value, (bytes, bytearray)):
        print(value.decode("utf-8"))
    else:
        print(value)
if __name__ == "__main__":
    main()

