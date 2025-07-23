import os
import tempfile

from src.test_vector_parser import TestVectorParser


def test_parse_simple_test_vectors() -> None:
    content = """a,b;out
                0,0;0
                0,1;0
                1,0;0
                1,1;1"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tv") as f:
        f.write(content)
        temp_path = f.name

    try:
        parser = TestVectorParser()
        vectors = parser.parse_test_file(temp_path)

        assert len(vectors) == 4

        assert vectors[0].inputs == {"a": 0, "b": 0}
        assert vectors[0].expected_outputs == {"out": 0}

        assert vectors[3].inputs == {"a": 1, "b": 1}
        assert vectors[3].expected_outputs == {"out": 1}

    finally:
        os.unlink(temp_path)


def test_parse_multi_output_vectors() -> None:
    content = """a,b;out1,out2
                0,0;0,1
                0,1;1,0
                1,0;1,0
                1,1;0,1"""

    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tv") as f:
        f.write(content)
        temp_path = f.name

    try:
        parser = TestVectorParser()
        vectors = parser.parse_test_file(temp_path)

        assert len(vectors) == 4
        assert vectors[0].expected_outputs == {"out1": 0, "out2": 1}
        assert vectors[1].expected_outputs == {"out1": 1, "out2": 0}

    finally:
        os.unlink(temp_path)
