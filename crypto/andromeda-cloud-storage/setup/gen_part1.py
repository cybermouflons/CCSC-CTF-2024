from secret import FLAG_PART_1
from encoder import Encoder

def generate_example():
    example = b"""In the neon-lit depths of the digital expanse, where the
whispers of ancient myths intertwine with the hum of overclocked processors,
a clandestine call echoes through the cybernetic ether. You, a skilled hacker,
find yourself thrust into the clandestine world of the Andromeda Initiative,
tasked with dismantling the sinister Project Echo devised by the omnipotent
OrionTech. Amidst the sprawling virtual landscapes of Cyprus, where the
echoes of history collide with cyberpunk rebellion, your keyboard becomes
a weapon of choice, and your wit a formidable shield against the encroaching
darkness. As you navigate the treacherous labyrinth of encrypted mysteries
and forge unlikely alliances with rogue AIs, the line between friend and foe
blurs in this high-stakes shadow war. The fate of global autonomy hangs in
the balance, and the network pulses with anticipation for the legendary deeds
that await. Ok that is enough, here is the first part of the flag. """
    example += b"'" + FLAG_PART_1 + b"'"
    output = Encoder.encode(example)
    assert Encoder.decode(output) == example
    return output


if __name__ == "__main__":
    part_1 = generate_example()
    print(part_1)
