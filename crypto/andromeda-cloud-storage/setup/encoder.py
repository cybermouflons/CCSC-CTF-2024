class Encoder:
    ASCII_CHARS = [bytes([i]) for i in range(128)]
    WINDOW_SIZE = 16
    MAX_COMPRESSION_SIZE = 2**3

    @classmethod
    def encode(cls, input: bytes) -> bytes:
        is_valid = all(0 <= b <= 127 for b in input)

        if not is_valid:
            raise ValueError("Not a valid ASCII input (0 <= ord(char) <= 127).")

        output = b""
        end_idx = len(input) - 1

        while end_idx >= 0:
            is_compressed = False
            start_idx = None
            for compression_size in range(cls.MAX_COMPRESSION_SIZE, 0, -1):
                start_idx = end_idx - (compression_size - 1)
                if start_idx < compression_size:
                    continue
                candidate_compression = input[start_idx : end_idx + 1]
                compression_window = input[
                    max(start_idx - cls.WINDOW_SIZE, 0) : start_idx
                ]
                occurance_idx = compression_window.rfind(candidate_compression)
                if occurance_idx == -1:
                    continue
                distance = len(compression_window) - (occurance_idx + 1)
                length = compression_size - 1
                code = bytes([(1 << 7) | (distance << 3) | (length)])
                output = code + output
                is_compressed = True
                break

            if not is_compressed:
                code = bytes([input[end_idx]])
                output = code + output
            end_idx -= compression_size

        return output

    @classmethod
    def decode(cls, input: bytes) -> bytes:
        output = b""
        output_len = 0
        for code in input:
            if (code >> 7) == 0:
                output += bytes([code])
                output_len += 1
                continue
            distance = ((code >> 3) & 0b1111) + 1
            length = (code & 0b111) + 1

            if distance > output_len:
                raise ValueError("Output is not long enough.")

            if length > distance:
                raise ValueError("Length of compression is shorter than the distance.")

            end_idx = -distance + length
            if end_idx >= 0:
                output += output[-distance:]
            else:
                output += output[-distance:end_idx]
            output_len += length
        return output


def test():
    a_test = b"Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
    assert Encoder.decode(Encoder.encode(a_test)) == a_test

    b_test = b"In information theory, data compression, source coding, or bit-rate reduction is the process of encoding information using fewer bits than the original representation. Any particular compression is either lossy or lossless. Lossless compression reduces bits by identifying and eliminating statistical redundancy. No information is lost in lossless compression. Lossy compression reduces bits by removing unnecessary or less important information. Typically, a device that performs data compression is referred to as an encoder, and one that performs the reversal of the process (decompression) as a decoder."
    assert Encoder.decode(Encoder.encode(b_test)) == b_test


if __name__ == "__main__":
    test()
