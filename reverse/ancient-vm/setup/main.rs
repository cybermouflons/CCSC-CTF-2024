use std::fs::OpenOptions;
use std::io::Write;

fn main() {
    // Read flag from file
    let flag = match std::fs::read_to_string("flag.txt") {
        Ok(contents) => contents.trim().to_string(),
        Err(_) => {
            println!("Failed to read flag file");
            return;
        }
    };

    // Read program from file
    let program = match std::fs::read("program.txt") {
        Ok(contents) => contents,
        Err(_) => {
            println!("Failed to read program file");
            return;
        }
    };

    // Execute the program
    execute_program(&flag, &program);
}

fn execute_program(flag: &str, program: &[u8]) {
    let mut idx = 0;

    while idx < program.len() {
        let opcode = program[idx];
        idx += 1;

        // Extract arguments based on the opcode
        let idx1 = program[idx] as usize;
        let idx2 = program[idx + 1] as usize;
        let l = program[idx + 2] as usize;
        idx += 3;

        let slice1 = &flag[idx1..idx1 + l];
        let slice2 = &flag[idx2..idx2 + l];

        // Execute the opcode and write the result to output.txt
        let result = match opcode {
            b'x' => {
                xor(slice1, slice2)
            },
            b'a' => {
                add(slice1, slice2)
            },
            b's' => {
                sub(slice1, slice2)
            },
            b'm' => {
                mul(slice1, slice2)
            },
            b'h' => {
                let shift_amt = program[idx] as u32;
                idx += 1;
                shift(slice1, slice2, shift_amt)
            }
            _ => {
                println!("Unknown opcode: {}", opcode);
                continue;
            }
        };

        // Write the result to output.txt
        if let Err(e) = write_output(result) {
            println!("Error writing to output.txt: {}", e);
            return;
        }
    }
}

fn xor(s1: &str, s2: &str) -> i32 {
    s1.bytes().zip(s2.bytes()).fold(0, |acc, (a, b)| acc + (a as i32 ^ b as i32))
}

fn add(s1: &str, s2: &str) -> i32 {
    s1.bytes().zip(s2.bytes()).fold(0, |acc, (a, b)| acc + (a as i32 + b as i32))
}

fn sub(s1: &str, s2: &str) -> i32 {
    s1.bytes().zip(s2.bytes()).fold(0, |acc, (a, b)| acc + (a as i32 - b as i32))
}

fn mul(s1: &str, s2: &str) -> i32 {
    s1.bytes().zip(s2.bytes()).fold(0, |acc, (a, b)| acc + (a as i32 * b as i32))
}

fn shift(s1: &str, s2: &str, shift_amt: u32) -> i32 {
    s1.bytes().zip(s2.bytes()).fold(0, |acc, (a, b)| {
        acc + ((a as i32) << shift_amt) + ((b as i32) >> shift_amt)
    })
}

fn write_output(result: i32) -> std::io::Result<()> {
    let mut file = OpenOptions::new().create(true).append(true).open("output.txt")?;
    write!(file, "{} ", result)?;
    Ok(())
}
